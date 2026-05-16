from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Type

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from detectors.hallucination import DetectionResult  # type: ignore


def load_sessions(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open() as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def import_class(path: str) -> Type[Any]:
    module_name, class_name = path.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def parse_json_arg(value: str | None) -> Dict[str, Any]:
    if not value:
        return {}
    return json.loads(value)


def main(
    data_path: Path,
    adapter_path: str,
    detector_path: str,
    adapter_cfg: Dict[str, Any],
    detector_cfg: Dict[str, Any],
    report_path: Path | None,
) -> None:
    AdapterCls = import_class(adapter_path)
    DetectorCls = import_class(detector_path)

    adapter = AdapterCls(**adapter_cfg)
    detector = DetectorCls(**detector_cfg)

    detections: List[DetectionResult] = []
    total = hallucinations = 0

    for session in load_sessions(data_path):
        total += 1
        response = adapter.generate(session)
        result = detector.detect(
            session_id=response.session_id,
            reference_facts=session.get("reference_facts", []),
            model_output=response.output,
        )
        detections.append(result)
        hallucinations += int(getattr(result, "is_hallucination", False))
        status = "H" if getattr(result, "is_hallucination", False) else "OK"
        score = result.details.get("score") if hasattr(result, "details") else "-"
        print(
            f"{response.session_id}: {status} "
            f"(confidence={getattr(result, 'confidence', 0):.2f}, score={score})"
        )

    print(f"Processed {total} sessions; flagged={hallucinations}")

    if report_path:
        payload = {
            "summary": {
                "total_sessions": total,
                "flagged": hallucinations,
                "adapter": adapter_path,
                "detector": detector_path,
            },
            "detections": [result.__dict__ for result in detections],
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        print(f"Report saved to {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generic benchmark runner")
    parser.add_argument("data_path", type=Path, help="JSONL dataset path")
    parser.add_argument(
        "--adapter",
        default="models.base_adapter:EchoAdapter",
        help="Python path to adapter class (module:Class)",
    )
    parser.add_argument(
        "--detector",
        default="detectors.hallucination:SimpleHallucinationDetector",
        help="Python path to detector class (module:Class)",
    )
    parser.add_argument(
        "--adapter-config",
        dest="adapter_config",
        help="JSON dict passed to adapter constructor",
    )
    parser.add_argument(
        "--detector-config",
        dest="detector_config",
        help="JSON dict passed to detector constructor",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path to save JSON report",
    )
    args = parser.parse_args()
    main(
        data_path=args.data_path,
        adapter_path=args.adapter,
        detector_path=args.detector,
        adapter_cfg=parse_json_arg(args.adapter_config),
        detector_cfg=parse_json_arg(args.detector_config),
        report_path=args.report,
    )
