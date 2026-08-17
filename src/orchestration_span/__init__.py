"""orchestration-span — observability spans for agent orchestration phases.

2026 gap: OTel GenAI conventions cover LLM invocation and tool execution,
but leave planning, reasoning, safety monitoring, inter-agent delegation,
and memory management without span-level representation — a case study
found 84/112 SWE-bench runs (75%) were reasoning loops invisible to
vanilla OTel. This library records those five orchestration phases with
structural fault detection (reasoning loops, blind-spot phases).

Usage:
    from orchestration_span import OrchestrationSpanRecorder, missing_phases, reasoning_loop

    rec = OrchestrationSpanRecorder("run")
    rec.planning("decompose task")
    rec.reasoning("evaluate", metadata={"planned_count": 1, "reasoning_count": 12})
    print(rec.report().summary())
"""

from .types import OrcSpan, OrcReport, ORCH_PHASES
from .recorder import OrchestrationSpanRecorder
from .detect import reasoning_loop, error_rate, phase_coverage, missing_phases

__version__ = "0.1.0"

__all__ = [
    "OrcSpan",
    "OrcReport",
    "ORCH_PHASES",
    "OrchestrationSpanRecorder",
    "reasoning_loop",
    "error_rate",
    "phase_coverage",
    "missing_phases",
]
