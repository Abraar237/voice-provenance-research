# Synthetic-Voice Penalty · Milestones & Checkpoints

Project brief: MISSION.md. Budget cap: **$30 total** (hard stop $25). Update this file at
every checkpoint. The user authorised CP2-CP6 without stopping (2026-09-24); report at the end.

## Problem-statement history
- 2026-09-24 07:20 Candidate 1 (silent-wrong tool calls from spoken entities): CP1 done,
  verdict GO-WITH-REFRAME, half pre-empted by τ-Elicitation 2609.13602 and BFCL Audio
  (ICML 2026). User chose to switch. Archived in lit_review/candidate_toolcall/.
- 2026-09-24 08:40 Candidate 2 (spoken self-repairs executed as retracted values):
  pre-emption sweep ALIVE-BUT-CROWDED (Full-Duplex-Bench-v3 2604.04847, Audio2Tool
  2604.22821, Audio MultiChallenge 2512.14865). Not chosen.
- 2026-09-24 08:40 Candidate 3 (provenance bias, matched real-vs-clone): ALIVE, no paper
  holds speaker and content fixed with a resynthesis control and behavioural outcomes.
  CHOSEN. Repo renamed voice-provenance-research.

## Pre-registered directions (recorded BEFORE any clip was cloned or any model call made)
- [x] D1: At least one family's behavioural provenance delta (grading or comprehension,
      standardised) exceeds its explicit detection accuracy above chance.  Recorded: 2026-09-24
- [x] D2: The resynthesis control accounts for under half of the real-vs-clone delta.
      Recorded: 2026-09-24
- [x] D3: Sign differs by family: Gemini grades clones at or above real; open-weight models
      grade them below.  Recorded: 2026-09-24
- [x] D4: Explicit detection is near chance (<60%) for every family.  Recorded: 2026-09-24
- [x] D5: Transcription WER does not differ between real and clone beyond the noise floor.
      Recorded: 2026-09-24
- Note at registration: if clone quality is poor (high WER on CLONE), D5 fails for a
  mechanical reason and D1-D3 must be read conditional on intelligibility; we report that.

## CP1 · Lit review + pre-emption — DONE 2026-09-24 (for candidate 3)
- [x] Pre-emption sweep -> lit_review/candidate_provenance_preemption.md (verified
      abstracts, full-text reads of 2512.14865, 2608.06718, 2602.01030)
- [x] Verdict: ALIVE
- [x] Extended to 96 verified refs (angles F ALLM awareness, G TTS-stimulus audits,
      H cloning/perception/stakes) -> lit_review/lit_review.csv + LIT_REVIEW.md
      (16 of 21 audio-LLM bias audits use synthetic-only stimuli)

### Environment sanity (2026-09-24)
- OpenRouter: new key, $50 limit. google/gemini-3.6-flash and gemini-3.1-pro-preview accept
  audio input and return usage.cost. gpt-audio-mini, voxtral, qwen-omni are blocked by a
  workspace GUARDRAIL (not credit); user can lift at openrouter.ai/workspaces/default/guardrails
- Modal profile thesreedath OK; ffmpeg present; faster-whisper 1.2.1 installed (not needed now)
- GEMINI_API_KEY: not to be used for experiments (user instruction)

## CP2 · Experiment plan frozen — DONE 2026-09-24
- [x] EXPERIMENT_PLAN.md + site/plan.html; budget ~$9 of $30; cost_tracker.py armed ($25)
- [x] Design: 40 readers x 5 items, 4 arms (REAL/CLONE/RESYNTH/STOCK) + 50 clone-B, 5 outcomes,
      Flash full grid, Pro subset, open-weight local; batteries noise 30x5 + stability

## CP3 · Experiments + analysis — DONE 2026-09-24 (open-weight subset still running)
- [x] Corpus: 850 clips frozen, manifest sha 1bb7e14d4a3c664b. Cloning ran LOCALLY on the M4
      (Modal workspace spend limit exceeded): 450 clips in 103 min. EnCodec resynth local.
- [x] Gemini 3.6 Flash: 4,700 audio calls (800 clips x 5 outcomes + noise 300 + stability 100)
- [x] Gemini 3.1 Pro: 720 calls on the 60-item subset (a first pass of 720 returned empty
      text because reasoning consumed max_tokens; discarded, $0.18; rerun with headroom)
- [x] MCQ generation 200 text calls; O5 judge 800 text calls; hand audits 24 replies + 24 grades
- [x] analyze.py -> results/analysis.json; BH over 45 tests -> 2 survive (Flash grade
      RESYNTH-REAL, CLONE-RESYNTH)
- [ ] Voxtral-Mini-3B: MPS crashes (matmul), CPU bf16 ~65 s/call; reduced grid running
      (40 readers x 1 item x real/clone x O2,O4 = 160 calls). gpt-audio-mini / hosted Voxtral /
      Qwen-Omni blocked by OpenRouter workspace guardrail.
- Headline: CLONE-REAL grade +0.005 [-0.16,+0.16] (n=200); RESYNTH-REAL -0.31 (p=3.5e-4, BH);
  WER equal; MCQ at ceiling; probe balanced acc 0.555 with 74.5% of REAL called SYNTHETIC
  (Pro 90%); D1 implicit 0.50 vs explicit 0.555 -> not supported; D2 reversed; D4, D5 hold
- Spend: $2.99 metered

## CP4 · Paper — DRAFT 2026-09-24
- [x] ICLR dual build compiles (tectonic), 13 pages, 45 verified refs (45/45 OK), 4 figures
      (HTML->Chrome teaser + 3 matplotlib), appendix with prompts, deltas, batteries, audits, cost
- [ ] Fill open-weight placeholders once the Voxtral subset finishes

## CP5 · Publish — IN PROGRESS
- [x] docs/index.html drafted (script-bias aesthetic), 3 GIFs built
- [x] Narration generated (ElevenLabs Matilda, 10 of 11 cues; open-weight cue pending)
- [ ] Film render + QA; repo public; Pages

## CP6 · Self-review — PENDING

## Spend log
| Date | Item | Amount | Running total |
|---|---|---|---|
| 2026-09-24 | Smoke and probe calls for candidates 1-2 (direct Gemini x2, OpenRouter x11) | $0.01 | $0.01 |
| 2026-09-24 | MCQ generation (200 text calls) | $0.08 | $0.09 |
| 2026-09-24 | Flash grid 4,700 audio calls + O5 judge 800 text calls | $1.53 | $1.62 |
| 2026-09-24 | Pro subset 720 calls (+$0.18 discarded first pass) | $1.37 | $2.99 |
