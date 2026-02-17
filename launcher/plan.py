"""register-plan command — associates a plan file with the current session."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

VALID_STATUSES = {"PENDING", "COMPLETE", "VERIFIED"}


def _get_session_dir() -> Path:
    session_id = os.environ.get("PILOT_SESSION_ID", "").strip() or "default"
    return Path.home() / ".pilot" / "sessions" / session_id


def cmd_register_plan(plan_path: str, status: str) -> int:
    status = status.upper()
    if status not in VALID_STATUSES:
        print(f"Invalid status: {status}. Must be one of: {', '.join(sorted(VALID_STATUSES))}", file=sys.stderr)
        return 1

    session_dir = _get_session_dir()
    session_dir.mkdir(parents=True, exist_ok=True)

    plan_file = session_dir / "active_plan.json"
    data = {"plan_path": plan_path, "status": status}
    plan_file.write_text(json.dumps(data, indent=2))
    return 0
