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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    from launcher.license import cmd_status, cmd_verify, cmd_trial, cmd_activate, cmd_deactivate

    dispatch = {
        "status": lambda: cmd_status(json_output=getattr(args, "json_output", False)),
        "verify": lambda: cmd_verify(json_output=getattr(args, "json_output", False)),
        "trial": lambda: cmd_trial(check=getattr(args, "check", False), start=getattr(args, "start", False)),
        "activate": lambda: cmd_activate(key=getattr(args, "key", "")),
        "deactivate": cmd_deactivate,
    }

    handler = dispatch.get(args.command)
    if handler:
        return handler()

    return 0
