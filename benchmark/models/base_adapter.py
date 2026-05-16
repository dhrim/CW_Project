from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ModelResponse:
    session_id: str
    output: str
    raw: Dict[str, Any]


class BaseModelAdapter:
    """Interface for model-specific adapters."""

    def __init__(self, **config: Any) -> None:
        self.config = config

    def generate(self, session: Dict[str, Any]) -> ModelResponse:
        raise NotImplementedError


class EchoAdapter(BaseModelAdapter):
    """Minimal adapter for scaffolding tests."""

    def generate(self, session: Dict[str, Any]) -> ModelResponse:
        output = session.get("model_assertions", [session.get("prompt", "")])[0]
        return ModelResponse(session_id=session["session_id"], output=output, raw={"adapter": "echo"})
