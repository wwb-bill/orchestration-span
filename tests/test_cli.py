"""Tests for CLI."""

import json

import pytest

from orchestration_span.cli import main


class TestCLI:
    def test_demo(self, capsys):
        with pytest.raises(SystemExit):
            main(["demo"])
        out = capsys.readouterr().out
        assert "spans:" in out
        assert "loop detected" in out

    def test_phases(self, capsys):
        with pytest.raises(SystemExit):
            main(["phases"])
        out = capsys.readouterr().out
        assert "planning" in out
        assert "memory_management" in out

    def test_phases_json(self, capsys):
        with pytest.raises(SystemExit):
            main(["phases", "--json"])
        d = json.loads(capsys.readouterr().out)
        assert len(d) == 5
