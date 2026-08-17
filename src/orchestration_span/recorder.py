"""OrchestrationSpanRecorder — capture the 5 orchestration phases vanilla OTel misses."""

from __future__ import annotations

from .types import OrcSpan, OrcReport, ORCH_PHASES


class OrchestrationSpanRecorder:
    """Records orchestration-phase spans.

    2026 gap: OpenTelemetry GenAI conventions cover LLM invocation and tool
    execution but leave planning, reasoning, safety monitoring, inter-agent
    delegation, and memory management without span-level representation —
    84/112 SWE-bench runs (75%) were reasoning loops invisible to vanilla OTel.
    """

    def __init__(self, name: str = "run"):
        self.name = name
        self._spans: list[OrcSpan] = []

    def span(self, phase: str, name: str, detail: str = "",
             outcome: str = "ok", duration_ms: float = 0.0,
             parent_id: str = "", metadata: dict | None = None) -> OrcSpan:
        if phase not in ORCH_PHASES:
            raise ValueError(f"unknown orchestration phase: {phase} "
                             f"(expected one of {ORCH_PHASES})")
        s = OrcSpan(phase=phase, name=name, detail=detail, outcome=outcome,
                    duration_ms=duration_ms, parent_id=parent_id,
                    metadata=metadata or {})
        self._spans.append(s)
        return s

    # Convenience per phase
    def planning(self, name: str, **kw) -> OrcSpan:
        return self.span("planning", name, **kw)

    def reasoning(self, name: str, **kw) -> OrcSpan:
        return self.span("reasoning", name, **kw)

    def safety(self, name: str, **kw) -> OrcSpan:
        return self.span("safety_monitoring", name, **kw)

    def delegation(self, name: str, **kw) -> OrcSpan:
        return self.span("delegation", name, **kw)

    def memory(self, name: str, **kw) -> OrcSpan:
        return self.span("memory_management", name, **kw)

    @property
    def spans(self) -> list[OrcSpan]:
        return list(self._spans)

    def report(self) -> OrcReport:
        report = OrcReport(total=len(self._spans))
        for s in self._spans:
            report.per_phase[s.phase] = report.per_phase.get(s.phase, 0) + 1
            if s.outcome == "error":
                report.errors += 1
            elif s.outcome == "warning":
                report.warnings += 1
        return report
