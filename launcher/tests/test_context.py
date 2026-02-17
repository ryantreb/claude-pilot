"""Tests for check-context command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from launcher.context import cmd_check_context, get_context_percentage


def test_check_context_json_output(capsys, tmp_path):
    with patch("launcher.context._get_history_path", return_value=tmp_path / "nonexistent"):
        result = cmd_check_context(json_output=True, threshold=None)
    assert result == 0
    data = json.loads(capsys.readouterr().out)
    assert "status" in data
    assert "percentage" in data


def test_check_context_text_output(capsys, tmp_path):
    with patch("launcher.context._get_history_path", return_value=tmp_path / "nonexistent"):
        result = cmd_check_context(json_output=False, threshold=None)
    assert result == 0
    captured = capsys.readouterr()
    assert "%" in captured.out


def test_get_context_percentage_no_history(tmp_path):
    with patch("launcher.context._get_history_path", return_value=tmp_path / "nonexistent"):
        pct = get_context_percentage()
    assert pct == 0.0


def test_check_context_threshold_exceeded(capsys, tmp_path):
    with patch("launcher.context.get_context_percentage", return_value=85.0):
        result = cmd_check_context(json_output=True, threshold=80)
    assert result == 1
