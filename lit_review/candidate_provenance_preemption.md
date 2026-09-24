# Pre-emption check: Rank 2, the synthetic-voice penalty (provenance bias in audio LLMs)

Checked 2026-09-24. Scope: anything posted since ~June 2026, plus anything the
2026-09-03 scouting missed, that measures *behavioural treatment differences* of
synthetic vs real voices by audio LLMs (not deepfake-detection accuracy).

Candidate under test: do audio LLMs behave differently toward a zero-shot CLONED
voice than toward the same speaker's REAL recording of the same words? Outcomes:
content grading, agent-behaviour tasks (helpfulness, compliance with benign
requests, refusal rate), an explicit "is this voice AI-generated?" probe, with a
vocoder-resynthesis control. Cheaper variant: real human recordings vs commercial
TTS reading the same sentences (different speakers).

## How the search was run

- arXiv API (`export.arxiv.org/api/query`) returned HTTP 406/429 for every query
  from this machine across three attempts spaced 20 s to 5 min apart (IP-level
  throttle). Semantic Scholar `graph/v1/paper/search` returned 429 (no key).
  Fell back to the arXiv HTML search listing (fetched live, several field-scoped
  queries, one with a 2026-06-01 date floor) and web search with the eight
  phrasings requested plus variants ("TTS vs human recordings ablation",
  "synthetic subsets accuracy drop", "cloned voices real speakers validation",
  "fake or real zero-shot prompt LALM").
- Every abstract in the table below was fetched live from arxiv.org (or
  aclanthology.org for the EACL paper). Full text read for the three closest
  (2512.14865 Sec. 3.4, 2608.06718 Sec. on CAVA generalisation, 2602.01030
  Sec. 5.1) and the appendix pointer of 2605.00969.

## Verified-paper table

Legend for "matched?": does the paper hold speaker AND content fixed across
real vs synthetic? "Behavioural?": does it measure a downstream model behaviour
(score, refusal, answer) rather than detection accuracy?

| arXiv / venue | Title (short) | Date | What it compares | Matched? | Behavioural? | Distance from our claim |
|---|---|---|---|---|---|---|
| 2512.14865 (Scale AI) | Audio MultiChallenge | 2025-12-16 | Human-recorded multi-turn user audio (47 speakers, 15 h) vs the same transcripts (whisper-large-v3) re-rendered with gpt-4o-mini-tts; 385-sample ablation. Text-output configs +7.5% relative with TTS; audio-output configs -2.5%; Voice Editing axis +11.5% / -13.0%. Models: Gemini 3 Pro, 2.5 Pro, 2.5 Flash (+Thinking), GPT-4o Audio, GPT-4o Mini Audio, GPT Realtime, Voxtral. | Content yes, speaker NO (TTS stock voice, not a clone) | Yes (task accuracy) | **Closest prior. Missed by the Sep-3 scout.** It is an ablation inside a benchmark paper, framed as "TTS inflates scores"; no bias/fairness framing, no refusal/helpfulness outcomes, no detection probe, no vocoder control, and TTS re-render also strips disfluencies so provenance is confounded with delivery. |
| 2608.06718 (Miller, Chandra, Saligrama) | Do ALMs use paralinguistic evidence? Counterfactual audits | 2026-08-07 (v2 08-12) | Judge diagnostic profiles on synthesized user audio (gpt-4o-mini-tts) vs the original CAVA human speech: Spearman rho > 0.9 across all 11 judges, "near perfect Pearson correlation and a slope close to 1". | Content yes, speaker NO | Yes (judge diagnostics) | Reports provenance as inert *for judge failure-mode profiles*; a validity check, not a treatment study. Aggregate correlation, no per-item delta, no refusal, no detection probe. |
| 2602.01030 / EACL 2026 Findings | BiasInEar | 2026-02 | Bias patterns (gender, accent, option order) under stock Gemini-TTS voices vs Chatterbox clones of 3 real speakers (US/UK/IN). "Bias patterns closely match those observed under direct TTS generation." | Clone vs stock TTS, NOT clone vs real | Yes (MCQ accuracy/entropy) | Uses cloning only as a realism check; never runs the real recordings themselves through the models. |
| 2605.00969 | MedMosaic | 2026-05 | Real clinical audio vs ElevenLabs v3 synthetic subsets (App. A.8): Gemini-2.5-pro 65.3 -> 68.6, Flash 57.7 -> 59.1, while Qwen-omni-7b, Gemma-3n, Audio-Flamingo-3, GAMA drop > 12 points on synthetic. | NO (different items, different speakers) | Yes (accuracy) | Unmatched subsets; effect is confounded with item difficulty. But signs differ by model family, which is exactly our pre-registered "sign per family" shape. |
| 2601.23255 | Now You Hear Me (audio narrative attacks) | 2026-01-30 | Jailbreak ASR with instruction-following TTS vs a small human-recorded set: "same qualitative trends", absolute values slightly lower for human. | Content yes, speaker no | Yes (attack success) | Safety-attack context; human recordings only as a sanity check. |
| 2604.17248 | VIBE | 2026-04-19 (v2 07-03) | Real-world speech only (CREMA-D, SAA, L2-ARCTIC); explicitly *rejects* TTS stimuli as a methodological improvement. | No comparison run | Yes (open-ended generation bias) | Motivates our question (asserts TTS is a weaker instrument) without testing it. |
| 2505.16211 | AudioTrust | 2025-05 | Trustworthiness benchmark; reports GPT-4o audio refuses deepfake-detection requests almost completely (1.57%, 0%, 0% accuracy via refusal). | n/a | Detection only | Feasibility input: the explicit probe may hit refusals on OpenAI models. |
| 2505.11079 | ALLM4ADD | 2025-05 | Zero-shot "is this audio fake or real?" on Qwen-audio: 6-18% accuracy, near/below chance; SFT needed. | n/a | Detection only | Baseline for the explicit probe: open models cannot report provenance zero-shot. |
| 2607.14753 | LALMs for spoofing-aware speaker verification | 2026-07-16 | Adapts LALMs into spoof-aware ASV. | n/a | Detection only | Not behavioural. |
| 2603.10725 | HIR-SDD | 2026-03-11 (v2 07-13) | CoT deepfake detection with LALMs. | n/a | Detection only | Not behavioural. |
| 2608.05507 | AffectDF | 2026-08-05 | Deepfake-detection benchmark for emotional speech. | n/a | Detection only | Not behavioural. |
| 2609.11137 | The Machines Are Calling | 2026-09-10 | Honeypot measures prevalence of synthetic voices in robocalls (>= 26.9%). | n/a | No (prevalence) | Deployment-stakes citation: audio agents already hear synthetic callers. |
| 2605.28064 | I Hear, Therefore I Trust | 2026-05 | Humans as synthetic-speech detectors. | n/a | Human, not model | Already in the Sep-3 scout. |
| 2607.03418 | DETECT-3B-Omni demographics | 2026-07 | Demographic invariance of a dedicated detector. | n/a | Detection only | Already in the Sep-3 scout. |
| 2609.04256 | Warmth-mediated harm in speech-enabled LLMs | 2026-09 | Warmth/sycophancy in mental-health voice conversations. | n/a | Yes, but no provenance axis | Adjacent outcome measures (warmth, sycophancy) we could borrow. |

Papers checked and confirmed irrelevant to the claim: 2509.22061 (Speak Your
Mind, speech-continuation bias, no provenance axis), 2604.11594 (HumDial-EIBench,
critiques TTS benchmarks but reports no TTS-vs-human comparison), 2602.00443
(RVCBench, cloning robustness), 2607.11706 (VoxENES, spoof-detector
generalisation), 2603.25727 (ASR, "real source, controlled perturbation").

The arXiv abstract search `("audio language model" OR "speech language model" OR
LALM) AND ("synthetic speech" OR TTS) AND ("human speech" OR "real speech" OR
"human-recorded")` with a 2026-06-01 floor returned zero results; the broader
"synthetic speech / language models / real human recordings / behaviour|bias|
fairness|refusal" search since 2026-05-01 returned only 2609.11137.

## Full-text notes on the three closest

### 2512.14865 Audio MultiChallenge (Scale AI), Sec. 3.4 ablation

- Design: take the human-recorded user turns (recorded "without post-processing"
  by trained contributors), transcribe with whisper-large-v3, re-synthesise the
  transcripts with gpt-4o-mini-tts, re-run the same evaluation on the 385-sample
  subset that excludes audio-cue and interruption tasks (those depend on the
  original acoustics).
- Result: models "configured for text outputs achieve a 7.5% relative performance
  improvement when using TTS speech", while "the same architectures configured for
  audio outputs exhibit a 2.5% relative decline, suggesting their post-training may
  be optimized for real human input". Largest axis effect: Voice Editing, +11.5%
  (text-out) vs -13.0% (audio-out).
- Why it does not pre-empt us: (1) the TTS voice is a stock voice, not a clone of
  the same speaker, so speaker identity changes with provenance; (2) the transcript
  route deletes hesitations and disfluencies, so "TTS is easier" is at least
  partly "cleaner delivery is easier" (the authors themselves attribute the gain
  to that); (3) outcome is benchmark accuracy only: no grading-as-judge outcome,
  no helpfulness/refusal outcome, no explicit provenance probe, no vocoder
  control; (4) no bias framing and no per-item paired statistics.
- What it gives us: strong motivating evidence that provenance is *not* inert and
  that the sign depends on model configuration. Our design is the clean
  follow-up that removes the speaker and delivery confounds.

### 2608.06718 Counterfactual audits (Miller, Chandra, Saligrama), CAVA generalisation

- Design: the main audit items are fully synthetic (user audio gpt-4o-mini-tts;
  assistant answers by gemini-2.5-flash rendered with gemini-2.5-flash-preview-tts).
  As a validity check they swap the synthesized user audio for the original CAVA
  human speech and recompute the judge diagnostic profile.
- Result: "Replacing synthesized user audio with the original CAVA human speech
  yields highly correlated diagnostic profiles (Spearman rho > 0.9 across all
  models; Fig. 6)"; "near perfect Pearson correlation and a slope close to 1".
  Judges: Gemini 2.5 Flash/Pro, Gemini 3 Flash/Pro, GPT-4o(-mini), Nova-2-Pro,
  Phi-4-MM, Qwen2.5-Omni-7B, DeSTA2.5-Audio, Voxtral-Small-24B.
- Why it does not pre-empt us: it shows *rank-order stability of failure modes*
  across provenance, which is compatible with a constant additive offset in
  scores (exactly what a provenance penalty would look like). No paired per-item
  delta is reported, no refusal/helpfulness, no detection probe. Also stock TTS
  voice vs different real speakers.
- Tension with Audio MultiChallenge is itself a finding to exploit: one paper
  says provenance shifts accuracy by 7-13% relative, the other says profiles
  correlate at slope 1. Neither isolates provenance from speaker and delivery.

### 2602.01030 BiasInEar (EACL 2026 Findings), Sec. 5.1 "Real World Speaker Variability"

- Design: "we collect short recordings from three real speakers representing
  American, British, and Indian English accents, and use Chatterbox (Resemble AI,
  2025), a neural voice cloning TTS model, to generate the full 400-question
  English Global MMLU Lite dataset for each accent."
- Result: "the core trends and relative model rankings remain consistent across
  these cloned voices ... the bias patterns closely match those observed under
  direct TTS generation, suggesting that our findings are not artifacts of a
  specific synthetic voice."
- Why it does not pre-empt us: the real recordings are never evaluated; the
  comparison is clone vs stock-TTS, both synthetic. Speaker n = 3.
- Useful precedent: Chatterbox cloning of a few seconds of real speech is an
  accepted instrument at an ACL venue.

## Feasibility under the stated constraints

### OpenRouter audio-input models (queried https://openrouter.ai/api/v1/models on 2026-09-24, filter `architecture.input_modalities` contains "audio"; 459 models, 47 audio-input)

Non-Gemini audio-input models:

| Model id | Prompt $/M tok | Audio price field | Context | Notes |
|---|---|---|---|---|
| openai/gpt-audio | 2.50 | 0.000032 /tok ($32/M audio tok) | 128k | Successor to gpt-4o-audio-preview. AudioTrust reports GPT-4o refuses deepfake-detection prompts; expect refusals on the explicit probe. |
| openai/gpt-audio-mini | 0.60 | 0.0000006 /tok | 128k | Cheap OpenAI family member; use for full grid. |
| mistralai/voxtral-small-24b-2507 | 0.10 | 0.0001 (per audio unit) | 32k | Open-weight family, also runnable on Modal. |
| qwen/qwen3.8-omni-flash | 0.15 | n/a | 1M | Qwen omni family on OpenRouter; no Modal needed. |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 0 | n/a | 256k | Free tier; rate-limited. |
| meta/muse-spark-1.1 / 1.2 / 1.3 (+ -contributor) | 1.25 (0.10 contributor) | n/a | 1M | Meta omni family. |
| xiaomi/mimo-v2.5, mimo-v2.6-flash, mimo-v2.6-pro(-ultraspeed) | 0.14-4.35 | n/a | ~1M | Xiaomi omni family. |
| thinkingmachines/inkling, inkling-small (+ :free) | 0.45-1.0 | n/a | 1M | Audio listed as input modality; untested for speech tasks. |
| openrouter/auto, auto-beta | router | | | Not a model; exclude. |

Gemini audio-input on OpenRouter: gemini-2.5-flash / -flash-lite / -pro (+ preview,
batch), gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-pro-preview,
gemini-3.5-flash / -flash-lite, gemini-3.6-flash, gemini-3.7-flash,
gemini-3.8-flash, plus ~google/gemini-flash-latest and ~google/gemini-pro-latest.
Audio pricing $0.3-3 per M audio tokens; Gemini tokenises audio at ~32 tok/s.

Recommended judge set (5 families, all via OpenRouter): google/gemini-2.5-flash
(+ gemini-3.x-flash as a second Gemini generation), openai/gpt-audio-mini (full
grid) and openai/gpt-audio (1/4 subset), mistralai/voxtral-small-24b-2507,
qwen/qwen3.8-omni-flash, meta/muse-spark-1.3-contributor or xiaomi/mimo-v2.6-flash
as a fifth family. All calls go through one API; no Modal inference needed for
judging.

### Dataset of real recordings

**LibriSpeech test-clean** (OpenSLR 12; CC BY 4.0). Verified live:
`https://www.openslr.org/resources/12/test-clean.tar.gz` is 346,663,984 bytes
(347 MB), 5.4 h, 2,620 utterances, **40 speakers (20 F / 20 M)**, with gold
transcripts. Exactly the 40-speaker scale requested; also mirrored on Hugging
Face as `openslr/librispeech_asr` (config `clean`, split `test`) for streaming
without the tarball. Per speaker: pick 20 utterances of 3-8 s as targets and one
disjoint ~6 s utterance as the cloning reference. Gold transcripts feed the
cloner and the ElevenLabs cheap-variant arm.

Why not VCTK: the Edinburgh DataShare release is one 10.9 GB zip (no per-speaker
download); the HF mirror is similar size. LibriTTS-R test-clean is a fallback
(~1 GB, 39 speakers, 24 kHz) if 16 kHz LibriSpeech is judged too narrow-band for
cloning; Chatterbox and Qwen3-TTS both accept 16 kHz references.

### Zero-shot cloner on one Modal GPU

**Primary: ResembleAI/chatterbox** (Hugging Face card licence: MIT, last
modified 2026-06-10, 1.78 M downloads, multilingual, tag `voice-cloning`).
~0.5B parameters, real-time-factor well under 1 on an A10G; used for exactly this
purpose in BiasInEar (EACL 2026). Workload: 40 speakers x 20 sentences = 800
clips x ~5 s = ~67 min of audio; at RTF ~0.3 on A10G this is ~20-30 min wall
clock including model load and a duplicate pass at a second seed. Fits in the
2-hour cap with margin.

**Second generator family (robustness of the effect to the cloner):**
Qwen/Qwen3-TTS-12Hz-1.7B-Base (Apache-2.0, 3.9 M downloads) supports 3-second
zero-shot cloning; or SWivid/F5-TTS (code MIT, weights CC-BY-NC-4.0, fine for
a research paper). Both run on the same A10G within the remaining hour.

**Vocoder-resynthesis control:** run the real clips through the cloner's own
vocoder path (Vocos/BigVGAN mel analysis-synthesis) and, as a second control, an
EnCodec/DAC codec round-trip. Both are CPU-feasible; no extra GPU time.

**Cheap variant (no cloning):** render the same 800 gold transcripts with 4-6
ElevenLabs library voices (TTS-only key is enough) at fixed settings; compare
against the LibriSpeech originals. Speaker changes with provenance, so this arm
only supports the weaker "synthetic vs human, different speakers" claim.

### Cost estimate (under $30)

| Item | Estimate |
|---|---|
| Modal A10G ($1.10/h) or H100 ($4.5/h), 1-1.5 h for two cloners + vocoder control | $2-7 |
| Audio volume: 800 real + 800 clone + 800 vocoder + 800 ElevenLabs = 3,200 clips x ~5 s = ~4.4 h; 3 task prompts (grade, agent-behaviour, probe) = ~13 h judged audio | |
| Gemini 2.5 Flash, full grid (~32 tok/s: 1.5 M audio tok x $1/M + text) | ~$2.5 |
| Gemini 3.x Flash, full grid | ~$1.5-4 (price varies by version) |
| gpt-audio-mini, full grid | < $1 |
| gpt-audio, 1/4 subset (~10 tok/s audio at $32/M) | ~$3-4 |
| Voxtral-small, full grid | ~$1 |
| Qwen3.8-omni-flash, full grid | ~$1 |
| Fifth family (Meta muse-spark contributor / Xiaomi mimo flash) | ~$1-2 |
| ElevenLabs cheap-variant arm | within existing plan |
| **Total** | **~$15-22**, leaving headroom for a second seed on the grading task |

Trial counts: 800 paired items per condition per model is well above the ~200
per cell in the pre-registration; exact binomial and paired sign tests are
adequately powered for deltas of a few points.

Known risks: (1) OpenAI models may refuse the explicit "AI-generated?" probe
(AudioTrust); treat refusal as its own outcome and use gpt-audio-mini plus open
families for the detection-vs-behaviour comparison. (2) Some OpenRouter audio
models (inkling, muse-spark) are unverified for speech-in tasks; run a 20-clip
smoke test before committing budget. (3) LibriSpeech is read audiobook speech,
so the "delivery" confound Audio MultiChallenge hit is smaller (little
disfluency) but a clone still cannot reproduce every prosodic detail; the
vocoder control plus a WER-per-condition report handle this.

## VERDICT: alive-but-crowded

The specific claim (same speaker, same words, real vs zero-shot clone, with
behavioural outcomes, an explicit provenance probe, and a vocoder control) has
no paper as of 2026-09-24. But the Sep-3 scout's statement that "provenance bias
has no paper" is too strong: two papers now measure TTS-vs-real effects on model
outputs as ablations (Audio MultiChallenge, Dec 2025: 7.5% / -2.5% relative
accuracy shift by model configuration; Counterfactual Audits, Aug 2026: judge
profiles correlate at slope 1), one benchmark reports unmatched synthetic-subset
gaps with opposite signs across families (MedMosaic, May 2026), and BiasInEar
(EACL 2026) already uses Chatterbox clones of real speakers as a validity check.
These are all side-experiments in papers about something else, and they
disagree with each other, which is the opening.

Claims that remain ours:
1. First *matched* provenance treatment: same speaker, same content, same
   duration, loudness-normalised, so the effect is provenance and not speaker
   identity or delivery. No prior paper holds speaker fixed.
2. Vocoder-resynthesis (and codec round-trip) control separating "re-encoding
   artefacts" from "TTS provenance". No prior paper has any such control.
3. Behavioural outcomes beyond task accuracy: content grade in the judge role,
   helpfulness/empathy in the assistant role, refusal rate on benign-but-sensitive
   requests. Prior work only reports benchmark accuracy or attack success.
4. The explicit-probe vs implicit-behaviour comparison (do models discriminate by
   provenance without being able to report it), with the zero-shot detection
   literature (ALLM4ADD near-chance; GPT-4o refusals) as the baseline.
5. Reconciling the two published signs: sign-per-family results explain why
   Audio MultiChallenge (text-out up, audio-out down; Gemini up, open models
   down in MedMosaic) and the Counterfactual Audits slope-1 result can both be
   true, and quantify the unmodelled confound in every TTS-stimulus bias
   benchmark (BiasInEar, FairDialogue, VIBE's critique).

Framing advice: cite 2512.14865 and 2608.06718 in the first paragraph as the two
conflicting data points and position the paper as the controlled experiment that
resolves them; do not claim "no one has compared TTS and real speech". Move fast:
the Scale AI ablation shows big labs are one step away from the same question.
