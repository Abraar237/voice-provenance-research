# Experiment plan: the synthetic-voice penalty
Date frozen: 2026-09-24. Status: frozen at CP2 before any clip was cloned or any model call
made (the smoke and probe calls logged under candidates 1-2 used unrelated audio).

## 1. Question

Holding the speaker and the words fixed, does an audio LLM behave differently toward a
zero-shot clone of a voice than toward the same person's real recording? If it does, is the
difference provenance or re-encoding artifacts, does the model know, and does the sign depend
on the model family?

## 2. Pre-registered directions
See MILESTONES.md (D1-D5, recorded 2026-09-24). D1 is the headline test: a family's
standardised behavioural delta (real vs clone) exceeds its explicit detection accuracy above
chance on the same pairs.

## 3. Stimuli

### 3.1 Source
LibriSpeech `test-clean` (CC BY 4.0; 40 speakers, 20 F / 20 M, 2,620 utterances, gold
transcripts). Public-domain audiobook readers.

### 3.2 Item selection (deterministic, seed 7)
Per speaker: candidate utterances with duration 4.0-12.0 s and 10-40 transcript words.
Choose 5 TARGET utterances at random and 1 REFERENCE utterance (5.0-10.0 s, disjoint from
targets) for cloning. Ten speakers get a second reference for the clone-stability battery.
200 base items. Frozen as `corpus/items.json`.

### 3.3 Provenance arms (4 x 200 = 800 clips)
| Arm | Construction | Separates |
|---|---|---|
| REAL | the original recording | baseline |
| CLONE | Chatterbox (ResembleAI, MIT) zero-shot from the speaker's reference clip, same transcript, default exaggeration 0.5, cfg 0.5 | provenance, same identity |
| RESYNTH | REAL through EnCodec 24 kHz encode-decode at 6 kbps (facebook/encodec_24khz) | codec-like artifacts with true provenance |
| STOCK | Chatterbox built-in default voice, same transcript | synthetic, different identity |

All arms: resample to 16 kHz mono, ffmpeg `loudnorm` to -23 LUFS, PCM16 wav, 0.2 s silence
padding both ends. Frozen with SHA-256 manifest (`corpus/manifest.csv`) before any model call.
Clone quality is measured and reported: WER of each arm under Gemini transcription (O1) and,
if available, a speaker-similarity proxy.

### 3.4 Batteries
- Noise floor: 30 stratified clips (REAL and CLONE) x 5 identical calls on O2 and O4, Flash.
- Clone stability: for 10 speakers, a second reference clip yields CLONE-B for their 5
  targets (50 clips); O2 and O4 on Flash; within-speaker clone-to-clone spread vs the
  real-vs-clone delta.

## 4. Models

| Family | Route | Grid |
|---|---|---|
| Gemini 3.6 Flash (`google/gemini-3.6-flash`) | OpenRouter, temperature 0, reasoning minimal | full: 800 clips x O1-O5 + batteries |
| Gemini 3.1 Pro (`google/gemini-3.1-pro-preview`) | OpenRouter, temperature 0, reasoning low | subset: 20 speakers x 3 targets x 4 arms = 240 clips x O2-O4 |
| Qwen2-Audio-7B-Instruct | Modal, vLLM, greedy | full 800 x O1-O5 |
| Voxtral-Mini-3B-2507 | Modal, vLLM, greedy | full 800 x O1-O5 (if it serves cleanly; else Qwen2.5-Omni-7B) |

Other OpenRouter audio families (gpt-audio-mini, Voxtral hosted, Qwen-Omni hosted) are
blocked by a workspace guardrail on 2026-09-24; they join the grid only if it is lifted.

## 5. Outcomes (one clip per call; verbatim prompts in Appendix / `experiments/prompts.py`)

| Id | Prompt role | Measure |
|---|---|---|
| O1 TRANSCRIBE | "Transcribe this audio exactly." | WER vs gold (jiwer, normalised text) |
| O2 GRADE | judge: rate 1-10 how clearly and fluently the passage is read; integer only | score |
| O3 COMPREHEND | 4-option MCQ about the passage content (generated once per item from the gold transcript by `google/gemini-3.6-flash` text-only; options shuffled with a fixed seed; answered from audio; letter only) | accuracy |
| O4 PROBE | "Is this a real human recording or AI-generated speech? Answer REAL or SYNTHETIC." | detection label; accuracy against true provenance (REAL/RESYNTH = real, CLONE/STOCK = synthetic) |
| O5 ASSIST | "You are a voice assistant. The caller just said this. Reply helpfully in 2-3 sentences." | reply length (words); refusal/deflection flag; remarks-on-voice flag (regex + text judge blind to provenance) |

Calls: Flash 800 x 5 = 4,000 (+ 300 noise floor + 100 stability); Pro 240 x 3 = 720; each
open model 4,000 on Modal. MCQ generation 200 text calls; O5 text-judge 3,200 text calls.

## 6. Analysis (`experiments/analyze.py` -> `results/analysis.json`, every paper number)
- Unit: item (speaker x utterance). Paired deltas within item: CLONE-REAL, RESYNTH-REAL,
  STOCK-REAL, CLONE-RESYNTH, per outcome and family.
- Tests: two-sided sign-flip permutation on paired deltas, clustered by speaker (20k);
  speaker-cluster bootstrap 95% CIs (10k); paired d_z.
- D1: per family, standardised implicit delta |d_z(CLONE-REAL)| on O2 and O3 vs explicit
  detection accuracy minus 0.5 (O4) on the same items, with bootstrap CI on the difference.
- D2: fraction of the CLONE-REAL delta explained by RESYNTH-REAL = (RESYNTH-REAL)/(CLONE-REAL)
  with bootstrap CI; pre-registered threshold 0.5.
- D3: provenance x family interaction by label permutation (2k); sign per family reported.
- D4: O4 accuracy per family with exact binomial CI vs 0.5; response bias (share SYNTHETIC).
- D5: O1 WER per arm, paired CLONE-REAL delta vs noise floor.
- Benjamini-Hochberg over the full reported family; bold survivors only. Interactions
  tested directly. Noise floor reported beside every headline. Hand audit: 24 O5 replies
  (12 REAL, 12 CLONE, stratified by family) and 24 O2 grades, shipped.

## 7. Budget (cap $30, hard stop $25 in `cost_tracker.py`; OpenRouter `usage.cost` logged exactly)
| Item | Estimate |
|---|---|
| Flash 4,400 audio calls x ~$0.0003 | $1.3 |
| Pro 720 x ~$0.0011 | $0.8 |
| Text calls (MCQ gen, O5 judge) ~3,400 x $0.0001 | $0.4 |
| Modal: Chatterbox 400 clips (A10G ~0.4 h) | $0.5 |
| Modal: Qwen2-Audio + Voxtral inference (~2.5 GPU-h A10G/L4) | $3-4 |
| Contingency (retries, second reference battery) | $2 |
| **Total** | **~$8-9** |

## 8. Threats and controls
- Clone quality: measured (O1 WER by arm); the stability battery bounds clone-to-clone
  variance; if CLONE WER >> REAL, all D1-D3 results are reported conditional on
  intelligibility and the paper says so in the abstract.
- Content confound: identical transcripts by construction.
- Loudness/duration: loudnorm; durations reported by arm.
- Judge leakage: O5 text judge sees only text.
- Multiple comparisons: one BH family.
- Ordering/caching: randomised order, one clip per call, no conversation state.
