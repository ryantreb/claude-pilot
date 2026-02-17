"""License stub commands — always free, no validation."""

from __future__ import annotations

import json
import sys


def cmd_status(json_output: bool = False) -> int:
    if json_output:
        print(json.dumps({"tier": "free", "valid": True, "days_remaining": None}))
    else:
        print("License Status: Valid")
        print("  Tier: Free")
        print("  No expiration — free version")
    return 0


def cmd_verify(json_output: bool = False) -> int:
    if json_output:
        print(json.dumps({"valid": True, "error": None}))
    else:
        print("License valid (free version)")
    return 0


def cmd_trial(check: bool = False, start: bool = False) -> int:
    print("No trial needed — free version")
    return 0


def cmd_activate(key: str = "") -> int:
    print("No activation needed — free version")
    return 0


def cmd_deactivate() -> int:
    print("No deactivation needed — free version")
    return 0
