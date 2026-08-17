# 🎼 orchestration-span

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Agent 编排阶段的观测 span。** 2026 缺口:OTel GenAI 规范覆盖 LLM 调用与工具执行,但把**规划、推理、安全监控、代理间委托、记忆管理**留在了 span 级表示之外——案例研究发现 84/112 个 SWE-bench run(75%)是 vanilla OTel 看不见的推理循环。本库记录这五个编排阶段,并带结构故障检测。

> 零依赖。纯 Python 标准库。

```python
from orchestration_span import OrchestrationSpanRecorder, reasoning_loop, missing_phases
rec = OrchestrationSpanRecorder("run")
rec.planning("decompose task")
rec.reasoning("evaluate", metadata={"planned_count": 1, "reasoning_count": 12})
print(rec.report().summary())
print(missing_phases(rec.spans))
```

```bash
pip install orchestration-span
orchestration-span demo
orchestration-span phases
```

MIT © [wwb-bill](https://github.com/wwb-bill)
