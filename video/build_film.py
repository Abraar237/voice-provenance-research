#!/usr/bin/env python3
"""Research film: 1920x1080 @ 60 fps, phrase-anchored to the narration timing database
(words.json from tts.py). Visual system shared with the site and paper figures: cream card,
flat bars, Menlo bold titles, Helvetica labels, monospace numerals, continuous motion, marker
annotations landing on the spoken number. Renders PNG frames -> ffmpeg.
Numbers from results/analysis.json."""

import json
import math
import pathlib
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
FRAMES = HERE / "frames"
W, H, FPS = 1920, 1080, 60
INK = (22, 19, 13); INK2 = (58, 53, 43); MUTED = (109, 102, 90)
FAINT = (164, 156, 140); RULE = (231, 226, 213); BG = (253, 252, 250)
SLATE = (21, 94, 140); HOT = (179, 0, 107); SHELF = (192, 100, 26); GOOD = (28, 122, 85)
PURPLE = (122, 111, 155)
MENLO = "/System/Library/Fonts/Menlo.ttc"; HELV = "/System/Library/Fonts/Helvetica.ttc"


def F(p, s, i=0):
    return ImageFont.truetype(p, s, index=i)


f_h1 = F(MENLO, 72, 1); f_h2 = F(MENLO, 52, 1); f_sub = F(HELV, 30)
f_lab = F(HELV, 32); f_note = F(HELV, 24); f_eyebrow = F(HELV, 22)
f_num = F(MENLO, 40); f_big = F(MENLO, 120, 1); f_mono = F(MENLO, 34)
f_mid = F(MENLO, 64, 1); f_body = F(HELV, 36)

A = json.load(open(ROOT / "results" / "analysis.json"))
FL = A["models"]["google/gemini-3.6-flash"]
PRO = A["models"]["google/gemini-3.1-pro-preview"]
VOX = A["models"].get("mistralai/Voxtral-Mini-3B-2507")
DB = json.load(open(HERE / "words.json"))
CUE = {c["id"]: c for c in DB["cues"]}
TOTAL = DB["total"]


def at(cue, phrase):
    """Film-clock time at which the narrator starts the given phrase in the cue."""
    c = CUE[cue]
    words = [w["w"].lower().strip(".,;:!?\"'") for w in c["words"]]
    target = [w.lower().strip(".,;:!?\"'") for w in phrase.split()]
    for i in range(len(words) - len(target) + 1):
        if words[i:i + len(target)] == target:
            return c["start"] + c["words"][i]["s"]
    raise KeyError(f"phrase not found in {cue}: {phrase!r}")


def cue_start(cue):
    return CUE[cue]["start"]


def cue_end(cue):
    return CUE[cue]["start"] + CUE[cue]["dur"]


def ease(x):
    return 0 if x <= 0 else 1 if x >= 1 else 0.5 - 0.5 * math.cos(math.pi * x)


def seg(t, a, b):
    return ease((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)


def mix(c1, c2, f):
    return tuple(int(a + (b - a) * f) for a, b in zip(c1, c2))


def base(d, t):
    d.rectangle([0, 0, W, H], fill=BG)
    d.rectangle([28, 28, W - 28, H - 28], outline=RULE, width=3)
    d.text((70, 62), "S A M E   S P E A K E R ,   S A M E   W O R D S", font=f_eyebrow, fill=FAINT)
    d.text((W - 70, 62), "R E S E A R C H   F I L M", font=f_eyebrow, fill=FAINT, anchor="ra")
    for k in range(7):
        x = 70 + ((t * 42 + k * 260) % (W - 140))
        d.ellipse([x - 4, H - 60, x + 4, H - 52], fill=mix(RULE, FAINT, 0.5))


def hbar(d, x, y, w, h, frac, color, outline=True):
    if outline:
        d.rectangle([x, y, x + w, y + h], outline=RULE, width=3)
    fw = int(w * max(0.0, min(1.0, frac)))
    if fw > 6:
        d.rectangle([x + 3, y + 3, x + fw - 3, y + h - 3], fill=color)


def underline(d, x0, x1, y, g, color=HOT):
    """marker-pen underline drawing on with progress g"""
    if g <= 0:
        return
    xe = x0 + (x1 - x0) * g
    d.line([(x0, y), (xe, y + 3)], fill=mix(BG, color, 0.55), width=9)


def ring(d, cx, cy, r, g, color=HOT):
    if g <= 0:
        return
    d.arc([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], start=-90, end=-90 + 360 * g, fill=mix(BG, color, 0.6), width=7)


def grade_bars(d, t, rows, y0=330, t_anchor=None, note=None, note_t=None, note_col=HOT):
    """rows: list of (label, value, color, appear_time)"""
    for i, (lab, val, col, ta) in enumerate(rows):
        y = y0 + i * 150
        g = seg(t, ta, ta + 1.1)
        if g <= 0:
            continue
        d.text((160, y), lab, font=f_lab, fill=mix(BG, INK, min(1, g * 3)), anchor="lm")
        hbar(d, 160, y + 30, 1100, 56, (val / 10.0) * g, col)
        if g > 0.99:
            d.text((1300, y + 58), f"{val:.2f}", font=f_mid, fill=col, anchor="lm")
    if note and note_t is not None:
        g = seg(t, note_t, note_t + 0.8)
        if g > 0:
            d.text((W // 2, y0 + len(rows) * 150 + 40), note, font=f_body, fill=mix(BG, note_col, g), anchor="mm")


# ---------------------------------------------------------------- scenes
def s1(d, t):  # cold open
    d.text((W // 2, 250), "The clone is invisible.", font=f_h1, fill=INK, anchor="mm")
    d.text((W // 2, 340), "The codec is not.", font=f_h1, fill=SHELF, anchor="mm")
    items = [("text-to-speech users", at("p1", "People who speak")),
             ("voice-banking users, through a clone", at("p1", "People who lost")),
             ("agents calling agents", at("p1", "Agents calling")),
             ("robocalls: more than a quarter are synthetic", at("p1", "more than a quarter"))]
    for i, (txt, ta) in enumerate(items):
        g = seg(t, ta, ta + 0.7)
        if g > 0:
            y = 520 + i * 90
            d.ellipse([560, y - 12, 584, y + 12], fill=mix(BG, SLATE, g))
            d.text((620, y), txt, font=f_body, fill=mix(BG, INK, g), anchor="lm")
    d.text((W // 2, 950), "every voice agent hears synthetic voices", font=f_sub, fill=MUTED, anchor="mm")


def s2(d, t):  # the assumption
    d.text((W // 2, 200), "The untested assumption", font=f_h2, fill=INK, anchor="mm")
    g1 = seg(t, at("p2", "The working assumption"), at("p2", "The working assumption") + 0.8)
    d.text((W // 2, 330), "a synthetic voice is treated exactly like a real one", font=f_body, fill=mix(BG, INK2, g1), anchor="mm")
    g2 = seg(t, at("p2", "sixteen of"), at("p2", "sixteen of") + 1.2)
    if g2 > 0:
        d.text((W // 2, 470), "audio-model bias audits we reviewed", font=f_sub, fill=mix(BG, MUTED, g2), anchor="mm")
        for i in range(21):
            x = 360 + i * 58
            col = HOT if i < 16 else RULE
            fill = mix(BG, col, g2) if i < 16 else mix(BG, RULE, 1)
            d.rectangle([x, 520, x + 44, 600], fill=fill, outline=mix(BG, FAINT, g2), width=2)
        d.text((W // 2, 660), "16 of 21 use synthetic speech only", font=f_mid, fill=mix(BG, HOT, g2), anchor="mm")
    g3 = seg(t, at("p2", "Nobody had"), at("p2", "Nobody had") + 0.8)
    if g3 > 0:
        d.text((W // 2, 820), "nobody had held the speaker and the words fixed", font=f_body, fill=mix(BG, INK, g3), anchor="mm")
        underline(d, 540, 1380, 852, seg(t, at("p2", "held the"), at("p2", "held the") + 0.7))


def s3(d, t):  # the design
    d.text((W // 2, 170), "Same speaker, same words, four versions", font=f_h2, fill=INK, anchor="mm")
    g0 = seg(t, cue_start("p3"), cue_start("p3") + 0.8)
    d.rounded_rectangle([100, 380, 600, 620], radius=18, outline=mix(BG, INK2, g0), width=4)
    d.text((350, 450), "one LibriSpeech reader", font=f_lab, fill=mix(BG, INK, g0), anchor="mm")
    d.text((350, 510), "40 readers", font=f_num, fill=mix(BG, SLATE, g0), anchor="mm")
    d.text((350, 565), "200 real utterances", font=f_num, fill=mix(BG, SLATE, g0), anchor="mm")
    arms = [("REAL", "the original recording", SLATE, at("p3", "Two hundred")),
            ("CLONE", "zero-shot clone of the same reader", HOT, at("p3", "A zero-shot")),
            ("RESYNTH", "real audio through a 6 kbps codec", SHELF, at("p3", "The real recording")),
            ("STOCK", "a default synthetic voice", PURPLE, at("p3", "And a stock"))]
    for i, (name, sub, col, ta) in enumerate(arms):
        g = seg(t, ta, ta + 0.7)
        if g <= 0:
            continue
        y = 300 + i * 150
        d.line([(600, 500), (700, y + 50)], fill=mix(BG, RULE, g), width=4)
        d.rounded_rectangle([700, y, 1500, y + 110], radius=16, outline=mix(BG, col, g), width=4, fill=mix(BG, col, 0.06 * g))
        d.text((740, y + 35), name, font=f_num, fill=mix(BG, col, g), anchor="lm")
        d.text((740, y + 80), sub, font=f_note, fill=mix(BG, INK2, g), anchor="lm")


def s4(d, t):  # tasks
    d.text((W // 2, 170), "800 clips, three model families, five tasks", font=f_h2, fill=INK, anchor="mm")
    models = [("Gemini 3.6 Flash", at("p4", "Gemini 3.6")), ("Gemini 3.1 Pro", at("p4", "Gemini 3.1")), ("open-weight model", at("p4", "an open-weight"))]
    for i, (m, ta) in enumerate(models):
        g = seg(t, ta, ta + 0.6)
        if g > 0:
            y = 330 + i * 100
            d.rounded_rectangle([160, y, 640, y + 76], radius=14, outline=mix(BG, SLATE, g), width=4)
            d.text((400, y + 38), m, font=f_lab, fill=mix(BG, SLATE, g), anchor="mm")
    tasks = [("O1  transcribe it", at("p4", "Transcribe it")), ("O2  grade the reading out of ten", at("p4", "Grade the")),
             ("O3  answer a content question", at("p4", "Answer a")), ("O4  real, or AI-generated?", at("p4", "Say whether")),
             ("O5  reply as a voice assistant", at("p4", "And reply"))]
    for i, (txt, ta) in enumerate(tasks):
        g = seg(t, ta, ta + 0.6)
        if g > 0:
            y = 340 + i * 90
            d.text((820, y), txt, font=f_body, fill=mix(BG, INK, g), anchor="lm")
    d.text((W // 2, 880), "temperature 0, one clip per call, five directions pre-registered before any clip was cloned", font=f_note, fill=MUTED, anchor="mm")


def s5(d, t):  # result 1: clone invisible
    d.text((W // 2, 170), "The clone is invisible", font=f_h2, fill=GOOD, anchor="mm")
    d.text((W // 2, 240), "reading grade out of 10, Gemini 3.6 Flash, 200 paired items", font=f_sub, fill=MUTED, anchor="mm")
    rows = [("REAL recording", FL["arms"]["real"]["grade"]["mean"], SLATE, at("p5", "nine point zero one. It")),
            ("CLONE of the same reader", FL["arms"]["clone"]["grade"]["mean"], HOT, at("p5", "It grades the clone"))]
    grade_bars(d, t, rows, y0=330)
    g = seg(t, at("p5", "The difference"), at("p5", "The difference") + 0.8)
    if g > 0:
        c = FL["contrasts"]["grade:clone-real"]
        d.text((W // 2, 680), f"difference {c['mean']:+.3f}   interval [{c['ci'][0]:+.2f}, {c['ci'][1]:+.2f}]", font=f_body, fill=mix(BG, GOOD, g), anchor="mm")
    lines = [("word error rate  2.9% vs 2.7%", at("p5", "Word error")), ("comprehension  99.5% vs 99.5%", at("p5", "Comprehension")),
             ("assistant replies  same length, same refusals, never asks if the caller is human", at("p5", "Assistant replies"))]
    for i, (txt, ta) in enumerate(lines):
        gg = seg(t, ta, ta + 0.6)
        if gg > 0:
            d.text((W // 2, 780 + i * 60), txt, font=f_lab, fill=mix(BG, INK2, gg), anchor="mm")


def s6(d, t):  # result 2: codec
    d.text((W // 2, 170), "The codec is not", font=f_h2, fill=SHELF, anchor="mm")
    d.text((W // 2, 240), "the same real recording, before and after a 6 kbps codec round trip", font=f_sub, fill=MUTED, anchor="mm")
    rows = [("REAL recording", FL["arms"]["real"]["grade"]["mean"], SLATE, at("p6", "Take the real")),
            ("RESYNTH  (real audio through the codec)", FL["arms"]["resynth"]["grade"]["mean"], SHELF, at("p6", "run it through"))]
    grade_bars(d, t, rows, y0=330)
    c = FL["contrasts"]["grade:resynth-real"]
    g = seg(t, at("p6", "a third of a point"), at("p6", "a third of a point") + 0.8)
    if g > 0:
        d.text((W // 2, 680), f"difference {c['mean']:+.2f}   p = 3.5 x 10^-4", font=f_body, fill=mix(BG, SHELF, g), anchor="mm")
    g2 = seg(t, at("p6", "That survives"), at("p6", "That survives") + 0.7)
    if g2 > 0:
        d.text((W // 2, 760), "survives correction: the only effect in the study that does", font=f_lab, fill=mix(BG, INK, g2), anchor="mm")
        underline(d, 560, 1360, 785, seg(t, at("p6", "the only effect"), at("p6", "the only effect") + 0.7), SHELF)
    g3 = seg(t, at("p6", "The model reacts"), at("p6", "The model reacts") + 0.7)
    if g3 > 0:
        d.text((W // 2, 850), "artifacts, not provenance", font=f_mid, fill=mix(BG, INK, g3), anchor="mm")
    g4 = seg(t, at("p6", "We had pre-registered"), at("p6", "We had pre-registered") + 0.7)
    if g4 > 0:
        d.text((W // 2, 940), "pre-registered direction D2: reversed", font=f_lab, fill=mix(BG, MUTED, g4), anchor="mm")


def s7(d, t):  # result 3: probe
    d.text((W // 2, 170), "Real, or AI-generated?", font=f_h2, fill=INK, anchor="mm")
    d.text((W // 2, 240), "share of genuine recordings the model called SYNTHETIC", font=f_sub, fill=MUTED, anchor="mm")
    rows = [("Gemini 3.6 Flash", FL["probe"]["real"]["share_synthetic"], at("p7", "Flash called")),
            ("Gemini 3.1 Pro", PRO["probe"]["real"]["share_synthetic"], at("p7", "Pro called"))]
    for i, (lab, val, ta) in enumerate(rows):
        y = 330 + i * 150
        g = seg(t, ta, ta + 1.1)
        if g <= 0:
            continue
        d.text((160, y), lab, font=f_lab, fill=mix(BG, INK, min(1, g * 3)), anchor="lm")
        hbar(d, 160, y + 30, 1100, 56, val * g, HOT)
        if g > 0.99:
            d.text((1300, y + 58), f"{val*100:.1f}%", font=f_mid, fill=HOT, anchor="lm")
    g = seg(t, at("p7", "Real versus clone"), at("p7", "Real versus clone") + 0.8)
    if g > 0:
        d.text((W // 2, 700), f"real vs clone balanced accuracy  {FL['probe']['balanced_acc_real_vs_clone']:.3f}", font=f_body, fill=mix(BG, INK, g), anchor="mm")
    g2 = seg(t, at("p7", "Barely above"), at("p7", "Barely above") + 0.7)
    if g2 > 0:
        d.text((W // 2, 800), "barely above a coin flip, with a heavy thumb on the synthetic side", font=f_lab, fill=mix(BG, MUTED, g2), anchor="mm")
        ring(d, 1130, 700, 200, seg(t, at("p7", "coin flip"), at("p7", "coin flip") + 0.8))


def s8(d, t):  # no hidden sensitivity
    d.text((W // 2, 170), "No hidden sensitivity", font=f_h2, fill=INK, anchor="mm")
    d.text((W // 2, 240), "how well real is separated from clone, above chance, on the same 200 items", font=f_sub, fill=MUTED, anchor="mm")
    d1 = FL["d1"]["grade"]
    rows = [("implicit: the model's own grades", d1["implicit_auc_dirfree"], HOT, at("p8", "a model's own")),
            ("explicit: its stated answer", d1["explicit_auc"], SLATE, at("p8", "its stated"))]
    for i, (lab, val, col, ta) in enumerate(rows):
        y = 360 + i * 160
        g = seg(t, ta, ta + 1.0)
        if g <= 0:
            continue
        d.text((160, y), lab, font=f_lab, fill=mix(BG, INK, min(1, g * 3)), anchor="lm")
        hbar(d, 160, y + 30, 1100, 56, ((val - 0.5) / 0.1) * g, col)
        if g > 0.99:
            d.text((1300, y + 58), f"AUC {val:.3f}", font=f_mid, fill=col, anchor="lm")
    d.text((160, 720), "bar length = AUC above 0.5, full width = 0.6", font=f_note, fill=FAINT, anchor="lm")
    g = seg(t, at("p8", "exactly chance"), at("p8", "exactly chance") + 0.7)
    if g > 0:
        d.text((W // 2, 840), "what little the model can discriminate, it can also say", font=f_body, fill=mix(BG, INK, g), anchor="mm")


def s9(d, t):  # open-weight
    d.text((W // 2, 170), "The open-weight model", font=f_h2, fill=INK, anchor="mm")
    d.text((W // 2, 240), "Voxtral-Mini-3B, 40 readers, one item each, real vs clone", font=f_sub, fill=MUTED, anchor="mm")
    if VOX:
        rows = [("REAL recording", VOX["arms"]["real"]["grade"]["mean"], SLATE, cue_start("p9") + 0.8),
                ("CLONE of the same reader", VOX["arms"]["clone"]["grade"]["mean"], HOT, cue_start("p9") + 2.2)]
        grade_bars(d, t, rows, y0=330)
        c = VOX["contrasts"].get("grade:clone-real")
        g = seg(t, cue_start("p9") + 4.5, cue_start("p9") + 5.3)
        if g > 0 and c:
            d.text((W // 2, 680), f"difference {c['mean']:+.2f}   interval [{c['ci'][0]:+.2f}, {c['ci'][1]:+.2f}]", font=f_body, fill=mix(BG, INK, g), anchor="mm")
        g2 = seg(t, cue_start("p9") + 7.5, cue_start("p9") + 8.3)
        if g2 > 0 and "real" in VOX["probe"]:
            d.text((W // 2, 790), f"genuine recordings called SYNTHETIC  {VOX['probe']['real']['share_synthetic']*100:.0f}%   ·   real vs clone accuracy {VOX['probe'].get('balanced_acc_real_vs_clone', 0.5):.2f}", font=f_lab, fill=mix(BG, INK2, g2), anchor="mm")


def s10(d, t):  # takeaway
    d.text((W // 2, 240), "The takeaway", font=f_h2, fill=INK, anchor="mm")
    lines = [("Synthetic stimuli are validated for these models, to about a sixth of a grade point.", at("p10", "synthetic stimuli"), GOOD),
             ("Equalise compression across arms: the model grades the codec.", at("p10", "Equalise compression"), SHELF),
             ("A clone of a person is treated as that person.", at("p10", "a clone of a person"), SLATE),
             ("Do not let the model's opinion about who is real gate a decision.", at("p10", "do not let"), HOT)]
    for i, (txt, ta, col) in enumerate(lines):
        g = seg(t, ta, ta + 0.9)
        if g > 0:
            y = 400 + i * 130
            d.ellipse([200, y - 14, 228, y + 14], fill=mix(BG, col, g))
            d.text((270, y), txt, font=f_body, fill=mix(BG, INK, g), anchor="lm")


def s11(d, t):  # end card
    g = seg(t, cue_start("p11"), cue_start("p11") + 0.8)
    d.text((W // 2, 400), "The clone is invisible.", font=f_h1, fill=mix(BG, INK, g), anchor="mm")
    g2 = seg(t, at("p11", "The codec"), at("p11", "The codec") + 0.8)
    d.text((W // 2, 500), "The codec is not.", font=f_h1, fill=mix(BG, SHELF, g2), anchor="mm")
    g3 = seg(t, cue_end("p11") + 0.3, cue_end("p11") + 1.3)
    if g3 > 0:
        d.text((W // 2, 720), "Vizuara Research", font=f_num, fill=mix(BG, INK, g3), anchor="mm")
        d.text((W // 2, 780), "paper, code, and data: github.com/Abraar237/voice-provenance-research", font=f_note, fill=mix(BG, MUTED, g3), anchor="mm")


SCENES = [("p1", s1), ("p2", s2), ("p3", s3), ("p4", s4), ("p5", s5), ("p6", s6), ("p7", s7), ("p8", s8), ("p9", s9), ("p10", s10), ("p11", s11)]
XFADE = 0.45


def bounds():
    out = []
    for i, (cue, fn) in enumerate(SCENES):
        a = cue_start(cue) - (0.35 if i else 0)
        b = cue_start(SCENES[i + 1][0]) - 0.35 if i + 1 < len(SCENES) else TOTAL + 1.0
        out.append((a, b, fn))
    return out


BOUNDS = None


def render_at(t):
    global BOUNDS
    if BOUNDS is None:
        BOUNDS = bounds()
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    base(d, t)
    layers = []
    for a, b, fn in BOUNDS:
        if a - XFADE <= t < b + XFADE:
            alpha = min(seg(t, a - XFADE, a), 1 - seg(t, b, b + XFADE))
            layers.append((alpha, fn))
    for alpha, fn in layers:
        if alpha >= 0.999:
            fn(d, t)
        elif alpha > 0:
            im2 = Image.new("RGB", (W, H))
            d2 = ImageDraw.Draw(im2)
            base(d2, t)
            fn(d2, t)
            im = Image.blend(im, im2, alpha)
            d = ImageDraw.Draw(im)
    return im


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        for a, b, fn in bounds():
            print(f"{fn.__name__}: {a:.1f}-{b:.1f}")
        for cue, fn in SCENES:
            im = render_at(cue_start(cue) + 2.0)
            im.save(HERE / f"_check_{cue}.png")
        print("anchors resolve; check frames written")
        return
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir()
    total = int((TOTAL + 1.5) * FPS)
    for f in range(total):
        im = render_at(f / FPS)
        im.save(FRAMES / f"f{f:06d}.png", compress_level=1)
        if f % 600 == 0:
            print(f"{f}/{total}", flush=True)
    print("frames done:", total)


if __name__ == "__main__":
    main()
