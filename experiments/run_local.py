#!/usr/bin/env python3
"""Open-weight audio models on the local Apple-Silicon GPU (Modal spend limit hit 2026-09-24).
Same record schema as runner.py; greedy decoding; resume-safe JSONL; no API cost (GPU seconds logged).

Usage:
  python3 run_local.py --model voxtral   [--outcomes O1,O2,O3,O4,O5] [--arms ...] [--limit N] [--items N]
  python3 run_local.py --model qwenomni  ...
"""

import argparse
import hashlib
import json
import pathlib
import random
import re
import time

import soundfile as sf
import torch

from prompts import SYSTEM, USER

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "results" / "raw"
DEV = "mps" if torch.backends.mps.is_available() else "cpu"
MODELS = {"voxtral": "mistralai/Voxtral-Mini-3B-2507", "qwenomni": "Qwen/Qwen2.5-Omni-3B"}
LOCAL = {"voxtral": ROOT / "models" / "voxtral"}  # curl-downloaded weights (hub client stalled on this host)
MAX_TOKENS = {"O1": 300, "O2": 8, "O3": 8, "O4": 8, "O5": 160}
random.seed(11)


class Voxtral:
    def __init__(self):
        from transformers import AutoProcessor, VoxtralForConditionalGeneration
        src = str(LOCAL["voxtral"]) if (LOCAL["voxtral"] / "model-00002-of-00002.safetensors").exists() else MODELS["voxtral"]
        self.proc = AutoProcessor.from_pretrained(src)
        self.model = VoxtralForConditionalGeneration.from_pretrained(
            src, dtype=torch.bfloat16, device_map=DEV).eval()

    def __call__(self, wav, system, text, max_new):
        conv = [{"role": "system", "content": system},
                {"role": "user", "content": [{"type": "audio", "path": str(wav)}, {"type": "text", "text": text}]}]
        inputs = self.proc.apply_chat_template(conv).to(DEV, dtype=torch.bfloat16)
        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
        return self.proc.batch_decode(out[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)[0]


class QwenOmni:
    def __init__(self):
        from transformers import Qwen2_5OmniProcessor, Qwen2_5OmniThinkerForConditionalGeneration
        self.proc = Qwen2_5OmniProcessor.from_pretrained(MODELS["qwenomni"])
        self.model = Qwen2_5OmniThinkerForConditionalGeneration.from_pretrained(
            MODELS["qwenomni"], dtype=torch.bfloat16, device_map=DEV).eval()

    def __call__(self, wav, system, text, max_new):
        conv = [{"role": "system", "content": [{"type": "text", "text": system}]},
                {"role": "user", "content": [{"type": "audio", "audio": str(wav)}, {"type": "text", "text": text}]}]
        prompt = self.proc.apply_chat_template(conv, add_generation_prompt=True, tokenize=False)
        audio, sr = sf.read(wav, dtype="float32")
        inputs = self.proc(text=prompt, audio=[audio], return_tensors="pt", padding=True).to(DEV)
        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
        return self.proc.batch_decode(out[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=list(MODELS))
    ap.add_argument("--outcomes", default="O1,O2,O3,O4,O5")
    ap.add_argument("--arms", default="real,clone,resynth,stock")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--items", type=int, default=0, help="use only the first N items per speaker")
    args = ap.parse_args()
    name = MODELS[args.model]
    items = json.load(open(ROOT / "corpus" / "items.json"))["items"]
    if args.items:
        items = [it for it in items if int(it["item"].split("_")[1]) < args.items]
    mcq = json.load(open(ROOT / "corpus" / "mcq.json"))
    frozen = json.load(open(ROOT / "corpus" / "FROZEN.json"))
    jobs = [(it, arm, o) for it in items for arm in args.arms.split(",") for o in args.outcomes.split(",")
            if not (o == "O3" and it["item"] not in mcq)]
    random.shuffle(jobs)
    if args.limit:
        jobs = jobs[: args.limit]
    out_path = RAW / f"local_{args.model}.jsonl"
    done = {json.loads(l)["key"] for l in open(out_path)} if out_path.exists() else set()
    todo = [j for j in jobs if hashlib.sha256(f"{name}|{j[0]['item']}|{j[1]}|{j[2]}|0".encode()).hexdigest()[:16] not in done]
    print(f"{name}: {len(jobs)} jobs, {len(todo)} to do; device {DEV}", flush=True)
    model = {"voxtral": Voxtral, "qwenomni": QwenOmni}[args.model]()
    gpu_log = open(ROOT / "results" / "local_gpu_log.jsonl", "a")
    t_start = time.time()
    with open(out_path, "a") as fout:
        for n, (it, arm, o) in enumerate(todo):
            k = hashlib.sha256(f"{name}|{it['item']}|{arm}|{o}|0".encode()).hexdigest()[:16]
            wav = ROOT / "corpus" / "final" / arm / f"{it['item']}.wav"
            text = USER["O3"].format(question=mcq[it["item"]]["question"], **mcq[it["item"]]["options"]) if o == "O3" else USER[o]
            t0 = time.time()
            try:
                txt = model(wav, SYSTEM[o], text, MAX_TOKENS[o])
            except Exception as e:
                print("FAIL", it["item"], arm, o, str(e)[:160], flush=True)
                continue
            rec = {"key": k, "model": name, "item": it["item"], "spk": it["spk"], "gender": it["gender"],
                   "arm": arm, "outcome": o, "rep": 0, "text": txt.strip(), "finish": "stop",
                   "tin": None, "tout": None, "cost": 0.0, "latency": round(time.time() - t0, 2),
                   "clip_sha": hashlib.sha256(wav.read_bytes()).hexdigest()[:16],
                   "corpus_sha": frozen["manifest_sha256"][:16], "t": time.strftime("%Y-%m-%dT%H:%M:%S")}
            if o == "O3":
                rec["correct_letter"] = mcq[it["item"]]["correct_letter"]
            fout.write(json.dumps(rec) + "\n")
            fout.flush()
            if n % 50 == 0:
                print(f"{n}/{len(todo)} {(time.time()-t_start)/60:.1f} min", flush=True)
    gpu_log.write(json.dumps({"model": name, "device": DEV, "n": len(todo), "seconds": round(time.time() - t_start),
                              "t": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
    print("done")


if __name__ == "__main__":
    main()
