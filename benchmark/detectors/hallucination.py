from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DetectionResult:
    session_id: str
    is_hallucination: bool
    confidence: float
    details: Dict[str, str]


class SimpleHallucinationDetector:
    """Rule-based detector comparing tokens with reference facts."""

    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def score(self, reference_facts: List[str], model_output: str) -> float:
        ref_tokens = set(" ".join(reference_facts).lower().split())
        output_tokens = set(model_output.lower().split())
        if not ref_tokens:
            return 0.0
        return len(ref_tokens & output_tokens) / len(ref_tokens)

    def detect(self, session_id: str, reference_facts: List[str], model_output: str) -> DetectionResult:
        score = self.score(reference_facts, model_output)
        is_hallucination = score < self.threshold
        return DetectionResult(
            session_id=session_id,
            is_hallucination=is_hallucination,
            confidence=1 - score,
            details={"score": f"{score:.2f}"},
        )
