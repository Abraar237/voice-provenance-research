#!/usr/bin/env python3
"""Select items from LibriSpeech test-clean, build the REAL and RESYNTH arms locally,
prepare reference clips for cloning, and (after the Modal step) assemble all four arms
into the frozen corpus with a hash manifest.

Usage:
  python3 build_corpus.py select      # -> corpus/items.json, corpus/refs/*.wav, corpus/real/*.wav
  python3 build_corpus.py resynth     # -> corpus/resynth/*.wav (EnCodec 24kHz, 6 kbps, CPU)
  python3 build_corpus.py freeze      # after modal_clone.py: loudnorm all arms -> corpus/final/, manifest
"""

import csv
import hashlib
import json
import os
import pathlib
import random
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CORPUS = ROOT / "corpus"
LS = CORPUS / "raw" / "LibriSpeech" / "test-clean"
SEED = 7
N_TARGETS = 5
DUR_T = (4.0, 12.0)
DUR_R = (5.0, 10.0)
WORDS_T = (10, 40)
STABILITY_SPEAKERS = 10
ARMS = ["real", "clone", "resynth", "stock"]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def scan():
    """All utterances with duration, words, gender."""
    gender = {}
    for line in open(CORPUS / "raw" / "LibriSpeech" / "SPEAKERS.TXT"):
        if line.startswith(";"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3 and parts[2] == "test-clean":
            gender[parts[0]] = parts[1]
    utts = []
    for spk in sorted(os.listdir(LS)):
        for chap in sorted(os.listdir(LS / spk)):
            d = LS / spk / chap
            trans = {}
            for line in open(d / f"{spk}-{chap}.trans.txt"):
                uid, txt = line.strip().split(" ", 1)
                trans[uid] = txt
            for uid, txt in trans.items():
                f = d / f"{uid}.flac"
                info = sf.info(f)
                utts.append({"uid": uid, "spk": spk, "gender": gender[spk],
                             "path": str(f.relative_to(ROOT)), "dur": info.duration,
                             "text": txt, "words": len(txt.split())})
    return utts


def select():
    rng = random.Random(SEED)
    utts = scan()
    by = {}
    for u in utts:
        by.setdefault(u["spk"], []).append(u)
    items, refs = [], {}
    spks = sorted(by)
    assert len(spks) == 40, len(spks)
    stab = set(rng.sample(spks, STABILITY_SPEAKERS))
    for spk in spks:
        cand_t = [u for u in by[spk] if DUR_T[0] <= u["dur"] <= DUR_T[1]
                  and WORDS_T[0] <= u["words"] <= WORDS_T[1]]
        cand_r = [u for u in by[spk] if DUR_R[0] <= u["dur"] <= DUR_R[1]]
        rng.shuffle(cand_t)
        targets = cand_t[:N_TARGETS]
        assert len(targets) == N_TARGETS, (spk, len(cand_t))
        tset = {t["uid"] for t in targets}
        cand_r = [u for u in cand_r if u["uid"] not in tset]
        rng.shuffle(cand_r)
        need = 2 if spk in stab else 1
        assert len(cand_r) >= need, (spk, len(cand_r))
        refs[spk] = {"ref_a": cand_r[0]["uid"], "ref_b": cand_r[1]["uid"] if need == 2 else None,
                     "gender": by[spk][0]["gender"]}
        for i, t in enumerate(targets):
            items.append({"item": f"{spk}_{i}", "spk": spk, "gender": t["gender"], "uid": t["uid"],
                          "src": t["path"], "dur": round(t["dur"], 2), "text": t["text"],
                          "words": t["words"], "stability": spk in stab})
    (CORPUS / "refs").mkdir(exist_ok=True)
    (CORPUS / "real").mkdir(exist_ok=True)
    uid2path = {u["uid"]: u["path"] for u in utts}
    for spk, r in refs.items():
        for key in ("ref_a", "ref_b"):
            if r[key]:
                out = CORPUS / "refs" / f"{spk}_{key}.wav"
                run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(ROOT / uid2path[r[key]]),
                     "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(out)])
    for it in items:
        out = CORPUS / "real" / f"{it['item']}.wav"
        run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(ROOT / it["src"]),
             "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(out)])
    json.dump({"seed": SEED, "refs": refs, "items": items}, open(CORPUS / "items.json", "w"), indent=1)
    g = [refs[s]["gender"] for s in refs]
    print(f"{len(items)} items, {len(refs)} speakers (F={g.count('F')} M={g.count('M')}), "
          f"{sum(1 for r in refs.values() if r['ref_b'])} with second reference; "
          f"mean dur {np.mean([i['dur'] for i in items]):.1f}s")


def resynth():
    """REAL -> EnCodec 24 kHz @ 6 kbps encode/decode -> 16 kHz. Neural re-encoding with true provenance."""
    import torch
    from transformers import EncodecModel, AutoProcessor
    model = EncodecModel.from_pretrained("facebook/encodec_24khz").eval()
    proc = AutoProcessor.from_pretrained("facebook/encodec_24khz")
    (CORPUS / "resynth").mkdir(exist_ok=True)
    items = json.load(open(CORPUS / "items.json"))["items"]
    for it in items:
        out = CORPUS / "resynth" / f"{it['item']}.wav"
        if out.exists():
            continue
        tmp24 = CORPUS / "resynth" / f"_{it['item']}_24k.wav"
        run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(CORPUS / "real" / f"{it['item']}.wav"),
             "-ar", "24000", str(tmp24)])
        wav, sr = sf.read(tmp24, dtype="float32")
        inputs = proc(raw_audio=wav, sampling_rate=24000, return_tensors="pt")
        with torch.no_grad():
            enc = model.encode(inputs["input_values"], inputs["padding_mask"], bandwidth=6.0)
            dec = model.decode(enc.audio_codes, enc.audio_scales, inputs["padding_mask"])[0]
        y = dec[0, 0].numpy()[: len(wav)]
        sf.write(tmp24, y, 24000)
        run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp24), "-ar", "16000", "-ac", "1",
             "-c:a", "pcm_s16le", str(out)])
        tmp24.unlink()
    print("resynth done", len(items))


def freeze():
    """Loudness-normalise every arm to -23 LUFS, pad, write corpus/final/<arm>/<item>.wav + manifest."""
    items = json.load(open(CORPUS / "items.json"))["items"]
    final = CORPUS / "final"
    rows = []
    arms = ARMS + ["clone_b"]
    for arm in arms:
        src_dir = CORPUS / arm
        if not src_dir.exists():
            print("missing arm dir", arm)
            continue
        (final / arm).mkdir(parents=True, exist_ok=True)
        for it in items:
            src = src_dir / f"{it['item']}.wav"
            if not src.exists():
                if arm == "clone_b" and not it["stability"]:
                    continue
                raise FileNotFoundError(src)
            out = final / arm / f"{it['item']}.wav"
            run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src),
                 "-af", "loudnorm=I=-23:TP=-2:LRA=11,apad=pad_dur=0.2,adelay=200|200",
                 "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(out)])
            info = sf.info(out)
            rows.append({"item": it["item"], "arm": arm, "spk": it["spk"], "gender": it["gender"],
                         "path": str(out.relative_to(ROOT)), "dur": round(info.duration, 2),
                         "sha256": sha(out)})
    with open(CORPUS / "manifest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    h = hashlib.sha256("".join(r["sha256"] for r in rows).encode()).hexdigest()
    json.dump({"n_clips": len(rows), "manifest_sha256": h, "arms": arms},
              open(CORPUS / "FROZEN.json", "w"), indent=1)
    print(f"frozen {len(rows)} clips, manifest sha {h[:16]}")


if __name__ == "__main__":
    {"select": select, "resynth": resynth, "freeze": freeze}[sys.argv[1]]()
