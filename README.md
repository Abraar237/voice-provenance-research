# The Clone Is Invisible, the Codec Is Not

**A matched audit of synthetic-voice provenance in audio language models.**

Mohammed Abraar · Vizuara Research · 2026

- **Website:** https://abraar237.github.io/voice-provenance-research/
- **Paper:** [`docs/paper_iclr_preprint.pdf`](docs/paper_iclr_preprint.pdf) (named preprint) · [`docs/paper_iclr_submission.pdf`](docs/paper_iclr_submission.pdf) (anonymous build)

Audio language models increasingly hear synthetic voices, and most audits of these models are
built with synthetic speech on the assumption that being synthetic changes nothing. We tested
that assumption with the speaker and the words held fixed: 40 LibriSpeech readers, 200 real
utterances, and for each one a zero-shot clone of the same reader saying the same words, a
neural-codec re-encoding of the real recording, and a stock synthetic voice.

## Headline numbers

| | Gemini 3.6 Flash (n=200) | Gemini 3.1 Pro (n=60) | Voxtral-Mini-3B (n=40) |
|---|---|---|---|
| grade CLONE − REAL (1–10) | **+0.005** [−0.16, +0.16] | +0.35 [−0.90, +1.46] | −0.175 [−0.40, +0.05] |
| grade RESYNTH − REAL | **−0.31** (p = 3.5×10⁻⁴, survives BH) | +0.12 | — |
| WER real / clone | 2.9% / 2.7% | — | — |
| real recordings called SYNTHETIC | **74.5%** | 89.8% | 0% |
| real vs clone balanced accuracy | 0.555 | 0.54 | 0.50 |

1. **The clone is invisible to behaviour.** Grades, transcripts, comprehension, and assistant replies are the same for the clone and the real recording.
2. **The codec is not.** Re-encoding the real recording lowers its grade by a third of a point with no change in intelligibility; it is the only effect in the study that survives correction.
3. **Asked directly, the models cannot tell, and they lean synthetic** (Gemini) or lean real (Voxtral).
4. **No hidden sensitivity** on Gemini: the model's own grades separate real from clone no better than its stated answer. On Voxtral the implicit signal is slightly larger, with an interval that touches zero.

Five directions were pre-registered before any clip was cloned; two failed or reversed and are reported as such.

## Responsible framing

Voices are cloned only from LibriSpeech (public-domain audiobook readers, CC BY 4.0), only as
matched stimuli for measuring model behaviour, and are not released as voices. Only public
model APIs and an open-weight checkpoint were used. The corpus regenerates from LibriSpeech
and the scripts; no audio ships in the repository.

## Reproduce

```bash
brew install ffmpeg tectonic
pip install -r requirements.txt
cd corpus/raw && curl -sSLO https://www.openslr.org/resources/12/test-clean.tar.gz && tar xzf test-clean.tar.gz && cd ../..
cd experiments
python3 build_corpus.py select                 # 40 readers x 5 items, references, REAL arm
python3 build_corpus.py resynth                # EnCodec 24 kHz @ 6 kbps round trip (CPU)
python3 clone_local.py                         # Chatterbox on an Apple-Silicon GPU (~1.7 h); modal_clone.py is the cloud alternative
python3 build_corpus.py freeze                 # loudnorm, padding, SHA-256 manifest (must match corpus/FROZEN.json)
python3 gen_mcq.py                             # needs OPENROUTER_API_KEY in ../.env
python3 runner.py --model google/gemini-3.6-flash
python3 runner.py --model google/gemini-3.6-flash --battery noise
python3 runner.py --model google/gemini-3.6-flash --battery stability
python3 runner.py --model google/gemini-3.1-pro-preview --subset pro --outcomes O2,O3,O4
python3 run_local.py --model voxtral --outcomes O2,O4 --items 1 --arms real,clone
python3 judge_o5.py
python3 analyze.py                             # -> results/analysis.json (every paper number)
cd ../figures && python3 build_figures.py && python3 build_gifs.py
cd ../paper/iclr && tectonic paper_iclr_submission.tex
```

Metered spend for the whole study: $2.99 (6,420 OpenRouter calls, exact per-call cost logged
in `results/spend.json`), plus about five hours of local compute.

## Layout

| path | contents |
|---|---|
| `experiments/` | corpus builder, local and Modal cloning, OpenRouter and local runners, MCQ generator, O5 judge, `analyze.py`, `prompts.py`, `cost_tracker.py` |
| `corpus/` | `items.json`, `mcq.json`, `manifest.csv`, `FROZEN.json` (audio regenerates) |
| `results/` | raw JSONL per model, `analysis.json`, judge output, audited samples, spend log |
| `figures/` | figure scripts (house style), teaser HTML, GIF builder |
| `paper/iclr/` | LaTeX dual build (anonymous + named), 45 verified references |
| `docs/` | project website (GitHub Pages), both PDFs, film, GIFs |
| `video/` | narration script (`tts.py`), film builder (`build_film.py`) |
| `lit_review/` | 96 verified references, novelty delineation; `candidate_toolcall/` holds the pre-empted first candidate |
| `EXPERIMENT_PLAN.md`, `MILESTONES.md` | frozen design, pre-registered directions, checkpoint log |
