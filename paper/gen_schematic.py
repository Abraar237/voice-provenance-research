#!/usr/bin/env python3
"""Generate the Figure 1 pipeline schematic with Nano Banana 2 (gemini-3.1-flash-image).

The image is a schematic, not data. Every string in it is fixed in the prompt below and must be
checked by eye after each generation, because image models can misspell.

    python3 paper/gen_schematic.py [out.png] [model]

Reads GEMINI_API_KEY from the environment.
"""
import base64, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "acl", "assets", "fig1_schematic.png")
MODEL = sys.argv[2] if len(sys.argv) > 2 else "gemini-3.1-flash-image"

PROMPT = """Create a clean scientific diagram for an academic research paper. Flat vector style, pure white background, thin dark-gray outlines, soft pastel fills, a clear sans-serif typeface, generous spacing. No shadows, no gradients, no 3D, no decoration, no title, no watermark. Portrait layout, four sections stacked top to bottom, joined by three short thick downward arrows.

SECTION 1. Small heading: "1. Same speaker, same words". Below it one wide rounded card, light gray fill, with a small book icon and a small waveform icon on its left. Text in the card on two lines: "LibriSpeech test-clean" and "40 readers, 200 real utterances".

SECTION 2. Small heading: "2. Four versions of every utterance". Below it four rounded cards in a 2 by 2 grid, each with a tiny waveform icon. Each card has a bold word and a small line under it:
top left, light green fill: "REAL" and "original recording";
top right, light blue fill: "CLONE" and "zero-shot clone";
bottom left, light orange fill: "RESYNTH" and "6 kbps codec";
bottom right, light purple fill: "STOCK" and "default TTS voice".

SECTION 3. Small heading: "3. Three audio LLMs, five tasks". Below it three small chip icons in one row with labels underneath: "Gemini 3.6 Flash", "Gemini 3.1 Pro", "Voxtral-Mini-3B". Under them five small pill-shaped tags in one row: "transcribe", "grade", "question", "reply", "real or AI?".

SECTION 4. Small heading: "4. Compare each version with REAL". Below it three rounded result boxes side by side. Left box, light green fill, two lines: "Clone" and "grade +0.005". Middle box, light orange fill, two lines: "Codec" and "grade -0.31". Right box, light gray fill, two lines: "Self-report" and "near chance".

At the very bottom, one line of larger bold text: "The model hears the codec, not the clone."

Spell every quoted string exactly as written. All text must be large and easy to read when the image is printed 8 centimetres wide. Do not add any other words, numbers or labels."""


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY not set")
    body = {"contents": [{"parts": [{"text": PROMPT}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": "3:4", "imageSize": "2K"}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:400].decode('utf-8', 'replace')}")
    for part in r["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            open(OUT, "wb").write(base64.b64decode(part["inlineData"]["data"]))
            print("wrote", OUT, part["inlineData"].get("mimeType"))
            return
    sys.exit("no image in response: " + json.dumps(r)[:400])


if __name__ == "__main__":
    main()
