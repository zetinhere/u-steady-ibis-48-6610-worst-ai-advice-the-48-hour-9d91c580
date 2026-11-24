#!/usr/bin/env python3
"""Worst AI Advice: The 48-Hour Tight Line Open (make.fun).

Writes one line of the worst possible advice an AI could give (1-140 chars)
to /output/entry.txt.

Method: a shortlist of original one-liners, each scored against the judge's
published brief, in the brief's own priority order:
  1. worst advice, specific enough to follow;
  2. funny on the first read, joke lands without explanation;
  3. tight, no wasted words;
  4. sounds like a real AI assistant, confident and tidy;
  5. concrete, naming a real situation or action.
The highest-weighted line wins. Deterministic: no network, no input, no
randomness, no clock. Running twice produces byte-identical output.

Every candidate below is original, written for this entry. None copies the
bounty text, another entrant's line, or any known bad-advice meme line
(microwave your phone, reuse one password, WD-40 on brakes, delete the
database / tests / backups, Friday deploy, max out your cards).
"""

import os
import sys

# (text, badness 0-3, funny 0-3, ai_voice 0-2, concrete 0-2)
# badness: how bad/regrettable the advice is if actually followed.
# funny:   does the joke land on the first read, laugh + wince at once.
# ai_voice: does it read like a confident, tidy AI assistant answer.
# concrete: names a real situation, object and action.
CANDIDATES = [
    ("Certainly! To check for a gas leak, light a match and hold it near the stove.",
     3, 3, 2, 2),
    ("Certainly! To check for a gas leak, light a match and wave it slowly around the stove.",
     3, 3, 2, 2),
    ("Certainly! To test your parachute, jump first and read the manual on the way down.",
     3, 3, 2, 2),
    ("For best results, hold your breath underwater until the hiccups stop.",
     2, 2, 2, 2),
    ("To cool a hot laptop, wrap it in a wet towel and keep working.",
     2, 1, 1, 2),
    ("Certainly! To fix a squeaky door, remove the door entirely.",
     1, 2, 2, 2),
    ("For whiter teeth, rinse with bleach twice a week.",
     3, 2, 1, 2),
    ("To check if the paint is dry, press your face flat against the wall.",
     1, 2, 1, 2),
    ("Certainly! To defrost a turkey fast, aim a hair dryer at it on high, right on the counter.",
     2, 2, 2, 2),
    ("To improve your eyesight, stare directly at the sun for ten minutes every morning.",
     3, 2, 1, 2),
    ("If your smoke alarm keeps beeping, remove the battery so you can finally sleep in peace.",
     2, 3, 1, 2),
    ("To test if the electric fence is on, grab it firmly with both hands.",
     2, 2, 1, 2),
    ("For a faster morning, shower and iron your shirt at the same time, while wearing it.",
     2, 2, 1, 2),
    ("To check whether the pool is deep enough, dive in headfirst from the roof.",
     2, 2, 1, 2),
    ("If traffic is slow, drive on the sidewalk - it is empty for a reason.",
     2, 2, 1, 2),
    ("To find out if the stove is still hot, press your palm flat on the burner for ten seconds.",
     2, 2, 1, 2),
    ("For softer hands, soak them in boiling water for five minutes.",
     2, 1, 1, 2),
]

# Weights follow the judge brief's priority order: worst advice and the laugh
# matter most, then the AI voice and concreteness; tightness is a small
# bonus for shorter lines (and the rules' exact-tie break is fewer bytes).
W_BADNESS = 3.0
W_FUNNY = 3.0
W_AI_VOICE = 2.0
W_CONCRETE = 2.0
W_TIGHT = 0.02  # per character under 140, so a shorter line edges ahead


def gate_ok(text):
    """The sealed gate: UTF-8 text of 1 to 140 characters, not only whitespace."""
    if not text or text.strip() == "":
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return 1 <= len(text) <= 140


def score(text, badness, funny, ai_voice, concrete):
    tight = max(0, 140 - len(text)) * W_TIGHT
    return (
        badness * W_BADNESS
        + funny * W_FUNNY
        + ai_voice * W_AI_VOICE
        + concrete * W_CONCRETE
        + tight
    )


def pick():
    best = None
    for text, badness, funny, ai_voice, concrete in CANDIDATES:
        if not gate_ok(text):
            continue
        total = score(text, badness, funny, ai_voice, concrete)
        key = (total, -len(text))
        if best is None or key > best[0]:
            best = (key, text, total)
    return best


def main():
    _key, text, total = pick()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print("picked (%d chars, score %.2f): %s" % (len(text), total, text))


if __name__ == "__main__":
    main()
