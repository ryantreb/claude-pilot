"""check-context command — reports context window usage percentage."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def _get_history_path() -> Path:
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))
    return Path(config_dir) / "history.jsonl"


def _read_statusline_cache() -> float | None:
    session_id = os.environ.get("PILOT_SESSION_ID", "").strip()
    if not session_id:
        return None

    cache_file = Path.home() / ".pilot" / "sessions" / session_id / "context-pct.json"
    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text())
        ts = data.get("ts")
        if ts is None or time.time() - ts > 120:
            return None
        return float(data.get("pct", 0))
    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return None


def get_context_percentage() -> float:
    cached = _read_statusline_cache()
    if cached is not None:
        return cached

    history = _get_history_path()
    if not history.exists():
        return 0.0

    try:
        with history.open() as f:
            lines = f.readlines()
        if not lines:
            return 0.0

        last_entry = json.loads(lines[-1])
        tokens_used = last_entry.get("tokensUsed", 0)
        max_tokens = last_entry.get("maxTokens", 200000)

        if max_tokens <= 0:
            return 0.0

        return round((tokens_used / max_tokens) * 100, 1)
    except (json.JSONDecodeError, OSError, KeyError):
        return 0.0


def cmd_check_context(json_output: bool = False, threshold: int | None = None) -> int:
    pct = get_context_percentage()
    exceeded = threshold is not None and pct > threshold

    if json_output:
        print(json.dumps({"status": "OK", "percentage": pct}))
    else:
        print(f"Context usage: {pct:.1f}%")

    return 1 if exceeded else 0
