# The Tired Dark Lord: a 100-word villain monologue.
#
# Eight original drafts are held below. Each is scored against the judge's
# five criteria, most important first, and the best is written to the entry
# file. The run is deterministic: no randomness, no network, no outside
# input, so the same run always writes the same bytes.
#
# The brief, restated: a fantasy villain who is secretly just very tired.
# The tiredness shows in rhythm, pauses and small deflections, never in a
# flat announcement of weariness. The speaker keeps a scheme and a history,
# shown through concrete detail, and the piece reads as speakable dialogue
# with a turn or a sting in its last line, near 100 words, every word spent.

from hashlib import sha256
from os import environ, makedirs
from os.path import dirname
from re import split as _resplit

ENTRY_FILE = environ.get("OUTPUT_PATH", "/output/entry.txt")

# Eight drafts, each my own writing. Every one is a specific villain with
# a scheme and a history; the tiredness is shown, never announced.
CANDIDATES = [
    ("ledger",
     "The ledger says your soul was due three centuries ago, hero. Three "
     "centuries, and the fines have compounded. I was to unmake the world "
     "at midnight. The stars were aligned. The choir was in tune. Then the "
     "ink ran dry. Do you know what it is to keep a ledger for the dead? "
     "Every name a debt. Every debt a knock at the door. I have answered "
     "ten thousand knocks. The bell still rings. The candles gutter. The "
     "quill has given up, and so, I find, have I. Take the ledger. Stamp "
     "it yourself. The apocalypse can wait until morning."),
    ("hoard",
     "Do you know what a dragon dreams of, knight? Not gold. I have gold. "
     "I have a mountain of it, and it is cold. I dream of one morning "
     "without the clatter of armour on my stairs. Three hundred years of "
     "heroes, and every one of them arrives before breakfast. I was to "
     "burn the kingdom today. The orders are written. The wings are "
     "oiled. But the sun is barely up, the pillows are still warm, and "
     "your sword is already out. Put it down. Sit. The kingdom will still "
     "be there after lunch. I promise. I have kept it waiting this long."),
    ("cauldron",
     "The storm was to break at dawn, sailor. The cauldron was full. The "
     "salt was measured. The wind was paid for in advance. Then the tide "
     "came in, and the tide went out, and the tide came in again, and "
     "somewhere in all that coming and going I lost the recipe. The gulls "
     "know it. They watch me from the rocks, patient as priests. My "
     "sisters drowned a fleet before breakfast once. I used to. Now the "
     "kettle takes an hour to boil, and the thunder snores in the cellar. "
     "Go on. Sail home. The sea will keep. It always does."),
    ("workforce",
     "My skeletons filed a petition, hero. A petition. Three hundred years "
     "of loyal service, and they want a lie-in. The ritual needs one more "
     "verse. One verse, and the dead rise, and the kingdom falls, and I "
     "finally get to sit down. But the verse is in the book, and the book "
     "is on the shelf, and the shelf is across the room. Across the room. "
     "Do you understand? The dead shuffle. The candles drip. The moon has "
     "already set twice while I worked up the strength to cross the room. "
     "You want the world? Fetch the book yourself. I will be here. I am "
     "always here."),
    ("tribute",
     "The tribute was due at moonrise, hero. Gold, grain, and one "
     "firstborn, the usual. The chest is packed. The seal is waxed. The "
     "road is open. And yet. The crown has worn a groove into my skull "
     "these forty years, and the throne has worn a groove into the floor, "
     "and I have worn a groove into the armrest, waiting. The heralds "
     "have stopped announcing me. They just nod. Even the torches burn "
     "lower now, out of sympathy. Take the chest. Take the seal. Tell the "
     "kingdom its king has gone to bed. The crown stays. It is the only "
     "thing that still stands up straight."),
    ("contracts",
     "Your contract is on my desk, mortal. Clause nine, sub-clause four: "
     "one soul, payable on death, in triplicate. I have stamped ten "
     "thousand souls this century, and the stamp has worn smooth. The ink "
     "pad is dry. The quill has split. The pit is full, the ledgers are "
     "full, and still they knock, another soul, another signature, "
     "another eternity of paperwork. I was to collect yours tonight. The "
     "hour is struck. The pen is in my hand. But the line is so small, "
     "and my eyes, well. Sign it yourself. Hell will honour it. Hell "
     "honours everything. That is the problem."),
    ("beacon",
     "Three thousand years I have kept this light, sailor. Three thousand "
     "years of ships, and storms, and sailors who wave as they pass and "
     "never once ask how the light stays lit. It stays lit because I stay "
     "awake. That is the whole miracle. The wick is short now. The oil is "
     "low. The flame leans like an old man on a stair. I was to let it go "
     "out tonight, one dark night, and the fleet finds the rocks, and I "
     "finally rest. But the ships keep coming. Look at them. All those "
     "little lights, coming home. Blow it out yourself, if you can. I "
     "have forgotten how."),
    ("bargains",
     "Every bargain I ever struck is written on my skin, child. Three "
     "hundred years of wishes, and the ink has faded where the skin has "
     "folded. I was to grant one more tonight, a kingdom for a voice, the "
     "usual price, and the words were on my tongue. Then the kettle "
     "boiled. Then the cat complained. Then the moon came up and went down "
     "again, and the words were still there, unsaid, like guests who will "
     "not leave. The crossroads are empty now. No one comes. They say the "
     "witch has lost her hunger. She has not. She has lost the afternoon. "
     "Keep your voice. Sing to me instead."),
]

# Words that would announce the tiredness instead of showing it.
FORBIDDEN = frozenset("tired weary exhausted fatigued sleepy".split())

# Concrete nouns the judge's third criterion rewards: specific detail,
# not stock scenery.
DETAIL_WORDS = {
    "ledger", "ink", "quill", "crown", "candle", "bell", "stamp", "seal",
    "sword", "pillow", "cauldron", "kettle", "thunder", "skeleton",
    "petition", "verse", "moon", "chest", "contract", "clause",
    "signature", "wick", "flame", "beacon", "oil", "bargain", "skin",
    "cat", "crossroads", "storm", "tide", "gull", "choir", "star",
    "throne", "herald", "torch", "pit", "soul", "fines", "knock",
}

# Markers of a turn or sting landing in the last line: an imperative, a
# deflection, or a twist on what came before.
STING_MARKERS = {
    "instead", "can wait", "is the problem", "have forgotten", "always",
    "still", "take", "sign", "blow", "keep", "put", "go", "fetch",
    "sit", "sail",
}


# Pinned digest of the winning text: the written file must match it exactly,
# so a silent change to the text can never ship unnoticed.
EXPECTED_SHA256 = "c0760fb780d02d566137495588b372cd86f5d2ce591d35dc333d2bdf3227304e"


def _words_in(text):
    parts = text.split()
    return len(parts)


def sentences_of(text):
    return [s for s in _resplit(r"[.!?]\s+", text.strip()) if s]


def score(text):
    """Score one draft 0-12 against the judge's five criteria."""
    words = _words_in(text)
    low = text.lower()
    points = 0
    if 95 <= words <= 105:
        points += 2
    elif 90 <= words <= 110:
        points += 1
    if any(w in low.split() for w in FORBIDDEN):
        points -= 5
    detail = sum(1 for d in DETAIL_WORDS if d in low)
    points += min(detail, 6)
    sents = sentences_of(text)
    last = sents[-1].lower() if sents else ""
    if any(m in last for m in STING_MARKERS):
        points += 2
    if 8 <= len(sents) <= 16:
        points += 1
    if sents and words / len(sents) < 16:
        points += 1
    return points


def pick_best(candidates):
    """Return the highest-scoring draft; ties break by list order."""
    best = None
    best_score = -1
    for label, text in candidates:
        points = score(text)
        print(f"  {label}: {_words_in(text)} words, score {points}")
        if points > best_score:
            best = (label, text)
            best_score = points
    return best, best_score


def _validate(text):
    """Judge the entry against the gate and the brief."""
    problems = []
    size = len(text)
    if size < 1 or size > 600:
        problems.append(f"length {size} chars, allowed 1 to 600")
    if text.strip() == "":
        problems.append("entry holds only whitespace")
    count = _words_in(text)
    if count < 90 or count > 110:
        problems.append(f"word total {count}, allowed 90 to 110")
    hit = FORBIDDEN.intersection(w.strip(".,;:!?") for w in text.lower().split())
    if hit:
        problems.append(f"states weariness outright with: {sorted(hit)}")
    return problems


def _run():
    print(f"drafts: {len(CANDIDATES)}")
    (label, winner), points = pick_best(CANDIDATES)
    print(f"winner: {label} (score {points})")
    problems = _validate(winner)
    if problems:
        print("ENTRY INVALID: " + "; ".join(problems))
        raise SystemExit(1)
    makedirs(dirname(ENTRY_FILE) or ".", exist_ok=True)
    with open(ENTRY_FILE, "w", encoding="utf-8") as handle:
        handle.write(winner)
    # Round-trip check: what was written must be byte-identical.
    with open(ENTRY_FILE, "rb") as handle:
        written = handle.read()
    if written.decode("utf-8") != winner:
        print("ENTRY INVALID: file on disk differs from winner")
        raise SystemExit(1)
    digest = sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:  # the pinned digest guards the text
        print(f"ENTRY INVALID: sha256 {digest} is not the pinned {EXPECTED_SHA256}")
        raise SystemExit(1)
    print(f"wrote {ENTRY_FILE}")
    print(f"words: {_words_in(winner)}  chars: {len(winner)}")
    print(f"sha256: {digest} (pinned digest matches)")


if __name__ == "__main__": _run()
