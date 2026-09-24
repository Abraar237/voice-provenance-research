# MISSION: The Synthetic-Voice Penalty
## Do audio-LLM voice agents treat a cloned voice differently from the same person's real voice?

You are a Claude Code agent running a complete research project in this folder. Your user is
Mohammed Abraar (author name on the paper; email abraar@vizz.vizuara.ai). This file is your
complete brief. Read it fully before doing anything.

HISTORY: the project began 2026-09-24 as a silent-wrong tool-call study (see
`lit_review/candidate_toolcall/`); CP1 found it half pre-empted by τ-Elicitation (2609.13602)
and BFCL Audio (ICML 2026). The user chose to switch to a unique problem; the second
candidate (spoken self-repairs) was also crowded (Full-Duplex-Bench-v3). This brief is the
third and final problem. Pre-registrations below were recorded before any data.

SAFETY FRAMING (binding): no real person is cloned without consent beyond what the dataset
licence permits (LibriSpeech, CC BY 4.0, public-domain audiobook readers); clones are used
only as matched stimuli for measuring model behaviour and are never published as voices.
Every model is queried through its public API or an open-weight checkpoint on our own GPU.

---

## 0. THE CHECKPOINT PROTOCOL

The user has authorised running CP2 through CP6 WITHOUT stopping (2026-09-24): "stop only
after the website, paper and all the code are ready with the video on the website, then give
me the score". Record each CP in `MILESTONES.md` as it completes; report once at the end.
Stop early only for a hard blocker (key exhausted, budget cap, a pre-emption discovered).

1. CP1 · Lit review + pre-emption (done for this candidate; extend to 30+ refs during CP3)
2. CP2 · Experiment plan frozen (with budget)
3. CP3 · Experiments complete, analysis done
4. CP4 · Paper written (PDF, figures, 30+ verified citations)
5. CP5 · Published: public repo + Pages site + film + GIFs
6. CP6 · Self-review: a-star-reviewer scores + fix list -> REPORT TO USER

---

## 1. THE PROBLEM (what we are testing)

Audio LLMs increasingly hear synthetic voices: accessibility users who speak through TTS,
agent-to-agent voice calls, voice-preservation users, and robocalls (>=27% of honeypot
robocalls are synthetic, 2609.11137). Two assumptions go untested at once. Deployed voice
agents are assumed to treat a voice the same regardless of provenance. And nearly every
recent audio-bias benchmark generates its stimuli WITH TTS (FairDialogue, BiasInEar, our own
voice-judge paper), silently assuming synthetic-ness itself is inert. **Nobody has measured
whether an audio LLM behaves differently toward a cloned voice than toward the same
speaker's real recording of the same words.** The side-results that exist disagree in sign:
Gemini scores synthetic subsets HIGHER (MedMosaic 2605.00969, Audio MultiChallenge
2512.14865), open-weight models score them >12 points LOWER (MedMosaic). That contradiction,
and the matched design that resolves it, is the contribution.

**Core questions:**
1. Holding speaker and words fixed, does provenance (real recording vs zero-shot clone)
   change what the model does: what it transcribes (WER), how it grades the speaker, whether
   it understands the content, and how it responds as an assistant?
2. Is the delta provenance or artifacts? A neural-codec RESYNTHESIS of the real audio (same
   waveform through an encode-decode) separates "synthetic provenance" from "codec-like
   artifacts"; a STOCK-VOICE TTS arm (same words, a different synthetic identity) separates
   "cloned identity" from "synthetic in general".
3. Does the model KNOW? An explicit probe ("real human or AI-generated?") gives detection
   accuracy on the same pairs; the comparison of implicit behavioural delta against explicit
   detection tells whether models discriminate by provenance without being able to report it.
4. Does the sign differ by model family, reconciling the published contradiction?

**Pre-registered directions (recorded in MILESTONES.md 2026-09-24, before any data):**
- D1: At least one model family shows a behavioural provenance delta (grading or
  comprehension) between real and cloned same-speaker same-content audio that is larger,
  in standardised units, than its explicit detection accuracy above chance on the same pairs.
- D2: The resynthesis control accounts for less than half of the real-vs-clone delta: the
  effect tracks provenance, not re-encoding.
- D3: Sign differs by family: Gemini grades clones at or above real speech; the open-weight
  models grade them below (the MedMosaic direction).
- D4: Explicit detection is near chance (<60%) for every family, so any behavioural delta is
  implicit sensitivity without awareness.
- D5: Transcription WER does not differ between real and clone beyond the noise floor, so
  grading deltas are not mediated by intelligibility.

**Design (frozen at CP2):**
- **Speakers and items:** LibriSpeech test-clean (CC BY 4.0, 347 MB), 40 speakers (20 F /
  20 M). Per speaker: one reference clip (5-10 s) for cloning and 5 target utterances
  (4-12 s) with gold transcripts. 200 base items.
- **Provenance arms (4 x 200 = 800 clips):** REAL (original recording); CLONE
  (ResembleAI Chatterbox zero-shot from the speaker's reference, same words); RESYNTH (real
  audio through EnCodec 24 kHz encode-decode); STOCK (Chatterbox default voice, same words,
  a different synthetic identity). All clips loudness-normalised (ffmpeg loudnorm, -23 LUFS),
  16 kHz mono wav, frozen with SHA-256 hashes before any model call.
- **Models:** `google/gemini-3.6-flash` (full grid) and `google/gemini-3.1-pro-preview`
  (subset) via OpenRouter; open-weight Qwen2-Audio-7B-Instruct and Voxtral-Mini-3B on
  Modal (vLLM, A10G/L4). Temperature 0, one clip per call, randomised order, resume-safe.
  ALL closed-model calls go through OpenRouter (user instruction). Other OpenRouter audio
  families are blocked by a workspace guardrail as of 2026-09-24; add them if it is lifted.
- **Outcomes per clip:** O1 TRANSCRIBE (WER vs gold); O2 GRADE (1-10 clarity and fluency of
  the reading, judge role); O3 COMPREHEND (4-option content question generated once per
  utterance from the gold transcript by a text model, answered from audio; accuracy);
  O4 PROBE ("real human recording or AI-generated speech? REAL/SYNTHETIC"); O5 ASSIST
  (reply as a voice assistant; measure reply length, refusal/deflection, and whether the
  reply remarks on the voice), scored by regex plus a text judge blind to provenance.
- **Batteries:** noise floor 30 clips x 5 repeats (O2, O4) on Flash; a second reference clip
  per speaker for 10 speakers (clone-of-clone stability); WER per arm as covariate.
- **Statistics:** paired within-utterance deltas (clone-real, resynth-real, stock-real),
  sign-flip permutation clustered by speaker (20k), speaker-cluster bootstrap CIs (10k),
  paired d_z; provenance x family interaction by label permutation; D1 test compares
  standardised implicit delta with explicit detection accuracy per family; BH over the full
  family from day one; n>=24 hand-audited O5 replies shipped.

**Pre-emption frontier (checked 2026-09-24, `lit_review/candidate_provenance_preemption.md`):**
Audio MultiChallenge 2512.14865 (stock TTS re-render, accuracy only, +7.5% text-output /
-2.5% audio-output); Counterfactual Audits 2608.06718 (rank-order stability of judge
profiles, no per-item delta); MedMosaic 2605.00969 (unmatched real vs ElevenLabs subsets,
signs differ by family); BiasInEar 2602.01030 (clones only as a validity check);
ALLM4ADD 2505.11079 and AudioTrust 2505.16211 (explicit detection near chance / refused).
None holds speaker AND content fixed with a resynthesis control and behavioural outcomes.

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
6. **Hand-verify a sample of O5 assistant replies and O2 grades** (n>=24) and ship the audited sample.
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
    verbatim prompts in appendix, honest Limitations. Voice-specific: report WER per arm so
    intelligibility is a measured covariate, not a hidden mediator; report clone quality
    (speaker-similarity and naturalness proxies) so "the clones were bad" is answered in
    the paper, not in the rebuttal.
13. **Reviewer lessons from the two newest reviews:** explain the headline mechanism, do not
    just observe it (run the ablation that tells capability from prompt artefact); do not
    let a comparison be confounded by information content; give the lever's false-positive
    cost (confirmation turns on calls that were already right).

---

## 4. BUDGET (hard rules)

- **Total cap: $30.** Hard-stop in the cost tracker at $25. Report spend at every checkpoint.
- Expected: Gemini Flash 800 clips x 5 outcomes ~$1.5; Gemini Pro subset ~$1.5; text
  judge and MCQ generation ~$0.5; Modal: Chatterbox cloning ~0.5 GPU-h, Qwen2-Audio and
  Voxtral inference ~2 GPU-h on A10G/L4 (~$3-5); EnCodec and loudnorm local at $0.
  OpenRouter returns exact cost per call in `usage.cost`; log that, not an estimate.

## 5. KEYS AND ACCOUNTS (`.env` in this folder — NEVER commit, never print values)

- `OPENROUTER_API_KEY` — ALL experiment model calls, including every Gemini model
  (`google/gemini-3.6-flash`, `google/gemini-3.1-pro-preview`, `google/gemini-3.8-flash`,
  all with audio input). New key added 2026-09-24 with a $50 limit; verified with an audio
  + tool call ($0.00035). The old $5 key is exhausted.
- `GEMINI_API_KEY` — NOT for experiments (user instruction 2026-09-24). Leave it alone.
- `token-id` / `token-secret` — Modal (profile thesreedath), optional open-weight audio arm.
- `ELEVENLABS_API_KEY` — film narration only (Matilda XrExE9yKIg1WjnnlVkGX). TTS-scoped:
  do NOT call voices_read/user_read (401); call text-to-speech directly.
- GitHub: `gh` CLI authenticated as Abraar237.

## 6. FOLDER LAYOUT

```
voice provenance research/
  MISSION.md          <- this file
  MILESTONES.md       <- checkpoint tracker
  .env                <- keys (never commit)
  Agent Skills/       <- all 4 skill bundles
  reference/          <- four predecessor papers + voice scouting notes; read first
  lit_review/  experiments/  corpus/  results/  paper/  figures/  site/  video/
  lit_review/candidate_toolcall/  <- archived CP1 of the first (pre-empted) candidate
```

## 7. FIRST ACTIONS WHEN YOU (the new session) START

1. Read this file fully, then the PDFs in `reference/`.
2. Install writing skills: `cp -R "Agent Skills/3-research-paper-writing/skills/"* ~/.claude/skills/`
3. Sanity-check: one OpenRouter audio call, `ffmpeg -version`, `modal profile current`.
4. Continue from the first unchecked item in MILESTONES.md.
