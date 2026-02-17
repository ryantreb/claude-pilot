"""Integration tests — verify CLI matches expected output formats."""

from __future__ import annotations

import json
import subprocess
import sys


def _run_pilot(*args: str) -> subprocess.CompletedProcess:
    """Run pilot CLI via the launcher module."""
    cmd = [sys.executable, "-c", "from launcher import app; exit(app())", *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_status_json_format():
    """status --json should match original format."""
    result = _run_pilot("status", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "tier" in data
    assert data["tier"] == "free"


def test_verify_json_format():
    """verify --json should match original format: {"valid": true, "error": null}."""
    result = _run_pilot("verify", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data == {"valid": True, "error": None}


def test_check_context_json_format():
    """check-context --json should match: {"status": "OK", "percentage": <float>}."""
    result = _run_pilot("check-context", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["status"] == "OK"
    assert isinstance(data["percentage"], (int, float))


def test_sessions_json_format():
    """sessions --json should match: {"count": <int>}."""
    result = _run_pilot("sessions", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "count" in data
    assert isinstance(data["count"], int)


def test_help_output():
    """pilot --help should show usage."""
    result = _run_pilot("--help")
    assert result.returncode == 0
    assert "Claude Pilot Free" in result.stdout


def test_version():
    """pilot --version should show version."""
    result = _run_pilot("--version")
    assert result.returncode == 0
    assert "free" in result.stdout
