#!/usr/bin/env python3
"""Three concept GIFs in the script-bias site aesthetic: 840x840, ~80ms/frame,
white-cream card, flat bars, thin rules, monospace numerals, flowing dots,
seamless-ish loop with hold. Numbers from results/analysis.json."""

import json
import math
import pathlib

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "docs" / "assets" / "gifs"
OUT.mkdir(parents=True, exist_ok=True)
A = json.loads((HERE.parent / "results" / "analysis.json").read_text())

W = H = 840
INK = (22, 19, 13)
INK2 = (58, 53, 43)
MUTED = (109, 102, 90)
FAINT = (164, 156, 140)
RULE = (231, 226, 213)
BG = (253, 252, 250)
SLATE = (21, 94, 140)
HOT = (179, 0, 107)
SHELF = (192, 100, 26)
GOOD = (28, 122, 85)

MENLO = "/System/Library/Fonts/Menlo.ttc"
HELV = "/System/Library/Fonts/Helvetica.ttc"


def F(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


f_title = F(MENLO, 30, 1)   # Menlo bold
f_sub = F(HELV, 15)
f_note = F(HELV, 13)
f_label = F(HELV, 17)
f_num = F(MENLO, 22)
f_big = F(MENLO, 44, 1)
f_mono = F(MENLO, 16)


def ease(t):
    return 0 if t <= 0 else 1 if t >= 1 else 0.5 - 0.5 * math.cos(math.pi * t)


def seg(t, a, b):
    return ease((t - a) / (b - a)) if b > a else 1.0


def card(d):
    d.rectangle([0, 0, W, H], fill=BG)
    d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=2)


def title_block(d, title, sub):
    d.text((W // 2, 62), title, font=f_title, fill=INK, anchor="mm")
    d.text((W // 2, 96), sub.upper(), font=f_sub, fill=MUTED, anchor="mm")


def footer(d, text):
    d.text((W // 2, H - 44), text.upper(), font=f_note, fill=FAINT, anchor="mm")


def hbar(d, x, y, w, h, frac, color, track=True):
    if track:
        d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    fw = int(w * max(0.0, min(1.0, frac)))
    if fw > 5:
        d.rectangle([x + 2, y + 2, x + fw - 2, y + h - 2], fill=color)


def save(frames, name):
    frames[0].save(OUT / name, save_all=True, append_images=frames[1:],
                   duration=80, loop=0, optimize=True)
    print(name, len(frames), "frames,", (OUT / name).stat().st_size // 1024, "KB")


FL = A["models"]["google/gemini-3.6-flash"]
G = {a: FL["arms"][a]["grade"]["mean"] for a in ("real", "clone", "resynth", "stock")}
S = {a: FL["probe"][a]["share_synthetic"] for a in ("real", "clone", "resynth", "stock")}
WER = {a: FL["arms"][a]["wer"]["mean"] for a in ("real", "clone")}
N = 110
ARM_COL = {"real": SLATE, "clone": HOT, "resynth": SHELF, "stock": (122, 111, 155)}
ARM_LAB = {"real": "REAL recording", "clone": "CLONE of the same reader", "resynth": "real audio through a codec", "stock": "STOCK synthetic voice"}


def grade_gif(name, title, sub, arms, note, note_col):
    frames = []
    for fi in range(N):
        t = fi / N
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        card(d)
        title_block(d, title, sub)
        y0 = 190
        for i, a in enumerate(arms):
            y = y0 + i * 130
            g = seg(t, 0.05 + 0.18 * i, 0.32 + 0.18 * i)
            d.text((70, y), ARM_LAB[a], font=f_label, fill=INK, anchor="lm")
            hbar(d, 70, y + 22, 560, 34, (G[a] / 10) * g, ARM_COL[a])
            if g > 0.98:
                d.text((650, y + 39), f"{G[a]:.2f}", font=f_big, fill=ARM_COL[a], anchor="lm")
        gn = seg(t, 0.62, 0.78)
        if gn > 0:
            col = tuple(int(BG[k] + (note_col[k] - BG[k]) * gn) for k in range(3))
            d.text((W // 2, 640), note, font=f_num, fill=col, anchor="mm")
            d.text((W // 2, 672), "reading grade out of 10 · Gemini 3.6 Flash · 200 paired items", font=f_note, fill=MUTED, anchor="mm")
        footer(d, "same speaker, same words · 40 readers")
        if t > 0.9:
            d.text((W - 40, H - 76), "replay", font=f_note, fill=FAINT, anchor="rm")
        frames.append(im)
    save(frames, name)


grade_gif("the-clone-is-invisible.gif", "The clone is invisible.", "Gemini grades the real reader and a clone of the same reader",
          ["real", "clone"], f"difference {G['clone']-G['real']:+.3f} points  ·  interval [-0.16, +0.16]  ·  WER {WER['real']*100:.1f}% vs {WER['clone']*100:.1f}%", GOOD)
grade_gif("the-codec-is-not.gif", "The codec is not.", "the same real recording, before and after a 6 kbps codec round trip",
          ["real", "resynth"], f"difference {G['resynth']-G['real']:+.2f} points  ·  survives correction  ·  intelligibility unchanged", SHELF)


def probe_gif():
    frames = []
    arms = ["real", "clone", "resynth", "stock"]
    for fi in range(N):
        t = fi / N
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        card(d)
        title_block(d, "Real, or AI-generated?", "share of clips the model calls SYNTHETIC")
        y0 = 175
        for i, a in enumerate(arms):
            y = y0 + i * 108
            g = seg(t, 0.05 + 0.14 * i, 0.30 + 0.14 * i)
            d.text((70, y), ARM_LAB[a], font=f_label, fill=INK, anchor="lm")
            hbar(d, 70, y + 22, 560, 30, S[a] * g, ARM_COL[a])
            if g > 0.98:
                d.text((650, y + 37), f"{S[a]*100:.1f}%", font=f_big, fill=ARM_COL[a], anchor="lm")
        gn = seg(t, 0.68, 0.84)
        if gn > 0:
            col = tuple(int(BG[k] + (HOT[k] - BG[k]) * gn) for k in range(3))
            d.text((W // 2, 640), f"{S['real']*100:.1f}% of genuine recordings called synthetic", font=f_num, fill=col, anchor="mm")
            d.text((W // 2, 672), f"real vs clone balanced accuracy {FL['probe']['balanced_acc_real_vs_clone']:.3f} · Gemini 3.6 Flash", font=f_note, fill=MUTED, anchor="mm")
        footer(d, "explicit probe · one word answer · 800 clips")
        if t > 0.9:
            d.text((W - 40, H - 76), "replay", font=f_note, fill=FAINT, anchor="rm")
        frames.append(im)
    save(frames, "who-is-real.gif")


probe_gif()
