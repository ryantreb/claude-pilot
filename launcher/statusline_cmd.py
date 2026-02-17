"""statusline command - formats status bar and caches context percentage."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def _get_session_cache_dir() -> Path:
    session_id = os.environ.get("PILOT_SESSION_ID", "").strip() or "default"
    return Path.home() / ".pilot" / "sessions" / session_id


def _get_claude_session_id() -> str:
    history = Path.home() / ".claude" / "history.jsonl"
    if not history.exists():
        return ""
    try:
        with history.open() as f:
            lines = f.readlines()
            if lines:
                return json.loads(lines[-1]).get("sessionId", "")
    except (json.JSONDecodeError, OSError):
        pass
    return ""


def _read_stdin() -> str:
    try:
        if not sys.stdin.isatty():
            return sys.stdin.read()
    except Exception:
        pass
    return ""


def write_context_cache(pct: float, cc_session_id: str = "") -> None:
    cache_dir = _get_session_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = cache_dir / "context-pct.json"
    data = {"pct": pct, "ts": time.time(), "session_id": cc_session_id}
    try:
        cache_file.write_text(json.dumps(data))
    except OSError:
        pass


def _read_usage_cache() -> dict:
    cache_file = Path.home() / ".pilot" / "cache" / "usage.json"
    if not cache_file.exists():
        return {}
    try:
        return json.loads(cache_file.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _format_bar(pct: float, width: int = 10) -> str:
    filled = int(pct / 100 * width)
    return "\u2593" * filled + "\u2591" * (width - filled)


def _color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"


def cmd_statusline() -> int:
    raw = _read_stdin()
    pct = 0.0

    if raw:
        try:
            data = json.loads(raw)
            pct = float(data.get("context_window_pct", 0))
        except (json.JSONDecodeError, ValueError, TypeError):
            pass

    cc_session_id = _get_claude_session_id()
    write_context_cache(pct, cc_session_id)

    bar = _format_bar(pct)
    pct_color = "32" if pct < 60 else ("33" if pct < 80 else "31")

    usage = _read_usage_cache()
    five_hour = usage.get("five_hour_pct", 0)
    weekly = usage.get("weekly_pct", 0)

    line1 = f"\033[2m{bar}\033[0m {_color(f'{pct:.0f}%', pct_color)}"
    if five_hour or weekly:
        fh_color = "32" if five_hour < 60 else ("33" if five_hour < 80 else "31")
        wk_color = "32" if weekly < 60 else ("33" if weekly < 80 else "31")
        line1 += f" \033[2m|\033[0m 5h: {_color(f'{five_hour:.0f}%', fh_color)} \033[2m|\033[0m 7d: {_color(f'{weekly:.0f}%', wk_color)}"

    line2 = "Pilot: Free \033[2m|\033[0m /spec for complex tasks \033[2m|\033[0m auto-compact preserves all state"

    print(line1)
    print(line2)
    return 0
