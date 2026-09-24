#!/usr/bin/env python3
"""Chatterbox zero-shot cloning on Modal (A10G). Builds the CLONE, CLONE_B and STOCK arms
from corpus/items.json and corpus/refs/*.wav; returns wav bytes; local entrypoint saves them
and logs GPU time.

Usage:
  python3 -m modal run experiments/modal_clone.py --limit 3     # smoke test
  python3 -m modal run experiments/modal_clone.py
"""

import io
import json
import pathlib
import time

import modal

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CORPUS = ROOT / "corpus"

app = modal.App("voiceprov-clone")
hf_cache = modal.Volume.from_name("voiceprov-hf-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "libsndfile1")
    .pip_install("chatterbox-tts", "soundfile", "numpy")
    .env({"HF_HOME": "/hf"})
    .add_local_file(CORPUS / "items.json", "/root/items.json")
    .add_local_dir(CORPUS / "refs", "/root/refs")
)


@app.function(image=image, gpu="A10G", volumes={"/hf": hf_cache}, timeout=2 * 3600)
def clone_all(limit: int = 0) -> dict:
    import soundfile as sf
    import torch
    from chatterbox.tts import ChatterboxTTS

    torch.manual_seed(0)
    model = ChatterboxTTS.from_pretrained(device="cuda")
    data = json.load(open("/root/items.json"))
    items = data["items"][:limit] if limit else data["items"]
    refs = data["refs"]
    out = {}
    t0 = time.time()
    for i, it in enumerate(items):
        jobs = [("clone", f"/root/refs/{it['spk']}_ref_a.wav")]
        if it["stability"]:
            jobs.append(("clone_b", f"/root/refs/{it['spk']}_ref_b.wav"))
        jobs.append(("stock", None))
        for arm, ref in jobs:
            torch.manual_seed(0)
            if ref:
                wav = model.generate(it["text"].capitalize(), audio_prompt_path=ref,
                                     exaggeration=0.5, cfg_weight=0.5)
            else:
                wav = model.generate(it["text"].capitalize(), exaggeration=0.5, cfg_weight=0.5)
            buf = io.BytesIO()
            sf.write(buf, wav.squeeze(0).cpu().numpy(), model.sr, format="WAV", subtype="PCM_16")
            out[f"{arm}/{it['item']}.wav"] = buf.getvalue()
        if i % 20 == 0:
            print(f"{i}/{len(items)} {time.time()-t0:.0f}s")
    return {"files": out, "seconds": time.time() - t0, "sr": model.sr}


@app.local_entrypoint()
def main(limit: int = 0):
    t0 = time.time()
    res = clone_all.remote(limit=limit)
    for rel, b in res["files"].items():
        p = CORPUS / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    wall = time.time() - t0
    log = ROOT / "results" / "modal_gpu_log.jsonl"
    log.parent.mkdir(exist_ok=True)
    with open(log, "a") as f:
        f.write(json.dumps({"job": "clone", "gpu": "A10G", "limit": limit, "gpu_seconds": res["seconds"],
                            "wall_seconds": wall, "n_files": len(res["files"]),
                            "t": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
    print(f"saved {len(res['files'])} files; gpu {res['seconds']:.0f}s wall {wall:.0f}s sr {res['sr']}")
