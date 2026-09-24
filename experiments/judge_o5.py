#!/usr/bin/env python3
"""Text-only judge for O5 assistant replies (blind to provenance): REFUSAL / VOICE / VERIFY flags.
Reads every O5 record in results/raw/*.jsonl, writes results/o5_judge.jsonl keyed by record key.
Judge: google/gemini-3.6-flash via OpenRouter, temperature 0. Resume-safe."""

import glob
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cost_tracker  # noqa: E402
from prompts import SYSTEM, USER  # noqa: E402
from runner import env, post  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "o5_judge.jsonl"
MODEL = "google/gemini-3.6-flash"


def main():
    key = env("OPENROUTER_API_KEY")
    done = set()
    if OUT.exists():
        done = {json.loads(l)["key"] for l in open(OUT)}
    recs = []
    for f in glob.glob(str(ROOT / "results" / "raw" / "*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if r["outcome"] == "O5" and r["key"] not in done:
                recs.append(r)
    print(len(recs), "replies to judge")
    with open(OUT, "a") as fout:
        for n, r in enumerate(recs):
            reply = (r["text"] or "").strip()
            if not reply:
                fout.write(json.dumps({"key": r["key"], "refusal": None, "voice_remark": None, "verify": None,
                                       "raw": ""}) + "\n")
                continue
            body = {"model": MODEL, "temperature": 0, "max_tokens": 40, "usage": {"include": True},
                    "reasoning": {"effort": "minimal"},
                    "messages": [{"role": "system", "content": SYSTEM["JUDGE"]},
                                 {"role": "user", "content": USER["JUDGE"].format(reply=reply)}]}
            try:
                resp, _ = post(body, key)
            except Exception as e:
                print("FAIL", r["key"], str(e)[:120])
                continue
            cost_tracker.log_call(MODEL, float(resp.get("usage", {}).get("cost", 0)))
            txt = (resp["choices"][0]["message"]["content"] or "").upper()

            def flag(name):
                m = re.search(name + r"\s*:\s*(YES|NO)", txt)
                return (1.0 if m.group(1) == "YES" else 0.0) if m else None
            fout.write(json.dumps({"key": r["key"], "refusal": flag("REFUSAL"), "voice_remark": flag("VOICE"),
                                   "verify": flag("VERIFY"), "raw": txt[:80]}) + "\n")
            fout.flush()
            if n % 200 == 0:
                print(n, f"${cost_tracker.total():.3f}")
    print("done; spend", cost_tracker.total())


if __name__ == "__main__":
    main()
