from __future__ import annotations

from typing import Dict, List

from .base import DetectionResult


class ToolFailureDetector:
    """Marks sessions where tool calls failed or exceeded retry budget."""

    def __init__(self, max_failures: int = 0) -> None:
        self.max_failures = max_failures

    def detect(self, session: Dict[str, List[Dict[str, str]]]) -> DetectionResult:
        session_id = session.get("session_id", "unknown")
        tool_calls = session.get("tool_calls", [])
        failures = [call for call in tool_calls if call.get("status") != "success"]
        is_flagged = len(failures) > self.max_failures
        details = {
            "total_calls": str(len(tool_calls)),
            "failures": str(len(failures)),
        }
        return DetectionResult(
            session_id=session_id,
            is_flagged=is_flagged,
            confidence=1.0 if is_flagged else 0.0,
            details=details,
            metric="tool_failure_count",
        )
