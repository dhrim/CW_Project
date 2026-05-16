from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class DetectionResult:
    session_id: str
    is_flagged: bool
    confidence: float
    details: Dict[str, str]
    metric: Optional[str] = None
