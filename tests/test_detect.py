"""Tests for fault detection."""

from orchestration_span import (
    OrchestrationSpanRecorder, reasoning_loop, error_rate,
    phase_coverage, missing_phases, OrcSpan,
)


class TestReasoningLoop:
    def test_reasoning_without_planning(self):
        s = OrcSpan(phase="reasoning", name="eval",
                    metadata={"planned_count": 0, "reasoning_count": 3})
        flagged, _ = reasoning_loop(s)
        assert flagged is True

    def test_balanced_ok(self):
        s = OrcSpan(phase="reasoning", name="eval",
                    metadata={"planned_count": 5, "reasoning_count": 3})
        flagged, _ = reasoning_loop(s)
        assert flagged is False

    def test_excessive_reasoning(self):
        s = OrcSpan(phase="reasoning", name="eval",
                    metadata={"planned_count": 2, "reasoning_count": 12})
        flagged, msg = reasoning_loop(s, max_planning=3, max_reasoning=8)
        assert flagged is True
        assert "loop" in msg

    def test_no_counters(self):
        s = OrcSpan(phase="reasoning", name="eval")
        flagged, _ = reasoning_loop(s)
        assert flagged is False

    def test_loop_message(self):
        s = OrcSpan(phase="reasoning", name="eval",
                    metadata={"planned_count": 0, "reasoning_count": 1})
        _, msg = reasoning_loop(s)
        assert "possible loop" in msg


class TestAggregates:
    def test_error_rate(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p", outcome="ok")
        rec.reasoning("r", outcome="error")
        rec.reasoning("r2", outcome="error")
        assert error_rate(rec.report()) == 2 / 3

    def test_error_rate_empty(self):
        from orchestration_span import OrcReport
        assert error_rate(OrcReport()) == 0.0

    def test_phase_coverage(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p")
        rec.safety("s")
        assert phase_coverage(rec.spans) == {"planning", "safety_monitoring"}

    def test_missing_phases(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p")
        missing = missing_phases(rec.spans)
        assert "planning" not in missing
        assert "delegation" in missing
        assert "memory_management" in missing

    def test_full_coverage(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p"); rec.reasoning("r"); rec.safety("s")
        rec.delegation("d"); rec.memory("m")
        assert missing_phases(rec.spans) == []
