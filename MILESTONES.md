# Voice Tool-Call Silent-Error Audit · Milestones & Checkpoints

Project brief: MISSION.md. Budget cap: **$30 total** (hard stop $25). Update this file at
every checkpoint. RULE: at each CP, STOP and report to the user; wait for approval.

## Pre-registered directions (recorded BEFORE any task-bank generation or data collection)
- [x] D1: Digit strings and amounts carry the highest silent-wrong rates; dates/times the
      lowest.  Recorded: 2026-09-24
- [x] D2: Audio-native pipeline (P3) surfaces fewer errors and asks fewer questions than the
      cascade but has a HIGHER silent-wrong rate.  Recorded: 2026-09-24
- [x] D3: Read-back confirmation with a truthful oracle recovers >80% of silent-wrong at one
      extra turn; confidence gating recovers under half; instruction alone recovers little.
      Recorded: 2026-09-24
- [x] D4: Telephone band and noise raise silent-wrong faster than WER; WER is a poor
      predictor of silent-wrong across conditions.  Recorded: 2026-09-24
- [x] D5: Non-US voices raise silent-wrong, but within-accent per-voice spread is as large as
      the between-accent gap.  Recorded: 2026-09-24
- Note at registration: D2 may reverse if the audio-native model is simply a better
  listener than small local Whisper; if so we report that as a reversal and add the
  Whisper model size as a factor.

## CP1 · Lit review + pre-emption — IN PROGRESS 2026-09-24
- [ ] Angle agents (A spoken tool calling / voice-agent benchmarks, B ASR entity errors and
      SLU slot robustness, C confirmation / clarification / confidence gating, D audio-native
      vs cascade, E recency sweep 2026) -> lit_review/lit_review.csv (verified ids)
- [ ] Full-text pre-emption reads on the nearest neighbours -> lit_review/preemption_fulltext.md
- [ ] LIT_REVIEW.md with novelty-delineation table + significance statement
- [ ] Verdict
- [ ] **REPORTED TO USER, APPROVAL RECEIVED: ____**

### Environment sanity (2026-09-24)
- Gemini key OK; models live: gemini-3.6-flash, gemini-3.8-flash, gemini-3.1-pro-preview,
  gemini-3.8-flash-tts
- OpenRouter: new key (2026-09-24), $50 limit; ALL model calls incl. Gemini go through it
  (user instruction); verified audio + tool call via OpenRouter, $0.00035, cost returned per call
- Modal profile thesreedath OK
- macOS `say`: 186 voices incl. en_US/en_GB/en_IN/en_AU; ffmpeg present; faster-whisper 1.2.1
  installed (small/int8 on CPU: 2.2 s per clip)
- End-to-end smoke test 2026-09-24: say -> 16 kHz wav -> (a) Whisper transcript, (b) Gemini
  3.6 Flash audio-native with a send_payment tool declaration; both correct on clean US voice
  and on 8 kHz mu-law telephone band; ~290 tokens in per 8 s clip. Repeated through
  OpenRouter (google/gemini-3.6-flash, input_audio + tools): identical correct call

## CP2 · Experiment plan frozen — PENDING
## CP3 · Experiments + analysis — PENDING
## CP4 · Paper — PENDING
## CP5 · Publish — PENDING
## CP6 · Self-review — PENDING

## Spend log
| Date | Item | Amount | Running total |
|---|---|---|---|
| 2026-09-24 | 2 direct Gemini smoke calls (before the OpenRouter rule) + 1 OpenRouter smoke call | <$0.01 | $0.01 |
