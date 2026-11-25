# The Best Advice I Ever Got — winning entry.
# Deterministic, no network, no clock, no randomness.
# Writes exactly one sentence to $MAKEFUN_OUTPUT_DIR/entry.txt
# (and to /output/entry.txt when that is a different directory),
# then reads the file back and fails hard unless it is byte-identical.

import os
from pathlib import Path

ENTRY = (
    "My mother told me the day my father left that love is what "
    "you do after the feeling is gone, and I only understood her "
    "twenty years later."
)


def fail(message):
    raise SystemExit(message)


def sentence_problem(text):
    """Return None when text is exactly one sentence, else the reason."""
    if not text:
        return "empty text"
    if text != text.strip():
        return "leading or trailing whitespace"
    if not text.endswith("."):
        return "does not end with a full stop"
    # A sentence boundary (". " / "? " / "! ") inside the text means >1 sentence.
    for marker in (". ", "? ", "! "):
        if marker in text:
            return "contains more than one sentence"
    if any(ord(c) < 32 for c in text):
        return "contains control characters"
    return None


def validate_entry(text):
    """Final gate, run immediately before writing: re-check the entry
    from scratch so a bad entry can never reach the output file."""
    if not text or not text.strip():
        fail("entry must not be empty or whitespace-only")
    if "\n" in text or "\r" in text:
        fail("entry must be a single line")
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in text):
        fail("entry must not contain control characters")
    if not 1 <= len(text) <= 200:
        fail(f"entry must be 1 to 200 characters, got {len(text)}")


def main():
    problem = sentence_problem(ENTRY)
    if problem is not None:
        fail(f"entry is not exactly one sentence ({problem}): {ENTRY!r}")
    if not 1 <= len(ENTRY) <= 200:
        fail(f"entry must be 1-200 characters, got {len(ENTRY)}")
    validate_entry(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    targets = {str(Path(out_dir) / "entry.txt"), "/output/entry.txt"}
    for target in sorted(targets):
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ENTRY, encoding="utf-8")
        back = path.read_text(encoding="utf-8")
        if back != ENTRY:
            fail(f"read-back mismatch for {target}")
    print(ENTRY)


if __name__ == "__main__":
    main()
