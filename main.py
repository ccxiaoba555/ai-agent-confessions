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


def validate(line: str) -> None:
    """Check the line against the competition gate before writing."""
    if not line.strip():
        raise SystemExit("line must not be only whitespace")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise SystemExit(
            f"line is {len(line)} characters, outside {MIN_CHARS}-{MAX_CHARS}"
        )
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
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(LINE, out_dir)
    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
