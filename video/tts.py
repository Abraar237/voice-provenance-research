#!/usr/bin/env python3
"""Generate narration cues with ElevenLabs with-timestamps, build the full
narration track with per-cue gaps, and emit a words.json timing database
with absolute film-clock times."""
import base64
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(HERE, "audio")
os.makedirs(AUDIO, exist_ok=True)

# read key from ../.env without printing it
KEY = None
with open(os.path.join(HERE, "..", ".env")) as f:
    for line in f:
        line = line.strip()
        if line.startswith("ELEVENLABS_API_KEY="):
            KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
if not KEY:
    sys.exit("no ELEVENLABS_API_KEY in .env")

VOICE = "XrExE9yKIg1WjnnlVkGX"  # Matilda

CUES = [
    ("p1", "Every voice agent now hears synthetic voices. People who speak through text-to-speech. People who lost their voice and speak through a clone of it. Agents calling agents. And more than a quarter of robocalls."),
    ("p2", "The working assumption is that the model treats a synthetic voice exactly like a real one. The same assumption sits under the research: sixteen of twenty-one recent bias audits of audio models are built entirely from synthetic speech. Nobody had tested it with the speaker and the words held fixed."),
    ("p3", "So we did. Forty readers from LibriSpeech. Two hundred real utterances. For each one, three matched versions. A zero-shot clone of the same reader saying the same words. The real recording re-encoded through a six kilobit neural codec. And a stock synthetic voice saying the same words."),
    ("p4", "Eight hundred clips. Each one goes to Gemini 3.6 Flash, Gemini 3.1 Pro, and an open-weight model, with five tasks. Transcribe it. Grade the reading out of ten. Answer a question about the content. Say whether the voice is real or AI-generated. And reply to the caller as a voice assistant."),
    ("p5", "First result. The clone is invisible. Flash grades the real recording nine point zero one. It grades the clone nine point zero one. The difference is half a hundredth of a point, and across two hundred paired items the interval runs from minus point one six to plus point one six. Word error rate, the same. Comprehension, the same. Assistant replies, the same length, the same rate of refusal, and never a question about whether the caller is human."),
    ("p6", "Second result. The codec is not invisible. Take the real recording, run it through the codec, and the same model grades it a third of a point lower. That survives multiple-comparison correction, and it is the only effect in the study that does. Intelligibility does not change. The model reacts to artifacts, not to provenance. We had pre-registered the opposite: that artifacts would explain less than half of a provenance effect. There was no provenance effect to explain."),
    ("p7", "Third. We asked the models directly. Real human recording, or AI-generated? Flash called seventy-four point five percent of the genuine recordings synthetic. Pro called ninety percent synthetic. Real versus clone accuracy: fifty-five percent. Barely above a coin flip, with a heavy thumb on the synthetic side."),
    ("p8", "And there is no hidden sensitivity. We had predicted that a model's own grades would separate real from clone better than its stated answer. They do not. The grade-based discriminability is exactly chance."),
    ("p9", "One more model. Voxtral, an open-weight audio model, on forty paired items. It grades the clone a sixth of a point lower than the real recording. The interval includes zero. And when asked, it calls every single clip real, the mirror image of Gemini. The sign pattern we pre-registered, Gemini at or above, open-weight below, is there in the point estimates, and not established by the tests."),
    ("p10", "So, three things. For audit designers: synthetic stimuli are validated for these models, to about a sixth of a grade point, with one new rule. Equalise compression across arms, because the model grades the codec. For deployers: a clone of a person is treated as that person. And do not let the model's own opinion about who is real gate a decision. It calls most real people synthetic."),
    ("p11", "Same speaker, same words. The clone is invisible. The codec is not."),
]

# gap AFTER each cue, seconds (scene-boundary cues get more air)
GAPS = {"p1": 0.6, "p2": 0.8, "p3": 0.7, "p4": 0.9, "p5": 0.8,
        "p6": 0.8, "p7": 0.8, "p8": 0.8, "p9": 0.9, "p10": 0.9,
        "p11": 4.0}
LEAD_IN = 0.6  # silence before p1


def tts(cue_id, text):
    mp3 = os.path.join(AUDIO, f"{cue_id}.mp3")
    aln = os.path.join(AUDIO, f"{cue_id}.align.json")
    if os.path.exists(mp3) and os.path.exists(aln):
        return json.load(open(aln))
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
        data=json.dumps({
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75,
                               "style": 0.25, "speed": 1.0},
        }).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        out = json.load(r)
    with open(mp3, "wb") as f:
        f.write(base64.b64decode(out["audio_base64"]))
    align = out["alignment"]
    json.dump(align, open(aln, "w"))
    return align


def words_from_alignment(align):
    """Group character timings into words (split on whitespace)."""
    words = []
    cur, start, end = "", None, None
    chars = align["characters"]
    s = align["character_start_times_seconds"]
    e = align["character_end_times_seconds"]
    for i, ch in enumerate(chars):
        if ch.isspace():
            if cur:
                words.append({"w": cur, "s": start, "e": end})
                cur, start = "", None
        else:
            if start is None:
                start = s[i]
            cur += ch
            end = e[i]
    if cur:
        words.append({"w": cur, "s": start, "e": end})
    return words


def dur_of(path):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(out.stdout.strip())


def main():
    db = {"cues": []}
    clock = LEAD_IN
    concat_parts = [("silence", LEAD_IN)]
    for cue_id, text in CUES:
        align = words_from_alignment(tts(cue_id, text))
        wav = os.path.join(AUDIO, f"{cue_id}.wav")
        if not os.path.exists(wav):
            subprocess.run(["ffmpeg", "-y", "-v", "quiet",
                            "-i", os.path.join(AUDIO, f"{cue_id}.mp3"),
                            "-ar", "48000", "-ac", "2", wav], check=True)
        d = dur_of(wav)
        db["cues"].append({
            "id": cue_id, "text": text, "start": clock, "dur": d,
            "words": align,
        })
        concat_parts.append(("file", wav))
        gap = GAPS[cue_id]
        concat_parts.append(("silence", gap))
        clock += d + gap
        print(f"{cue_id}: start={clock - d - gap:.2f} dur={d:.2f}")
    db["total"] = clock
    print(f"total narration track: {clock:.2f}s")

    # build the full track
    inputs, filters, idx = [], [], 0
    segs = []
    for kind, val in concat_parts:
        if kind == "silence":
            filters.append(
                f"aevalsrc=0:d={val}:s=48000,aformat=channel_layouts=stereo[s{idx}]")
            segs.append(f"[s{idx}]")
        else:
            inputs += ["-i", val]
            segs.append(f"[{len(inputs)//2 - 1}:a]")
        idx += 1
    fc = ";".join(filters) + ";" + "".join(segs) + \
        f"concat=n={len(segs)}:v=0:a=1[out]"
    full = os.path.join(AUDIO, "narration_raw.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "quiet"] + inputs +
                   ["-filter_complex", fc, "-map", "[out]", full], check=True)
    print("raw track:", dur_of(full))
    json.dump(db, open(os.path.join(HERE, "words.json"), "w"), indent=1)


if __name__ == "__main__":
    pass
    main()
