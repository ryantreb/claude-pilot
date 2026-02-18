"""CLI argument parser and command routing."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pilot",
        description="Claude Pilot Free — Claude Code is powerful. Pilot makes it reliable.",
    )
    parser.add_argument("--version", action="version", version="0.1.0-free")
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # License commands
    sub_status = subparsers.add_parser("status", help="Show current license status.")
    sub_status.add_argument("--json", dest="json_output", action="store_true")

    sub_verify = subparsers.add_parser("verify", help="Verify license for hook authentication.")
    sub_verify.add_argument("--json", dest="json_output", action="store_true")

    sub_trial = subparsers.add_parser("trial", help="Manage trial status.")
    sub_trial.add_argument("--check", action="store_true")
    sub_trial.add_argument("--start", action="store_true")

    sub_activate = subparsers.add_parser("activate", help="Activate a license key.")
    sub_activate.add_argument("key", nargs="?", default="")

    subparsers.add_parser("deactivate", help="Deactivate license.")

    # Context command
    sub_context = subparsers.add_parser("check-context", help="Check context window usage percentage.")
    sub_context.add_argument("--json", dest="json_output", action="store_true")
    sub_context.add_argument("--threshold", type=int, default=None)

    # Plan command
    sub_plan = subparsers.add_parser("register-plan", help="Register plan association for current session.")
    sub_plan.add_argument("plan_path", help="Plan file path")
    sub_plan.add_argument("status", help="Plan status (PENDING, COMPLETE, VERIFIED)")

    # Sessions command
    sub_sessions = subparsers.add_parser("sessions", help="Show the number of active Pilot sessions.")
    sub_sessions.add_argument("--json", dest="json_output", action="store_true")

    # Worktree command
    sub_worktree = subparsers.add_parser("worktree", help="Manage spec worktrees.")
    wt_sub = sub_worktree.add_subparsers(dest="wt_command", metavar="SUBCOMMAND")

    for name in ("create", "detect", "diff", "sync", "cleanup"):
        p = wt_sub.add_parser(name, help=f"{name.capitalize()} a worktree.")
        p.add_argument("plan_slug", help="Plan slug (e.g., add-auth)")
        p.add_argument("--json", dest="json_output", action="store_true")

    p_status = wt_sub.add_parser("status", help="Show current worktree status.")
    p_status.add_argument("--json", dest="json_output", action="store_true")

    # Statusline command
    subparsers.add_parser("statusline", help="Run status line formatter (called by Claude Code).")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    from .license import cmd_status, cmd_verify, cmd_trial, cmd_activate, cmd_deactivate
    from .context import cmd_check_context
    from .plan import cmd_register_plan
    from .session import cmd_sessions
    from .worktree import (
        cmd_worktree_create, cmd_worktree_detect, cmd_worktree_diff,
        cmd_worktree_sync, cmd_worktree_cleanup, cmd_worktree_status,
    )
    from .statusline_cmd import cmd_statusline

    # Handle worktree subcommands
    if args.command == "worktree":
        wt_dispatch = {
            "create": lambda: cmd_worktree_create(args.plan_slug, getattr(args, "json_output", False)),
            "detect": lambda: cmd_worktree_detect(args.plan_slug, getattr(args, "json_output", False)),
            "diff": lambda: cmd_worktree_diff(args.plan_slug, getattr(args, "json_output", False)),
            "sync": lambda: cmd_worktree_sync(args.plan_slug, getattr(args, "json_output", False)),
            "cleanup": lambda: cmd_worktree_cleanup(args.plan_slug, getattr(args, "json_output", False)),
            "status": lambda: cmd_worktree_status(getattr(args, "json_output", False)),
        }
        wt_cmd = getattr(args, "wt_command", None)
        if wt_cmd and wt_cmd in wt_dispatch:
            return wt_dispatch[wt_cmd]()
        parser.print_help()
        return 0

    dispatch = {
        "status": lambda: cmd_status(json_output=getattr(args, "json_output", False)),
        "verify": lambda: cmd_verify(json_output=getattr(args, "json_output", False)),
        "trial": lambda: cmd_trial(check=getattr(args, "check", False), start=getattr(args, "start", False)),
        "activate": lambda: cmd_activate(key=getattr(args, "key", "")),
        "deactivate": cmd_deactivate,
        "check-context": lambda: cmd_check_context(
            json_output=getattr(args, "json_output", False),
            threshold=getattr(args, "threshold", None),
        ),
        "register-plan": lambda: cmd_register_plan(args.plan_path, args.status),
        "sessions": lambda: cmd_sessions(json_output=getattr(args, "json_output", False)),
        "statusline": cmd_statusline,
    }

    handler = dispatch.get(args.command)
    if handler:
        return handler()

    return 0
