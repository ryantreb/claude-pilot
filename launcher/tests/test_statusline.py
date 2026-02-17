"""Tests for statusline command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from launcher.statusline_cmd import cmd_statusline, write_context_cache


def test_write_context_cache(tmp_path):
    cache_dir = tmp_path / "sessions" / "test-session"
    with patch("launcher.statusline_cmd._get_session_cache_dir", return_value=cache_dir):
        write_context_cache(42.5, "test-cc-session")

    cache_file = cache_dir / "context-pct.json"
    assert cache_file.exists()
    data = json.loads(cache_file.read_text())
    assert data["pct"] == 42.5
    assert "ts" in data
    assert data["session_id"] == "test-cc-session"


def test_statusline_outputs_text(capsys, tmp_path):
    stdin_data = json.dumps({"context_window_pct": 55.0})
    cache_dir = tmp_path / "sessions" / "test"
    with patch("launcher.statusline_cmd._read_stdin", return_value=stdin_data):
        with patch("launcher.statusline_cmd._get_session_cache_dir", return_value=cache_dir):
            result = cmd_statusline()
    assert result == 0
    captured = capsys.readouterr()
    assert "%" in captured.out
