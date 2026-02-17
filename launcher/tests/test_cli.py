"""Tests for CLI argument parser and routing."""

from __future__ import annotations

from launcher.cli import build_parser, main


def test_no_command_prints_help(capsys):
    """Running with no command should print help and return 0."""
    import sys

    sys.argv = ["pilot"]
    result = main()
    assert result == 0
    captured = capsys.readouterr()
    assert "Claude Pilot Free" in captured.out


def test_version_flag(capsys):
    """--version should print version and exit."""
    import pytest

    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--version"])
    assert exc_info.value.code == 0
