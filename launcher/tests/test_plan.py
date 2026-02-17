"""Tests for register-plan command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from launcher.plan import cmd_register_plan


def test_register_plan_creates_file(tmp_path):
    session_dir = tmp_path / "sessions" / "test-session"
    with patch("launcher.plan._get_session_dir", return_value=session_dir):
        result = cmd_register_plan("docs/plans/my-plan.md", "PENDING")
    assert result == 0

    plan_file = session_dir / "active_plan.json"
    assert plan_file.exists()
    data = json.loads(plan_file.read_text())
    assert data["plan_path"] == "docs/plans/my-plan.md"
    assert data["status"] == "PENDING"


def test_register_plan_updates_existing(tmp_path):
    session_dir = tmp_path / "sessions" / "test-session"
    session_dir.mkdir(parents=True)
    (session_dir / "active_plan.json").write_text(
        json.dumps({"plan_path": "old.md", "status": "PENDING"})
    )
    with patch("launcher.plan._get_session_dir", return_value=session_dir):
        result = cmd_register_plan("new.md", "COMPLETE")
    assert result == 0

    data = json.loads((session_dir / "active_plan.json").read_text())
    assert data["plan_path"] == "new.md"
    assert data["status"] == "COMPLETE"


def test_register_plan_validates_status(capsys):
    result = cmd_register_plan("plan.md", "INVALID")
    assert result == 1
