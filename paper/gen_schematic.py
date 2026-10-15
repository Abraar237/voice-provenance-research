#!/usr/bin/env python3
"""Generate the Figure 1 pipeline schematic with Nano Banana 2 (gemini-3.1-flash-image).

The image is a schematic, not data. Every string in it is fixed in the prompt below and must be
checked by eye after each generation, because image models can misspell.

    python3 paper/gen_schematic.py [out.png] [model]

Reads GEMINI_API_KEY from the environment.
"""
import base64, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "iclr", "assets", "fig1_schematic.png")
MODEL = sys.argv[2] if len(sys.argv) > 2 else "gemini-3.1-flash-image"

PROMPT = """Create a clean schematic diagram of an experimental pipeline for an academic machine-learning paper (ICLR style). Flat vector style, pure white background, thin dark-gray outlines, rounded rectangles, soft pastel fills, a clean sans-serif typeface, generous spacing. No shadows, no gradients, no 3D, no people, no decoration, no title, no watermark. Wide landscape layout. Six columns read left to right, each with a small bold numbered heading at the top, joined by thick gray right-pointing arrows.

COLUMN 1, heading "1. Dataset". One box with a small book icon and a small waveform icon. Text in the box: "LibriSpeech test-clean", then "40 readers", then "200 real utterances".

COLUMN 2, heading "2. Four matched clips". Four boxes stacked vertically, each with a tiny waveform icon on its left. Same width.
Box 1, light green fill: bold "REAL", small text "original recording".
Box 2, light blue fill: bold "CLONE", small text "same speaker, same words".
Box 3, light orange fill: bold "RESYNTH", small text "real audio, 6 kbps codec".
Box 4, light purple fill: bold "STOCK", small text "default synthetic voice".
Below the four boxes, small gray text: "800 clips, loudness-matched".

COLUMN 3, heading "3. Audio LLMs". Three boxes stacked, each with a small chip icon:
"Gemini 3.6 Flash" with small text "n = 200";
"Gemini 3.1 Pro" with small text "n = 60";
"Voxtral-Mini-3B" with small text "n = 40".

COLUMN 4, heading "4. Five tasks per clip". Five short rows stacked, each a small rounded tag. From top to bottom:
"O1 Transcribe";
"O2 Grade the reading 1-10";
"O3 Content question";
"O5 Assistant reply";
then a small gap, then "O4 Real or synthetic?" alone at the bottom.
To the right of the top four tags (O1, O2, O3, O5) draw one thin curly bracket labeled "behaviour". To the right of the single bottom tag (O4) draw a separate small bracket labeled "self-report".

COLUMN 5, heading "5. Paired analysis". One box containing three short lines: "CLONE minus REAL", "RESYNTH minus REAL", "STOCK minus REAL". Under the box, small gray text: "speaker bootstrap, 49 tests corrected".

COLUMN 6, heading "6. Findings". Three stacked boxes:
Light green box: bold "Clone: no change", small text "grade +0.005".
Light orange box: bold "Codec: grade drops", small text "-0.31, survives correction".
Light gray box: bold "Probe: near chance", small text "real called synthetic 74.5%".

Spell every quoted string exactly as written, including numbers and signs. All text must be large and easy to read when the image is printed 14 centimetres wide. Do not add any other words, numbers or labels."""


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY not set")
    body = {"contents": [{"parts": [{"text": PROMPT}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": "21:9", "imageSize": "4K"}}}
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
