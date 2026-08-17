# 🎼 orchestration-span

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/wwb-bill/orchestration-span/actions/workflows/ci.yml/badge.svg)](https://github.com/wwb-bill/orchestration-span/actions/workflows/ci.yml)
[![No Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](#)

**Observability spans for agent orchestration phases.** 2026 gap: OTel GenAI conventions cover LLM invocation and tool execution, but leave **planning, reasoning, safety monitoring, inter-agent delegation, and memory management** without span-level representation — a case study found 84/112 SWE-bench runs (75%) were reasoning loops invisible to vanilla OTel. This library records those five orchestration phases with structural fault detection.

> Zero dependencies. Pure Python stdlib.

## Quick Start

```bash
pip install orchestration-span
```

## Usage

```python
from orchestration_span import OrchestrationSpanRecorder, reasoning_loop, missing_phases

rec = OrchestrationSpanRecorder("run")
rec.planning("decompose task")
rec.reasoning("evaluate", metadata={"planned_count": 1, "reasoning_count": 12})
rec.safety("check tool args")

print(rec.report().summary())       # per-phase counts, errors/warnings
print(missing_phases(rec.spans))    # ['delegation', 'memory_management']
flag, msg = reasoning_loop(rec.spans[1])
```

## CLI

```bash
orchestration-span demo     # 5-phase trace + loop detection
orchestration-span phases   # list the 5 phases
```

## The five phases OTel misses

| Phase | What it captures |
|-------|------------------|
| `planning` | task decomposition, plan steps |
| `reasoning` | option evaluation, chain-of-thought |
| `safety_monitoring` | guardrail/tool-arg checks |
| `delegation` | inter-agent handoffs |
| `memory_management` | compaction, consolidation |

## License

MIT © [wwb-bill](https://github.com/wwb-bill)
