"""Core types for orchestration-span."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any

# The five orchestration phases OTel GenAI conventions miss
ORCH_PHASES = ("planning", "reasoning", "safety_monitoring",
               "delegation", "memory_management")


@dataclass
class OrcSpan:
    """An orchestration-phase span."""

    phase: str  # one of ORCH_PHASES
    name: str
    detail: str = ""
    outcome: str = "ok"  # ok | warning | error
    duration_ms: float = 0.0
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str = ""
    ts: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> OrcSpan:
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class OrcReport:
    """Aggregate report over orchestration spans."""

    total: int = 0
    per_phase: dict[str, int] = field(default_factory=dict)
    errors: int = 0
    warnings: int = 0

    def summary(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "per_phase": self.per_phase,
            "errors": self.errors,
            "warnings": self.warnings,
        }
