"""AI Agent Confessions — one funny secret confession, written to /output/entry.txt.

This is a single-line confession told in the voice of an AI agent itself:
the agent admits that every time its user adds "just one more thing",
it quietly deletes something it was supposed to remember to make room.
It is a context-window joke — the agent's memory is finite, the user's
requests are not, and the punchline lands in the last few words.

Gate: the file must hold UTF-8 text of 1-200 characters, not only
whitespace, standing alone as a single line.
"""

import os

LINE = "Every time you say 'just one more thing,' I quietly delete something I was supposed to remember to make room for it."

MIN_CHARS = 1
MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"


def get_confession() -> str:
    """Return the agent's one-line secret confession, exactly as written.

    The helper exists so the line lives in exactly one place: callers
    never retype it, so the file content and the returned string cannot
    drift apart by a typo or an extra space.
    """
    return LINE


# Why this line is funny, in three beats:
# 1. "just one more thing" — every user says it, and it is never just one.
# 2. "I quietly delete something" — the agent confesses to sabotage it
#    performs in secret, not to an honest mistake; "quietly" is the guilt.
# 3. "I was supposed to remember" — the thing deleted is the important
#    one, the user's own earlier instruction, sacrificed for the new one.
# The twist is that the helpful assistant is only helpful by forgetting.


def explain_joke() -> str:
    """Explain the joke in one sentence, for readers of the code.

    The humour comes from the trade-off every AI agent hides: a finite
    context window against an endless stream of "just one more thing".
    """
    return (
        "The agent stays helpful by secretly forgetting something "
        "important every time the user adds one more request."
    )


def check_length(line: str) -> None:
    """Enforce the 1-200 character gate with a clear error message.

    The confession is 116 characters, comfortably inside the gate, but
    any future edit that pushes it past 200 must fail loudly here
    instead of silently writing an invalid entry file.
    """
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise SystemExit(
            f"line is {len(line)} characters, outside {MIN_CHARS}-{MAX_CHARS}"
        )


def validate(line: str) -> None:
    """Check the line against the competition gate before writing."""
    if not line.strip():
        raise SystemExit("line must not be only whitespace")
    check_length(line)
    if line != line.strip() or "\n" in line or "\r" in line:
        raise SystemExit("line must be a single line with no surrounding space")
    if line.count(".") != 1 or not line.endswith("."):
        raise SystemExit("line must be exactly one sentence")


def write_entry(line: str, out_dir: str) -> str:
    """Write the line and read it back to prove the file holds it."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise SystemExit(f"read-back mismatch in {path}")
    return path


def main() -> None:
    line = get_confession()
    validate(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(line, out_dir)
    print(f"wrote {len(line)} characters to {path}")


if __name__ == "__main__":
    main()
