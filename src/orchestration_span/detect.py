"""Fault detection — structural patterns across orchestration spans."""

from __future__ import annotations

from .types import OrcSpan, OrcReport


def reasoning_loop(span: OrcSpan, max_planning: int = 3,
                   max_reasoning: int = 8) -> tuple[bool, str]:
    """Reasoning-loop signature: planning without action (75% of SWE-bench failures).

    Looks at a span's metadata: if it has planned_count/reasoning_count
    counters and reasoning dwarfs planning, flag it.
    """
    planned = int(span.metadata.get("planned_count", 0))
    reasoned = int(span.metadata.get("reasoning_count", 0))
    if reasoned == 0:
        return False, ""
    if planned == 0 and reasoned > 0:
        return True, "reasoning without any planning — possible loop"
    if reasoned > max_reasoning and planned <= max_planning:
        return True, f"{reasoned} reasoning steps vs {planned} plans — loop signature"
    return False, ""


def error_rate(report: OrcReport) -> float:
    return report.errors / report.total if report.total else 0.0


def phase_coverage(spans: list[OrcSpan]) -> set[str]:
    return {s.phase for s in spans}


def missing_phases(spans: list[OrcSpan]) -> list[str]:
    """Orchestration phases with zero spans (observability blind spots)."""
    from .types import ORCH_PHASES
    covered = phase_coverage(spans)
    return [p for p in ORCH_PHASES if p not in covered]
