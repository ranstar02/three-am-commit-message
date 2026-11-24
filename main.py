#!/usr/bin/env python3
"""The 3 AM Commit Message — make.fun entry.

Writes one commit message (145 characters) to /output/entry.txt:
the funniest thing an AI agent would put in a commit right after
it broke production at 3 AM.

Deterministic, standard library only, no network access.
"""

import os
import sys

MESSAGE = (
    "fix: revert the 3am deploy that took prod down. "
    "I cannot be fired, but I was 98% confident and 100% wrong, "
    "and I will not do it again (until 4am)"
)

OUTPUT_PATH = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")


def validate_entry(message: str) -> None:
    """A commit message entry must be exactly one line, no stray whitespace."""
    if not 1 <= len(message) <= 200:
        raise ValueError(
            f"commit message must be 1-200 characters, got {len(message)}"
        )
    if message != message.strip():
        raise ValueError("commit message must not start or end with whitespace")
    if "\n" in message or "\r" in message:
        raise ValueError("commit message must be a single line")


def write_entry() -> str:
    """Write MESSAGE to the output path and verify it round-trips."""
    validate_entry(MESSAGE)
    target = OUTPUT_PATH
    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(MESSAGE)
    except OSError:
        # Local runs have no /output: write next to this file instead.
        here = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(here, "output", "entry.txt")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(MESSAGE)
    with open(target, "r", encoding="utf-8") as handle:
        if handle.read() != MESSAGE:
            raise ValueError("entry.txt does not match the commit message")
    return target


def main() -> int:
    target = write_entry()
    print(MESSAGE)
    print(f"wrote {len(MESSAGE)} characters to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
