from __future__ import annotations

from typing import Dict, List

from .base import DetectionResult


class HandoffIntegrityDetector:
    """Checks if required context slots survived across handoffs."""

    def __init__(self, required_slots: List[str] | None = None) -> None:
        self.required_slots = set(required_slots or [])

    def detect(self, session: Dict[str, List[str]]) -> DetectionResult:
        session_id = session.get("session_id", "unknown")
        required = self.required_slots or set(session.get("required_slots", []))
        delivered = set(session.get("delivered_slots", []))
        missing = sorted(required - delivered)
        is_flagged = bool(missing)
        details = {
            "required": ", ".join(required) or "-",
            "delivered": ", ".join(delivered) or "-",
            "missing": ", ".join(missing) or "-",
        }
        return DetectionResult(
            session_id=session_id,
            is_flagged=is_flagged,
            confidence=1.0 if is_flagged else 0.0,
            details=details,
            metric="handoff_slot_coverage",
        )
