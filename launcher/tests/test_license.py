"""Tests for license stub commands."""

from __future__ import annotations

import json
import sys

from launcher.license import cmd_status, cmd_verify, cmd_trial, cmd_activate, cmd_deactivate


def test_status_prints_free(capsys):
    result = cmd_status(json_output=False)
    assert result == 0
    captured = capsys.readouterr()
    assert "Free" in captured.out
    assert "Valid" in captured.out


def test_status_json(capsys):
    result = cmd_status(json_output=True)
    assert result == 0
    data = json.loads(capsys.readouterr().out)
    assert data["tier"] == "free"


def test_verify_json(capsys):
    result = cmd_verify(json_output=True)
    assert result == 0
    data = json.loads(capsys.readouterr().out)
    assert data["valid"] is True
    assert data["error"] is None


def test_trial_check(capsys):
    result = cmd_trial(check=True)
    assert result == 0
    captured = capsys.readouterr()
    assert "free" in captured.out.lower()


def test_activate_noop(capsys):
    result = cmd_activate(key="fake-key")
    assert result == 0
    captured = capsys.readouterr()
    assert "free" in captured.out.lower()


def test_deactivate_noop(capsys):
    result = cmd_deactivate()
    assert result == 0
