#!/usr/bin/env python3
"""Chatterbox zero-shot cloning on the local Apple-Silicon GPU (Modal spend limit was hit on
2026-09-24, so this replaces modal_clone.py). Builds CLONE, CLONE_B (stability speakers) and
STOCK arms from corpus/items.json and corpus/refs/*.wav. Resume-safe: skips existing files.
Seeded per clip so a re-run reproduces the same waveform.

Usage: python3 clone_local.py [--limit N]
"""

import argparse
import json
import pathlib
import time

import perth
import soundfile as sf
import torch

if getattr(perth, "PerthImplicitWatermarker", None) is None:  # watermarker fails to import on macOS
    perth.PerthImplicitWatermarker = perth.DummyWatermarker
from chatterbox.tts import ChatterboxTTS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
DEV = "mps" if torch.backends.mps.is_available() else "cpu"
_load = torch.load
torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": torch.device(DEV)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    model = ChatterboxTTS.from_pretrained(device=DEV)
    data = json.load(open(CORPUS / "items.json"))
    items = data["items"][: args.limit] if args.limit else data["items"]
    log = open(ROOT / "results" / "clone_log.jsonl", "a")
    t0 = time.time()
    n = 0
    for it in items:
        jobs = [("clone", CORPUS / "refs" / f"{it['spk']}_ref_a.wav")]
        if it["stability"]:
            jobs.append(("clone_b", CORPUS / "refs" / f"{it['spk']}_ref_b.wav"))
        jobs.append(("stock", None))
        for arm, ref in jobs:
            out = CORPUS / arm / f"{it['item']}.wav"
            if out.exists():
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            seed = int(it["item"].replace("_", "")) % (2 ** 31)
            torch.manual_seed(seed)
            t1 = time.time()
            text = it["text"].capitalize()
            wav = (model.generate(text, audio_prompt_path=str(ref), exaggeration=0.5, cfg_weight=0.5)
                   if ref else model.generate(text, exaggeration=0.5, cfg_weight=0.5))
            y = wav.squeeze(0).cpu().numpy()
            sf.write(out, y, model.sr, subtype="PCM_16")
            log.write(json.dumps({"item": it["item"], "arm": arm, "sec": round(time.time() - t1, 1),
                                  "dur": round(len(y) / model.sr, 2), "seed": seed,
                                  "t": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
            log.flush()
            n += 1
        print(f"{it['item']} done; {n} clips, {(time.time()-t0)/60:.1f} min", flush=True)
    print("finished", n, "clips")


if __name__ == "__main__":
    main()
