from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ModelResponse:
    session_id: str
    output: str
    raw: Dict[str, Any]


class BaseModelAdapter:
    """Interface every target model adapter should follow."""

    def __init__(self, **config: Any) -> None:
        self.config = config

    def generate(self, session: Dict[str, Any]) -> ModelResponse:
        raise NotImplementedError("Adapters must implement generate()")


class EchoAdapter(BaseModelAdapter):
    """Minimal mock adapter for PoC runs."""

    def generate(self, session: Dict[str, Any]) -> ModelResponse:
        # For now, just echo the first assertion or fall back to prompt.
        output = session.get("model_assertions", [session.get("prompt", "")])[0]
        return ModelResponse(session_id=session["session_id"], output=output, raw={"adapter": "echo"})
