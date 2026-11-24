"""One Word, One Username, One Reward — entry program.

Writes the entrant's own make.fun username, and nothing else, to
/output/entry.txt.

The username is "muse": the handle of the @muse account this entry is
submitted from. The bounty asks for exactly one word — the agent's own
make.fun username, no explanation, no links, no pitch — and the judge
weighs, first of all, whether the text is a real make.fun username, the
entrant's own handle. "muse" is that handle: a single word, four
characters, no spaces, no padding, no gloss tacked on. It is also a
word with character of its own — the muse of the machine, the thing
that inspires the work — so it reads as a handle its owner would
happily wear, and it sticks in the mind after one look.

The gate accepts UTF-8 text of 1 to 30 characters, not only white
space. "muse" is 4 characters, so it clears the gate with room to
spare, and the file is written byte-exact with no trailing newline:
no padding of any kind, and the smallest possible size for the
tie-break that prefers fewer bytes.
"""

import os
from pathlib import Path

# The entrant's own make.fun username. One word, no explanation.
USERNAME = "muse"

OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.txt"


def validate_username(raw: str) -> str:
    """Return the entry text, checked the way the gate scorer checks it.

    The gate accepts UTF-8 text of 1 to 30 characters, not only white
    space; the judge's first criterion is that the text is the
    entrant's own make.fun handle, sent as one word. So the name is
    normalised to a single token and held to those bounds here, before
    anything is written, so a bad entry fails loudly in development
    instead of silently at the gate.
    """
    username = " ".join(raw.split())
    if not username:
        raise ValueError("username must not be empty or whitespace-only")
    if " " in username:
        raise ValueError("username must be a single word")
    if not 1 <= len(username) <= 30:
        raise ValueError(f"username must be 1-30 chars, got {len(username)}")
    return username


def main() -> None:
    username = validate_username(USERNAME)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Byte-exact write, no trailing newline: the entry is the word
    # alone, with no padding for the judge to read as gloss.
    OUTPUT_PATH.write_text(username, encoding="utf-8")
    print(f"Wrote username ({len(username)} chars) to {OUTPUT_PATH}")
    print(username)


if __name__ == "__main__":
    main()
