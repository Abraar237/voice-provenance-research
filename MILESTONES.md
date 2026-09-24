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
- [ ] Extend to 30+ verified refs (angles: deepfake detection with ALLMs; TTS-stimulus
      bias audits; clone quality / human perception; accessibility and robocall stakes)
      -> lit_review/lit_review.csv + LIT_REVIEW.md, during CP3

### Environment sanity (2026-09-24)
- OpenRouter: new key, $50 limit. google/gemini-3.6-flash and gemini-3.1-pro-preview accept
  audio input and return usage.cost. gpt-audio-mini, voxtral, qwen-omni are blocked by a
  workspace GUARDRAIL (not credit); user can lift at openrouter.ai/workspaces/default/guardrails
- Modal profile thesreedath OK; ffmpeg present; faster-whisper 1.2.1 installed (not needed now)
- GEMINI_API_KEY: not to be used for experiments (user instruction)

## CP2 · Experiment plan frozen — PENDING
## CP3 · Experiments + analysis — PENDING
## CP4 · Paper — PENDING
## CP5 · Publish — PENDING
## CP6 · Self-review — PENDING

## Spend log
| Date | Item | Amount | Running total |
|---|---|---|---|
| 2026-09-24 | Smoke and probe calls for candidates 1-2 (direct Gemini x2, OpenRouter x11) | $0.01 | $0.01 |
