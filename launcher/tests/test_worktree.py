"""Tests for worktree command."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from launcher.worktree import cmd_worktree_detect, cmd_worktree_status, worktree_path_for_slug


def test_worktree_path_for_slug():
    path = worktree_path_for_slug("add-auth", project_root="/home/user/project")
    assert ".worktrees/spec-add-auth-" in str(path)
    assert path.is_absolute()


def test_worktree_detect_not_found(capsys):
    with patch("launcher.worktree._git_worktree_list", return_value=[]):
        result = cmd_worktree_detect("nonexistent", json_output=True)
    assert result == 0
    data = json.loads(capsys.readouterr().out)
    assert data["found"] is False


def test_worktree_status_json(capsys):
    with patch("launcher.worktree._git_worktree_list", return_value=[]):
        result = cmd_worktree_status(json_output=True)
    assert result == 0
    data = json.loads(capsys.readouterr().out)
    assert "worktrees" in data
