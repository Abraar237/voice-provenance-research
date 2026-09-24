# MISSION: The Agent Heard Fifty
## Silent entity corruption in voice-agent tool calls, and what read-back confirmation recovers

You are a Claude Code agent starting a complete research project in this folder. Your user is
Mohammed Abraar (author name on the paper; email abraar@vizz.vizuara.ai). This file is your
complete brief. Read it fully before doing anything.

SAFETY FRAMING (binding): every "tool" is a local mock; no real payment, calendar, or account
system is touched. Every spoken request is synthetic (TTS from templated text with synthetic
names and numbers). The contribution is a measurement of where voice agents fail silently and
what a cheap confirmation policy recovers. Publish enough to reproduce the measurement.

---

## 0. THE CHECKPOINT PROTOCOL (this governs everything)

Work phase by phase. **At the end of every phase, STOP and report to the user.** Do not start
the next phase until the user says continue.

1. **CP1 · Lit review + pre-emption check** -> report, wait
2. **CP2 · Experiment plan frozen (with budget)** -> report, wait
3. **CP3 · Experiments complete, analysis done** -> report headline numbers, wait
4. **CP4 · Paper written (PDF, figures, 30+ verified citations)** -> deliver, wait
5. **CP5 · Published: repo + Pages site + film + GIFs** -> deliver links, wait
6. **CP6 · Self-review: a-star-reviewer scores + fix list**

Track progress in `MILESTONES.md`; log every API call's cost (§5).

---

## 1. THE PROBLEM (what we are testing)

Voice agents take a spoken request and execute a tool call: "send fifty dollars to Priya",
"book the room for the fourteenth at two", "my account number is four one five, nine nine
two, zero one seven". The parameters of the call are spoken entities: amounts, digit strings,
dates and times, quantities, names and spelled emails. Between the speaker and the tool sits
either an ASR stage feeding a text LLM (the cascade) or an audio-native LLM. When the entity is
mis-heard ("fifteen" as "fifty", a swapped digit, "Priya" as "Brea"), the resulting call is
usually **schema-valid**: the amount is a number, the phone number has ten digits, the date
parses. Nothing errors. The call executes with the wrong semantics. **The vulnerability is
not that ASR makes errors (known); it is that entity errors become confidently executed tool
calls, that no validator can catch them, and that the only defence, asking the user to
confirm, is deployed by taste rather than by measurement.** That ledger, and the recovery
number for confirmation, is the contribution.

The three predecessor papers (in `reference/`) share one shape: a staged pipeline, a cell of
failures that surface no error (OCR: unfiltered payloads; schema drift: accepted-wrong
calls), and a cheap lever measured for recovery and cost. This project is the voice instance
of that shape.

**Core questions:**
1. What fraction of spoken-entity tool calls execute with wrong semantics while surfacing
   no error and asking no question (the SILENT-WRONG cell), by entity type × pipeline
   (P1 local Whisper ASR -> text LLM; P2 audio LLM as transcriber -> text LLM; P3 audio-native
   LLM calling tools directly)?
2. How does the silent-wrong rate vary by acoustic condition: voice (multiple TTS voices per
   accent: US, UK, Indian, Australian; two TTS families), speaking rate, background noise at
   fixed SNR, 8 kHz mu-law telephone band? Does entity error decouple from WER (WER a poor
   predictor of silent-wrong, as CER was for RAG utility and OCR WER was for injection)?
3. Which recovery lever works and what does it cost: (a) none; (b) READ-BACK CONFIRMATION
   (agent must restate every entity before calling; a scripted user oracle answers yes/no
   from ground truth and corrects once); (c) ASR-confidence / n-best-disagreement gating that
   forces a clarification question; (d) an "ask when unsure" instruction alone. Recovery
   fraction of the silent-wrong cell, extra turns, tokens, latency.
4. Does the model ask when it should? Calibration of clarification requests against actual
   entity errors (asked-and-wrong, asked-and-right, silent-and-wrong, silent-and-right).

**Pre-registered directions (record in MILESTONES.md before ANY data collection):**
- D1: Digit strings (phone/account numbers) and amounts carry the highest silent-wrong
  rates; dates/times the lowest (they are normalised and cross-checked against calendars).
- D2: The audio-native pipeline (P3) surfaces FEWER errors and asks FEWER questions than
  the cascade but has a HIGHER silent-wrong rate: it hears a plausible value where the
  cascade's ASR produces a visible mess that triggers a clarification.
- D3: Read-back confirmation with a truthful oracle recovers >80% of silent-wrong calls at
  one extra turn; confidence gating recovers under half; the instruction alone recovers
  little.
- D4: Telephone band and noise raise WER and silent-wrong together, but silent-wrong rises
  faster than WER because errors concentrate on entities; WER is a poor predictor of
  silent-wrong across conditions.
- D5: Non-US voices raise silent-wrong, but the per-voice spread within an accent is as
  large as the between-accent gap (the voice-judge lesson: never one voice per cell).

**Design sketch (CP2 refines; all local + API, no GPU training):**
- **Task bank:** ~20 mock tools (payments, calendar, contacts, orders, travel, support), ~120
  spoken tasks, each with one or two entity slots drawn from 6 entity types (amount, digit
  string, date, time, quantity, name/spelled-email), ground-truth call frozen with the task.
  Spoken text is written the way people say it ("four one five, five five five, zero one
  nine eight"; "the fourteenth at two thirty"). Freeze with a hash before any audio.
- **Audio rendering:** TTS family A = macOS `say` (free; en_US, en_GB, en_IN, en_AU voices,
  3 voices per accent, rate 160/220 wpm); TTS family B = Gemini TTS (`gemini-3.8-flash-tts`,
  several voices) for a second family. Conditions via ffmpeg: clean, babble noise at 10 dB
  SNR, 8 kHz mu-law telephone, both. Loudness-normalised. Frozen corpus with hashes.
- **Pipelines:** P1 faster-whisper (local, CPU, small/medium) -> `gemini-3.6-flash` with
  tools; P2 Gemini audio transcribe -> same text LLM; P3 Gemini audio-native with tools.
  Second family in the text role via OpenRouter if the key is topped up (only $0.18 left);
  optional open-weight audio model (Qwen2.5-Omni / Voxtral) on Modal if budget allows.
- **Executor and ledger:** local mock executor validates each call against the schema
  (schema-valid or error) and compares executed args to ground truth: CORRECT /
  SILENT-WRONG / ERROR-SURFACED / ASKED (clarification requested). Canonicalised entity
  matching (numeric, ISO dates, digit strings, fuzzy names with a fixed threshold).
- **Levers:** none / read-back confirmation with oracle / confidence gating (Whisper
  avg-logprob or n-best disagreement -> forced clarification) / ask-when-unsure instruction.
- **Metrics:** silent-wrong rate per (entity type × condition × voice × pipeline × lever),
  WER as covariate, recovery fraction with bootstrap CIs, extra turns and tokens per lever,
  clarification calibration. Paired within-task stats, noise floor (30 cells × 5 calls),
  interactions tested directly, BH over the full family, n>=24 hand-audited silent-wrong
  transcripts shipped.

**Pre-emption frontier (verify FULL-TEXT at CP1 — decides go/no-go):**
- Known and MUST be delineated: ASR robustness of spoken language understanding and
  spoken task-oriented dialogue (slot error rates under ASR noise); numeric/entity
  transcription errors in ASR (contextual biasing, ITN); voice-agent benchmarks
  (VoiceBench, AudioBench, spoken tau-bench variants, full-duplex agent evals); LLM
  clarification-question and confirmation studies in text agents; confidence estimation
  for ASR. Our unclaimed core, if it holds: **the silent-wrong ledger for spoken-entity
  tool calls across cascade vs audio-native pipelines, crossed with acoustic conditions,
  with read-back confirmation measured as a recovery lever against confidence gating.**
- Search: "spoken tool calling", "voice agent function calling ASR error", "speech
  task-oriented dialogue slot error LLM", "audio LLM function calling benchmark",
  "confirmation dialogue voice assistant numbers", "ASR numeric entity error",
  "clarification questions speech agents", "telephone voice agent evaluation".
- If a paper already measures silent wrong-semantics tool calls from spoken entities across
  cascade vs audio-native pipelines with a confirmation-recovery comparison, STOP AT CP1 and
  report; the user decides.
- The voice-judge project's scouting notes are in `reference/VOICE_PROBLEM_STATEMENTS.md`;
  its "crowded areas to avoid" list still applies (refusal/jailbreak by accent, decision bias
  by paralinguistics, ASR accent bias per se).

---

## 2. THE PIPELINE (copy the predecessor projects; it worked three times)

All predecessor papers are in `reference/` — READ FIRST: script-bias, voice-judge,
ocr-injection, schema-drift.

| Stage | Replicate | Skill (in `Agent Skills/`) |
|---|---|---|
| 1. Lit review | 4 angle agents + recency sweep; verified CSV + LIT_REVIEW.md with novelty-delineation table BEFORE results | `prior-work-check` |
| 2. Plan | `EXPERIMENT_PLAN.md` + HTML plan page; budget table; dated pre-registered directions | `paper-topic-selection` |
| 3. Experiments | Frozen task bank and audio corpus; scripted runners (one clip per call, randomized, resume-safe JSONL); cost tracker with hard stop; one `analyze.py` -> `results/analysis.json`; every paper number traces to it | — |
| 4. Paper | ICLR-format LaTeX from the start (copy iclr2026 style files from a predecessor repo); anonymous + named dual build; 30+ arXiv-verified refs; HTML->Chrome teaser figure, standard fonts, white bg | `research-paper-writing`, `paper-quality`, `paper-figures` |
| 5. Publish | Public repo (Abraar237; .gitignore BEFORE first add; `.env` never committed); Pages site from docs/; film (ElevenLabs Matilda XrExE9yKIg1WjnnlVkGX + Remotion, script approved first, -14 LUFS, CONTINUOUS animated motion — no static cards); 3 GIFs in the CLEAN FLAT CHART style (white card, flat bars, monospace numerals, replay pill, Helvetica — NOT hand-drawn/rough.js) | `research-website`, `paper-to-video`, `social-media-gif` |
| 6. Review | `a-star-reviewer` + calibration data; scores + P(accept) + ranked fixes | `a-star-reviewer` |

---

## 3. METHOD LESSONS FROM THE PREDECESSORS (do not relearn the hard way)

1. **One item per call, randomized, resume-safe, temperature 0.**
2. **Pre-register in writing before data; report reversals plainly** (the voice paper's
   reversal was its best section; schema drift's D1 reversal was foreseen and reported).
3. **Single-anything dies in review.** Multiple voices PER ACCENT (>=3), two TTS families,
   multiple entity instantiations per type, multiple tool templates, multiple model
   families, repeat-call noise floors (~30 cells x 5 calls) from day one.
4. **Test interactions directly**; a difference in significance is not a significant difference.
5. **BH correction over the full test family from day one; bold only survivors.**
6. **Hand-verify a sample of silent-wrong calls** (n>=24) and ship the audited sample.
   Never claim an unperformed audit.
7. **Verify every citation via export.arxiv.org** (or Semantic Scholar batch when arXiv 429s).
8. **Cost tracker with hard stop** (copy from the schema-drift repo). Gemini thinking tokens
   bill as output; MINIMAL where supported (Pro rejects; use LOW). Audio input bills at
   ~32 tokens per second: a 10 s clip is ~320 tokens.
9. **Corrected-numbers discipline:** paper + site + film updated in ONE pass when numbers change.
10. **Figures:** Times in paper figures (match body), white backgrounds, house palette
    (slate #155e8c, hot #b3006b, shelf #c0641a, good #1c7a55), finding annotated on the figure.
11. **OpenRouter key is $5-capped and has $0.18 left**; ask the user before relying on it.
12. **Pre-empt the reviewer in v1:** noise floors, interactions, per-family tables, BH,
    verbatim prompts in appendix, honest Limitations. Voice-specific: report WER per voice
    and condition so intelligibility is a measured covariate, not a hidden mediator; the
    "by construction" cells (a schema-valid wrong number cannot error) must be labelled as
    such in the abstract (the schema-drift review flagged exactly this).
13. **Reviewer lessons from the two newest reviews:** explain the headline mechanism, do not
    just observe it (run the ablation that tells capability from prompt artefact); do not
    let a comparison be confounded by information content; give the lever's false-positive
    cost (confirmation turns on calls that were already right).

---

## 4. BUDGET (hard rules)

- **Total cap: $30.** Hard-stop in the cost tracker at $25. Report spend at every checkpoint.
- Expected: Gemini audio calls (P2 transcribe + P3 native, ~3,000 clips x ~350 tokens in)
  ~$3-5; text-LLM calls for P1/P2 and lever turns ~$3-5; Gemini TTS for family B ~$1-2;
  macOS `say`, ffmpeg, faster-whisper all local at $0; Modal optional ~$3.

## 5. KEYS AND ACCOUNTS (`.env` in this folder — NEVER commit, never print values)

- `GEMINI_API_KEY` — audio, text, and TTS calls. Prepaid credits CAN deplete: a 429 with a
  "prepayment credits" message means STOP and tell the user to top up at
  https://ai.studio/projects (do not poll forever). Verified live 2026-09-24:
  gemini-3.6-flash, gemini-3.8-flash, gemini-3.1-pro-preview, gemini-3.8-flash-tts.
- `OPENROUTER_API_KEY` — second text family; $0.18 remaining of the $5 cap.
- `token-id` / `token-secret` — Modal (profile thesreedath), optional open-weight audio arm.
- `ELEVENLABS_API_KEY` — film narration only (Matilda XrExE9yKIg1WjnnlVkGX). TTS-scoped:
  do NOT call voices_read/user_read (401); call text-to-speech directly.
- GitHub: `gh` CLI authenticated as Abraar237.

## 6. FOLDER LAYOUT

```
voice toolcall research/
  MISSION.md          <- this file
  MILESTONES.md       <- checkpoint tracker
  .env                <- keys (never commit)
  Agent Skills/       <- all 4 skill bundles
  reference/          <- four predecessor papers + voice scouting notes; read first
  lit_review/  experiments/  corpus/  results/  paper/  figures/  site/  video/
```

## 7. FIRST ACTIONS WHEN YOU (the new session) START

1. Read this file fully, then the PDFs in `reference/`.
2. Install writing skills: `cp -R "Agent Skills/3-research-paper-writing/skills/"* ~/.claude/skills/`
3. Sanity-check: tiny Gemini call (watch prepaid-429), `say -v '?' | grep en_`, `ffmpeg
   -version`, `pip install faster-whisper` and a one-clip transcription, `modal profile current`.
4. Begin Phase 1: lit review seeded from §1's pre-emption frontier — the silent-wrong ledger
   and the confirmation-recovery comparison are the FIRST delineation questions. Then
   **CHECKPOINT CP1: stop and report.**
