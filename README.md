# The Synthetic-Voice Penalty

**Do audio-LLM voice agents treat a cloned voice differently from the same person's real voice?**

Audio LLMs increasingly hear synthetic voices: accessibility users speaking through TTS,
agent-to-agent calls, robocalls. And most audio-LLM bias audits are built with TTS stimuli,
assuming synthetic-ness is inert. This project holds the speaker and the words fixed and
compares a real recording, a zero-shot clone of the same utterance, a neural-codec
resynthesis of the real audio, and a stock synthetic voice, across four behavioural outcomes
and an explicit "real or synthetic?" probe, on several model families.

Status: experiments in progress (2026-09-24). Numbers appear here when `results/analysis.json`
is final.

## Layout

| path | contents |
|---|---|
| `EXPERIMENT_PLAN.md`, `site/plan.html` | frozen design, pre-registered directions, budget |
| `MILESTONES.md` | checkpoint log and spend |
| `experiments/` | `build_corpus.py` (select, resynth, freeze), `clone_local.py` (Chatterbox on Apple Silicon), `modal_clone.py` (GPU alternative), `gen_mcq.py`, `runner.py` (OpenRouter), `run_local.py` (open-weight), `judge_o5.py`, `analyze.py`, `prompts.py`, `cost_tracker.py` |
| `corpus/` | `items.json`, `mcq.json`, `manifest.csv`, `FROZEN.json` (audio regenerates from LibriSpeech + the scripts) |
| `results/` | raw JSONL per model, `analysis.json`, spend log |
| `lit_review/` | 96 verified references, novelty delineation |

## Reproduce

```bash
brew install ffmpeg
pip install -r requirements.txt
cd corpus/raw && curl -sSLO https://www.openslr.org/resources/12/test-clean.tar.gz && tar xzf test-clean.tar.gz && cd ../..
cd experiments
python3 build_corpus.py select && python3 build_corpus.py resynth
python3 clone_local.py                       # Chatterbox, ~1.5 h on an M-series GPU
python3 build_corpus.py freeze               # loudnorm + SHA-256 manifest
python3 gen_mcq.py                           # OPENROUTER_API_KEY in ../.env
python3 runner.py --model google/gemini-3.6-flash
python3 runner.py --model google/gemini-3.1-pro-preview --subset pro --outcomes O2,O3,O4
python3 runner.py --model google/gemini-3.6-flash --battery noise
python3 runner.py --model google/gemini-3.6-flash --battery stability
python3 run_local.py --model voxtral
python3 judge_o5.py
python3 analyze.py
```
