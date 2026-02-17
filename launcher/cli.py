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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    from launcher.license import cmd_status, cmd_verify, cmd_trial, cmd_activate, cmd_deactivate
    from launcher.context import cmd_check_context
    from launcher.plan import cmd_register_plan
    from launcher.session import cmd_sessions

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
    }

    handler = dispatch.get(args.command)
    if handler:
        return handler()

    return 0
