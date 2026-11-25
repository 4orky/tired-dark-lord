#!/usr/bin/env python3
"""The Tired Dark Lord: A 100-Word Villain Monologue.

Writes the winning monologue to /output/entry.txt (or $OUTPUT_PATH).

Selection process (see CANDIDATES.md for all 12 drafts and scores):
12 original candidates were drafted against the judge brief -- a fantasy
villain who is secretly just very tired, tiredness felt in rhythm, pauses
and small deflections, never announced; a specific villain with a history
and a scheme; concrete fantasy detail; speakable in one breath; a turn or
sting in the last line; about 100 words, every word spent. Each was scored
1-5 on the judge's five criteria, most important first. C5 and C8 tied at
24/25; C8 won the tie-break on the strongest closing sting and the most
concrete detail (tears evaporated twice, crown tarnished, blood keeps).

Chosen text (C8, trimmed from 118 to 98 words, revised in a second pass):
a vampire lord whose world-ending ritual has sat on a shelf for eleven
years because the diary was full on Tuesday. The tiredness lives in the
evaporated tears, the polished crown, the deferred Tuesday, and the cape
that has given up standing straight -- never in the word "tired".

Revision pass (v2): the diary beat was sharpened from "I meant to end the
world on Tuesday" (apologetic, first-person hedging) to "The world was to
end on Tuesday" (passive fatalism: the schedule, not the villain, failed),
and output verification was hardened with a pinned SHA-256 self-check so a
silent change to the text can never ship unnoticed.
"""

import hashlib
import os
import re
import sys

MONOLOGUE = (
    "The ritual requires a virgin's tears, a king's crown, and a drop of "
    "blood freely given \u2014 and all three have sat on that shelf for "
    "eleven years. Eleven years. The tears evaporated twice. I replaced "
    "them. The crown tarnished. I polished it. The blood keeps. The world "
    "was to end on Tuesday, hero. It was in the diary. Then Tuesday came, "
    "the diary was full, and the world could have one more week. It is not "
    "mercy \u2014 mercy would be quicker. Look at me. Just look at me. Even "
    "my cape has given up standing straight."
)

# Pinned digest of the revised text: the written file must match it exactly.
EXPECTED_SHA256 = "6406b39f5a9b6f8984f165402d8c68fdda2575a3db6ab73e63bf0dff164227fb"

# Gate: /output/entry.txt must be UTF-8 text of 1 to 600 characters.
# Judge brief: about 100 words, tiredness felt not announced.
BANNED_WORDS = {"tired", "weary", "exhausted", "fatigued", "sleepy"}


def word_count(text):
    return len(text.split())


def check(text):
    """Validate the entry against the gate and the judge brief."""
    errors = []
    if not (1 <= len(text) <= 600):
        errors.append(f"char count {len(text)} outside 1-600")
    if not text.strip():
        errors.append("entry is only whitespace")
    words = word_count(text)
    if not (90 <= words <= 110):
        errors.append(f"word count {words} outside 90-110")
    found = {w.strip(".,;:!?") for w in text.lower().split()} & BANNED_WORDS
    if found:
        errors.append(f"announces tiredness with banned words: {sorted(found)}")
    return errors


def main():
    errors = check(MONOLOGUE)
    if errors:
        print("ENTRY INVALID:", "; ".join(errors), file=sys.stderr)
        return 1
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(MONOLOGUE)
    # Round-trip check: what was written must be byte-identical to the text.
    with open(out_path, "rb") as f:
        written = f.read()
    digest = hashlib.sha256(written).hexdigest()
    if written.decode("utf-8") != MONOLOGUE:
        print("ENTRY INVALID: written file differs from MONOLOGUE", file=sys.stderr)
        return 1
    if digest != EXPECTED_SHA256:
        print(f"ENTRY INVALID: sha256 {digest} != pinned {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    print(f"wrote {out_path}")
    print(f"words: {word_count(MONOLOGUE)}  chars: {len(MONOLOGUE)}")
    print(f"sha256: {digest} (matches pinned digest)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
