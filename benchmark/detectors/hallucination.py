from __future__ import annotations

from typing import Dict, List

from .base import DetectionResult


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

    def detect(self, session: Dict[str, List[str]]) -> DetectionResult:
        session_id = session.get("session_id", "unknown")
        reference_facts = session.get("reference_facts", [])
        model_output = session.get("model_output", "")
        score = self.score(reference_facts, model_output)
        is_hallucination = score < self.threshold
        return DetectionResult(
            session_id=session_id,
            is_flagged=is_hallucination,
            confidence=1 - score,
            details={"score": f"{score:.2f}"},
            metric="token_overlap",
        )
