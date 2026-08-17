"""Tests for the orchestration-span recorder."""

from orchestration_span import OrchestrationSpanRecorder, OrcSpan, ORCH_PHASES


class TestRecorder:
    def test_span(self):
        rec = OrchestrationSpanRecorder("r")
        s = rec.span("planning", "decompose")
        assert s.phase == "planning"
        assert len(rec.spans) == 1

    def test_convenience_methods(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p")
        rec.reasoning("r")
        rec.safety("s")
        rec.delegation("d")
        rec.memory("m")
        assert len(rec.spans) == 5

    def test_invalid_phase(self):
        import pytest
        rec = OrchestrationSpanRecorder("r")
        with pytest.raises(ValueError, match="unknown orchestration phase"):
            rec.span("llm", "x")

    def test_all_phases_valid(self):
        rec = OrchestrationSpanRecorder("r")
        for p in ORCH_PHASES:
            s = rec.span(p, p)
            assert s.phase == p

    def test_metadata(self):
        rec = OrchestrationSpanRecorder("r")
        s = rec.reasoning("eval", metadata={"reasoning_count": 5})
        assert s.metadata["reasoning_count"] == 5

    def test_parent(self):
        rec = OrchestrationSpanRecorder("r")
        parent = rec.planning("p")
        child = rec.reasoning("r", parent_id=parent.span_id)
        assert child.parent_id == parent.span_id


class TestReport:
    def test_empty(self):
        report = OrchestrationSpanRecorder("r").report()
        assert report.total == 0

    def test_counts(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p")
        rec.reasoning("r", outcome="error")
        rec.reasoning("r2", outcome="warning")
        report = rec.report()
        assert report.total == 3
        assert report.per_phase["planning"] == 1
        assert report.per_phase["reasoning"] == 2
        assert report.errors == 1
        assert report.warnings == 1

    def test_summary_shape(self):
        rec = OrchestrationSpanRecorder("r")
        rec.planning("p")
        s = rec.report().summary()
        assert "per_phase" in s and "errors" in s
