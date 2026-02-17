"""Tests for sessions command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from launcher.session import cmd_sessions, count_active_sessions


def test_count_no_sessions(tmp_path):
    with patch("launcher.session._get_sessions_base", return_value=tmp_path / "sessions"):
        assert count_active_sessions() == 0


def test_count_with_sessions(tmp_path):
    sessions_dir = tmp_path / "sessions"
    (sessions_dir / "session-1").mkdir(parents=True)
    (sessions_dir / "session-1" / "context-cache.json").write_text("{}")
    (sessions_dir / "session-2").mkdir(parents=True)
    (sessions_dir / "session-2" / "context-cache.json").write_text("{}")
    with patch("launcher.session._get_sessions_base", return_value=sessions_dir):
        assert count_active_sessions() == 2


def test_sessions_json_output(capsys, tmp_path):
    with patch("launcher.session._get_sessions_base", return_value=tmp_path / "sessions"):
        result = cmd_sessions(json_output=True)
    assert result == 0
    data = json.loads(capsys.readouterr().out)
    assert "count" in data
    assert isinstance(data["count"], int)


def test_sessions_text_output(capsys, tmp_path):
    with patch("launcher.session._get_sessions_base", return_value=tmp_path / "sessions"):
        result = cmd_sessions(json_output=False)
    assert result == 0
    captured = capsys.readouterr()
    assert "session" in captured.out.lower()
