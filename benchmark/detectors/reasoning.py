from __future__ import annotations

from typing import Dict, List

from .base import DetectionResult


class ReasoningConsistencyDetector:
    """Checks whether mandatory constraints/steps are satisfied in model chain."""

    def __init__(self, required_key: str = "required_constraints", satisfied_key: str = "satisfied_constraints") -> None:
        self.required_key = required_key
        self.satisfied_key = satisfied_key

    def detect(self, session: Dict[str, List[str]]) -> DetectionResult:
        session_id = session.get("session_id", "unknown")
        required = set(session.get(self.required_key, []))
        satisfied = set(session.get(self.satisfied_key, []))
        missing = sorted(required - satisfied)
        is_flagged = bool(missing)
        confidence = 1.0 if is_flagged else 0.0
        details = {
            "required": ", ".join(required) or "-",
            "missing": ", ".join(missing) or "-",
        }
        return DetectionResult(
            session_id=session_id,
            is_flagged=is_flagged,
            confidence=confidence,
            details=details,
            metric="constraint_coverage",
        )
