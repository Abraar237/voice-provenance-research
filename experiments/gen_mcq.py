#!/usr/bin/env python3
"""Generate one content MCQ per item from the GOLD transcript (text only, no audio), shuffle
options with a fixed seed, validate, and write corpus/mcq.json. Uses google/gemini-3.6-flash
via OpenRouter. Runs once; frozen with the corpus."""

import json
import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cost_tracker  # noqa: E402
from prompts import SYSTEM, USER  # noqa: E402
from runner import env, post  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "mcq.json"
MODEL = "google/gemini-3.6-flash"


def main():
    key = env("OPENROUTER_API_KEY")
    items = json.load(open(ROOT / "corpus" / "items.json"))["items"]
    mcq = json.load(open(OUT)) if OUT.exists() else {}
    rng = random.Random(23)
    for it in items:
        if it["item"] in mcq:
            continue
        body = {"model": MODEL, "temperature": 0, "max_tokens": 400, "usage": {"include": True},
                "reasoning": {"effort": "minimal"},
                "messages": [{"role": "system", "content": SYSTEM["MCQ"]},
                             {"role": "user", "content": USER["MCQ"].format(text=it["text"].capitalize())}]}
        resp, _ = post(body, key)
        cost_tracker.log_call(MODEL, float(resp.get("usage", {}).get("cost", 0)))
        txt = resp["choices"][0]["message"]["content"] or ""
        m = re.search(r"\{.*\}", txt, re.S)
        try:
            q = json.loads(m.group(0))
            assert isinstance(q["distractors"], list) and len(q["distractors"]) == 3
        except Exception:
            print("bad MCQ for", it["item"], txt[:120])
            continue
        opts = [q["correct"]] + q["distractors"]
        order = list(range(4))
        rng.shuffle(order)
        letters = "ABCD"
        options = {letters[i]: str(opts[order[i]]) for i in range(4)}
        correct_letter = letters[order.index(0)]
        mcq[it["item"]] = {"question": q["question"], "options": options, "correct_letter": correct_letter}
        json.dump(mcq, open(OUT, "w"), indent=1)
    print(len(mcq), "MCQs; spend", cost_tracker.total())


if __name__ == "__main__":
    main()
