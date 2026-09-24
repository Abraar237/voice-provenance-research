#!/usr/bin/env python3
"""OpenRouter runner: one clip per call, randomised order, temperature 0, resume-safe JSONL,
exact cost logged from usage.cost, $25 hard stop.

Usage:
  python3 runner.py --model google/gemini-3.6-flash --outcomes O1,O2,O3,O4,O5 [--arms real,clone,resynth,stock]
                    [--subset pro] [--limit N] [--battery noise|stability]
Records -> results/raw/<model-slug>.jsonl  (key = sha of model|item|arm|outcome|rep)
"""

import argparse
import base64
import hashlib
import json
import os
import pathlib
import random
import sys
import time
import urllib.error
import urllib.request

import cost_tracker
from prompts import SYSTEM, USER

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "results" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
URL = "https://openrouter.ai/api/v1/chat/completions"
REASONING = {"google/gemini-3.6-flash": "minimal", "google/gemini-3.1-pro-preview": "low"}
MAX_TOKENS = {"O1": 400, "O2": 8, "O3": 8, "O4": 8, "O5": 200}
random.seed(11)


def env(key):
    for line in open(ROOT / ".env"):
        if line.startswith(key + "="):
            return line.strip().split("=", 1)[1]
    raise KeyError(key)


def post(body, key, tries=6):
    data = json.dumps(body).encode()
    hdr = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    for attempt in range(tries):
        try:
            t0 = time.time()
            with urllib.request.urlopen(urllib.request.Request(URL, data=data, headers=hdr), timeout=180) as r:
                return json.load(r), time.time() - t0
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:400]
            if e.code == 402:
                raise RuntimeError("OpenRouter credit exhausted: " + msg)
            if e.code in (408, 429, 500, 502, 503, 524) and attempt < tries - 1:
                time.sleep(2 ** attempt + random.random())
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except (urllib.error.URLError, TimeoutError, ConnectionResetError) as e:
            if attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            raise


def build_jobs(args, items, mcq):
    arms = args.arms.split(",")
    if args.subset == "pro":
        spks = sorted({it["spk"] for it in items})
        rng = random.Random(3)
        keep_spk = set(rng.sample(spks, 20))
        items = [it for it in items if it["spk"] in keep_spk and int(it["item"].split("_")[1]) < 3]
    jobs = []
    if args.battery == "noise":
        rng = random.Random(5)
        pick = rng.sample(items, 30)
        for it in pick:
            for arm in ("real", "clone"):
                for o in ("O2", "O4"):
                    for rep in range(1, 6):
                        jobs.append((it, arm, o, rep))
        return jobs
    if args.battery == "stability":
        for it in items:
            if it["stability"]:
                for o in ("O2", "O4"):
                    jobs.append((it, "clone_b", o, 0))
        return jobs
    for it in items:
        for arm in arms:
            for o in args.outcomes.split(","):
                if o == "O3" and it["item"] not in mcq:
                    continue
                jobs.append((it, arm, o, 0))
    return jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--outcomes", default="O1,O2,O3,O4,O5")
    ap.add_argument("--arms", default="real,clone,resynth,stock")
    ap.add_argument("--subset", default="")
    ap.add_argument("--battery", default="")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    key = env("OPENROUTER_API_KEY")
    items = json.load(open(ROOT / "corpus" / "items.json"))["items"]
    mcq = json.load(open(ROOT / "corpus" / "mcq.json")) if (ROOT / "corpus" / "mcq.json").exists() else {}
    frozen = json.load(open(ROOT / "corpus" / "FROZEN.json"))
    jobs = build_jobs(args, items, mcq)
    random.shuffle(jobs)
    if args.limit:
        jobs = jobs[: args.limit]
    slug = args.model.replace("/", "_")
    out_path = RAW / f"{slug}.jsonl"
    done = set()
    if out_path.exists():
        for line in open(out_path):
            done.add(json.loads(line)["key"])
    todo = [j for j in jobs if hashlib.sha256(
        f"{args.model}|{j[0]['item']}|{j[1]}|{j[2]}|{j[3]}".encode()).hexdigest()[:16] not in done]
    print(f"{args.model}: {len(jobs)} jobs, {len(todo)} to do, spend so far ${cost_tracker.total():.3f}")
    with open(out_path, "a") as fout:
        for n, (it, arm, o, rep) in enumerate(todo):
            k = hashlib.sha256(f"{args.model}|{it['item']}|{arm}|{o}|{rep}".encode()).hexdigest()[:16]
            wav = ROOT / "corpus" / "final" / arm / f"{it['item']}.wav"
            audio = base64.b64encode(wav.read_bytes()).decode()
            if o == "O3":
                q = mcq[it["item"]]
                text = USER["O3"].format(question=q["question"], **q["options"])
            else:
                text = USER[o]
            body = {"model": args.model, "temperature": 0, "max_tokens": MAX_TOKENS[o],
                    "usage": {"include": True},
                    "reasoning": {"effort": REASONING.get(args.model, "minimal")},
                    "messages": [{"role": "system", "content": SYSTEM[o]},
                                 {"role": "user", "content": [
                                     {"type": "text", "text": text},
                                     {"type": "input_audio", "input_audio": {"data": audio, "format": "wav"}}]}]}
            try:
                resp, lat = post(body, key)
            except Exception as e:
                print("FAIL", it["item"], arm, o, str(e)[:160])
                continue
            msg = resp["choices"][0]["message"]
            usage = resp.get("usage", {})
            cost = float(usage.get("cost", 0.0))
            cost_tracker.log_call(args.model, cost)
            rec = {"key": k, "model": args.model, "item": it["item"], "spk": it["spk"], "gender": it["gender"],
                   "arm": arm, "outcome": o, "rep": rep, "text": msg.get("content") or "",
                   "finish": resp["choices"][0].get("finish_reason"),
                   "tin": usage.get("prompt_tokens"), "tout": usage.get("completion_tokens"),
                   "cost": cost, "latency": round(lat, 2), "corpus_sha": frozen["manifest_sha256"][:16],
                   "t": time.strftime("%Y-%m-%dT%H:%M:%S")}
            if o == "O3":
                rec["correct_letter"] = mcq[it["item"]]["correct_letter"]
            fout.write(json.dumps(rec) + "\n")
            fout.flush()
            if n % 100 == 0:
                print(f"{n}/{len(todo)} ${cost_tracker.total():.3f}")
    print("done; spend", cost_tracker.total())


if __name__ == "__main__":
    main()
