# Literature Review — Silent-wrong tool calls from spoken entities in voice agents
## Where mis-heard entities go silent, and what catching them costs

Date: 2026-09-24. Method: five parallel search angles (A spoken tool calling and voice-agent
benchmarks, B ASR entity errors and SLU robustness, C confirmation / clarification /
confidence-gating levers, D cascade vs audio-native, E recency sweep Jan–Sep 2026) over arXiv,
Semantic Scholar and Google Scholar, followed by FULL-TEXT reads of the seven nearest
neighbours (`preemption_fulltext.md`). 121 unique verified ids, every abstract fetched live
(`lit_review.csv`; the arXiv export API rate-limited this host all day, so verification went
through the Semantic Scholar batch endpoint and arxiv.org/abs pages, recorded per angle file).
Angle files: `angle_A_spoken_toolcalling.md` … `angle_E_recency.md`.

---

## Verdict: GO-WITH-REFRAME

No paper meets the MISSION stop condition (silent wrong-semantics tool calls from spoken
entities across cascade vs audio-native pipelines with a confirmation-recovery comparison).
But two papers, both from the last four months, each own half of the original pitch:

- **τ-Elicitation (arXiv 2609.13602, posted 2026-09-11, two weeks ago)** owns the
  read-back-confirmation recovery headline for audio-native realtime agents: a
  spell/read-back/confirm/correct scaffold lifts robust exact success by 14–31 points at
  21–28 s per call; agents verify wrong captures barely more often than correct ones
  (66/64% vs 50/50%); only 24–37% of verified errors get repaired. It has no ASR or
  cascade arm, no confidence gating, no telephone band, no WER covariate, no amounts, and
  its task is an elicitation loop where the caller can be asked to spell.
- **BFCL Audio (ICML 2026, no arXiv id)** owns the two-suite cascade-vs-native benchmark
  under controlled noise, with a failure taxonomy that names our cell ("valid but incorrect
  function call"; "the model never asks for confirmation") but reports only failure
  shares: no per-entity or per-condition rate, no telephone band, WER used as a sanity
  check only, no recovery lever.

The residual is real but narrower than the original pitch. The area has produced four
converging papers in five months (τ-Elicitation, BFCL Audio, From Text to Voice, SpeechGym).
Speed matters, and the title phrase "what read-back confirmation recovers" must go:
τ-Elicitation owns it.

---

## Novelty delineation (what is known vs what is ours)

We want to be clear about what is already known. That ASR mis-hears numbers and names, and
that those errors propagate into slots, is not ours (angle B: a decade of SLU robustness
work; VoiceCodeBench 2608.28916 shows system-level WER correlates at only ρ ≈ −0.28 with
entity recovery). That audio-induced tool-calling failures sit mostly in argument values
rather than call structure is not ours either (From Text to Voice 2605.15104: 39–57% of
paired failures; SpeechGym 2608.26432: 32% of speech rollouts vs 2% text; BFCL Audio).
That read-back confirmation repairs spoken-entity capture for audio-native agents, at a
measured time cost, is τ-Elicitation's. What is new here is the executed, schema-checked
silent-wrong RATE, on identical clips across three pipelines, crossed with telephone band
and fixed-SNR noise, with WER as a per-cell covariate, and a head-to-head of the levers
including the one the cascade uniquely affords (confidence gating) and the bill each runs
up on calls that were already right.

| Closest neighbour (full-text read) | What it established | What it does NOT cover (ours) |
|---|---|---|
| τ-Elicitation (2609.13602, Sep 2026) | 200 elicitation tasks, 10 entity types, 5 ElevenLabs voices, 3 environments; audio-native realtime agents reach 0.14–0.41 robust exact success; read-back scaffold +14–31 Pass³ at 21–28 s/call; asked-vs-silent calibration 66/64% vs 50/50% | No ASR/cascade or transcriber arm; no confidence/n-best gating (cannot: no ASR); no telephone band or rate; no WER covariate; no amounts or quantities; elicitation loop with a spelling oracle, not single-utterance commands; one voice per caller, no accent design; no schema step, no error-surfaced class; no false-positive cost of confirmation |
| BFCL Audio (ICML 2026) | Pipelined (3 ASRs) vs end-to-end suites, same model both roles; controlled noise types; AST argument grading; taxonomy with FM3 "valid but incorrect function call" and FM6 "never asks for confirmation" | Failure shares only, no silent-wrong rate per entity type or per condition; no telephone band; 225 voice clones but no accent/rate breakdown; WER declined as covariate; no recovery lever (ask-when-unsure prompt held constant); calls graded unexecuted |
| From Text to Voice (2605.15104) | Cascade (GPT-4o-Transcribe) vs direct voice on Confetti/When2Call, 7 omni models; argument-value errors 39–57% of paired failures | Clean audio only in the paired comparison; one ASR; no silent/asked split; no entity-type ledger; no lever; no telephone band or rate |
| SpeechGym (2608.26432) | Audio-native RL gym on τ²-bench; mis-heard slot values in 32% of speech rollouts vs 2% text | Wrong keys error out (surfaced, not silent); no pipeline axis; no lever ablation; no acoustic grid |
| VoiceCodeBench (2608.28916) | 19 ASR systems; WER vs entity recovery ρ ≈ −0.28; numeric entities easiest (93.7%) | ASR only, no LLM, no tool call, no noise, no lever |
| MTVA-Bench (2609.20152) | Mock backend executes the arguments a cascaded LM sends; argument values are the main gap | Text only; ASR damage simulated and steered away from the caller's known values; wrong arguments become failures, not silent successes; no lever |
| Proactive for Uncertainty (2605.25404) | Cause-aware error detectors drive clarification in a cascade, beating entropy-based confidence gating at matched FPR | Transcript-level, no tool calls or entities; no read-back arm; the confidence-gating baseline we reuse |

**Ours alone (verified against all seven full texts):**
1. The four-way ledger (correct / silent-wrong / error-surfaced / asked) as a per-task
   RATE on executed, schema-validated mock tools, by entity type, including amounts and
   quantities.
2. The same clips through three pipelines: Whisper cascade, audio-LLM-as-transcriber
   cascade (P2, absent everywhere), audio-native. Silent-wrong and ask-rate per pipeline.
3. 8 kHz mu-law telephone band and fixed-SNR babble crossed with pipeline (telephone band
   is absent from all seven papers).
4. WER measured per cell and set against silent-wrong within a pipeline across conditions:
   the decoupling curve.
5. Confidence / n-best gating as a lever on tool-call arguments, head-to-head with read-back
   and instruction-only, on recovery fraction AND the false-positive bill (confirmations
   spent on already-correct calls, extra turns, tokens).
6. The single-utterance command regime ("send fifty dollars to Priya") where the agent
   must decide to read back before executing, with multiple voices per accent from two
   TTS families so D5 is testable.

---

## Significance

**Who is affected.** Anyone deploying a voice agent that executes actions from spoken
parameters: payment and banking IVRs, booking and scheduling agents, order-taking, support
lines that update account details. Every one of them runs either a cascade or an
audio-native model, and most run over the telephone band.

**What changes.** (1) The silent-wrong rate, not WER, is the number to monitor and to put
in a vendor comparison; we give the first per-entity, per-condition table and show how
poorly WER tracks it. (2) Cascades expose a confidence signal that audio-native models do
not; if gating recovers a meaningful share at a fraction of read-back's turn cost, the
architecture choice carries a safety lever with it. (3) Read-back is not free: we price the
confirmations spent on calls that were already correct, which τ-Elicitation's time cost
does not separate, so a practitioner can set the policy per entity type rather than by
taste.

---

## Reframing this forces (proposed for CP2; needs user approval)

**Working title:** "Same Clip, Three Ears: Where Spoken-Entity Errors Go Silent in Voice
Tool Calls, and What Catching Them Costs."

**Headline order:** (A) the same-clip three-pipeline silent-wrong ledger with the WER
decoupling curve, telephone band and noise; (B) read-back vs confidence gating vs
instruction with recovery fraction and false-positive bill; (C) D2, "the cascade asks, the
native model executes", as the headline finding inside A if it holds and a reported
reversal if it does not.

**Pre-registration amendments (before any data; recorded in MILESTONES.md with reason):**
- D1 as written is contradicted on the digit half by two published results (phones are
  the second-easiest entity in τ-Elicitation; numeric entities easiest in VoiceCodeBench).
  Re-register D1 as a conditional test: in single-utterance commands where the caller
  cannot be asked to spell, and for amounts (untested anywhere), do digit strings and
  amounts still carry the highest silent-wrong rate? Either outcome is reportable.
- D3 keeps its gating-vs-read-back half (novel) and drops the bare read-back recovery
  number from the headline (a replication of τ-Elicitation in a cascade, reported as such).

**Must be cited in the abstract or first page:** τ-Elicitation, BFCL Audio, From Text to
Voice, SpeechGym.

---

## Angle summaries

| Angle | Verified | Closest | Verdict |
|---|---|---|---|
| A spoken tool calling / voice-agent benchmarks | 41 | τ-Elicitation, BFCL Audio, From Text to Voice | Not pre-empted; each axis owned separately, none combined |
| B ASR entity errors, SLU robustness, WER decoupling | 30 | From Text to Voice, MTVA-Bench, Proactive for Uncertainty | Not pre-empted; components established separately |
| C confirmation / clarification / gating levers | 33 | Proactive for Uncertainty, From Text to Voice, Ambig-DS | Not pre-empted; levers studied in isolation, mostly in text |
| D cascade vs audio-native, audio-LLM entity behaviour | 30 | From Text to Voice, VoiceAgentBench, MTVA-Bench | Not pre-empted; no silent ledger, no lever comparison |
| E recency sweep 2026 | 30 | τ-Elicitation (EXACT-NICHE on the lever axis) | Partially pre-empted; residual defensible but narrow |

Open items before CP2: full read of Audio2Tool (2604.22821) for its cascade-vs-SpeechLM
numbers under noise; confirm SFC-Bench (2608.05126) has no confirmation arm.
