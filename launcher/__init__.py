"""Claude Pilot Free — CLI entry point."""


def app() -> int:
    """Main entry point called by the shell wrapper."""
    from .cli import main

    return main()
