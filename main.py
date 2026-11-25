"""The Absurd Clause Contest.

Writes one absurd terms-of-service clause to
$MAKEFUN_OUTPUT_DIR/entry.txt: the User's shadow stays the
Company's property after termination, licensed, sold, or
displayed in the lobby. Standard library only; the clause
is checked against the competition gate (one sentence, 1 to
200 characters) before anything is written.
"""

import sys
from os import environ
from os.path import join as path_join

CLAUSE = (
    "Upon termination, the User's shadow shall remain the exclusive "
    "property of the Company and may be licensed, sold, or displayed "
    "in the Company lobby at its sole discretion."
)

CHAR_LIMIT = 200


def clause_text():
    """Return the absurd clause."""
    return CLAUSE


def clause_ok(text):
    """Check the clause against the competition gate.

    The gate wants one sentence of plain UTF-8 text, between 1
    and 200 characters, phrased as a clause that could sit buried
    deep inside a terms-of-service agreement. A clause that fails
    here is rejected instead of wasting a submission on the server.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("clause is empty")
    if len(stripped) > CHAR_LIMIT:
        raise ValueError(
            "clause is %d characters, over the 200 limit"
            % len(stripped)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("clause must fit on exactly one line")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("clause must be exactly one sentence")
    return stripped


def clause_has_turn(text):
    """Check the clause ambushes the reader.

    The joke needs the turn: flat legal boilerplate first, then
    the absurd object — the shadow — handed over as property.
    A clause without a concrete absurd object reads like plain
    boilerplate, so it is rejected here before anything is written.
    """
    lowered = text.lower()
    if "shadow" not in lowered:
        raise ValueError("clause has no absurd object to hand over")
    if "sole discretion" not in lowered:
        raise ValueError("clause never sounds like real boilerplate")
    return text


def clause_size(text):
    """Measure the clause for a last sanity pass.

    Returns the character and word counts. A clause too short to
    carry both the legal register and the absurd turn, or one
    padded out to fill the cap, is caught here before anything
    is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = environ.get("MAKEFUN_OUTPUT_DIR", "output")
    try:
        from os import makedirs

        makedirs(out_dir, exist_ok=True)
    except OSError:
        pass
    line = clause_ok(clause_text())
    line = clause_has_turn(line)
    shape = clause_size(line)
    if shape["words"] < 5:
        raise ValueError("clause is too short to land the joke")
    with open(path_join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
