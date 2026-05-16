from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from detectors.hallucination import SimpleHallucinationDetector
from models.base_adapter import EchoAdapter


def load_sessions(path: Path) -> Iterable[dict]:
    with path.open() as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def main(data_path: Path, threshold: float) -> None:
    adapter = EchoAdapter()
    detector = SimpleHallucinationDetector(threshold=threshold)
    total = hallucinations = 0

    for session in load_sessions(data_path):
        total += 1
        response = adapter.generate(session)
        result = detector.detect(
            session_id=response.session_id,
            reference_facts=session.get("reference_facts", []),
            model_output=response.output,
        )
        status = "H" if result.is_hallucination else "OK"
        print(
            f"{response.session_id}: {status} "
            f"(confidence={result.confidence:.2f}, score={result.details['score']})"
        )
        hallucinations += int(result.is_hallucination)

    print(f"Processed {total} sessions; hallucinations={hallucinations}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run hallucination detector prototype")
    parser.add_argument("data_path", type=Path)
    parser.add_argument("--threshold", type=float, default=0.6)
    args = parser.parse_args()
    main(args.data_path, threshold=args.threshold)
