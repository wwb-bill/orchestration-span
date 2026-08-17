"""CLI for orchestration-span."""

from __future__ import annotations

import json
import sys

from .recorder import OrchestrationSpanRecorder
from .detect import reasoning_loop, missing_phases


def _utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv: list[str] | None = None) -> None:
    args = list(argv) if argv is not None else sys.argv[1:]
    if not args or args[0] in ("--help", "-h"):
        print("orchestration-span — observability spans for agent orchestration phases")
        print("\nUsage:")
        print("  orchestration-span demo")
        print("  orchestration-span phases [--json]")
        sys.exit(0)

    if args[0] == "demo":
        rec = OrchestrationSpanRecorder("demo")
        rec.planning("decompose task", detail="3 subtasks")
        rec.reasoning("evaluate options", outcome="warning",
                      metadata={"planned_count": 1, "reasoning_count": 9})
        rec.safety("check tool args", outcome="ok")
        rec.delegation("handoff to writer", detail="context propagated")
        rec.memory("consolidate session")
        report = rec.report()
        print(f"spans: {report.total}, errors: {report.errors}, warnings: {report.warnings}")
        print("phases:", ", ".join(sorted(report.per_phase)))
        print("missing:", missing_phases(rec.spans) or "none")
        loop, msg = reasoning_loop(rec.spans[1])
        if loop:
            print(f"loop detected: {msg}")
        sys.exit(0)

    if args[0] == "phases":
        if "--json" in args:
            print(json.dumps(list(__import__("orchestration_span.types", fromlist=["ORCH_PHASES"]).ORCH_PHASES)))
        else:
            for p in __import__("orchestration_span.types", fromlist=["ORCH_PHASES"]).ORCH_PHASES:
                print(f"  {p}")
        sys.exit(0)

    print(f"Unknown: {args[0]}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    _utf8_stdout()
    main()
