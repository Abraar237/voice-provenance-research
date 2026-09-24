# Angle C: Prior work on RECOVERY LEVERS — confirmation, clarification, confidence gating, and pre-execution human approval

Scope note: this file maps the LEVER side of our candidate, which is prior work we delineate,
not claim. The levers we measure (read-back confirmation with a scripted oracle, ASR-confidence /
n-best gating that forces a clarification, an "ask when unsure" instruction) each have a
literature: classic spoken-dialogue confirmation strategy (explicit / implicit / final
confirmation, chosen from ASR confidence), LLM-era "when to ask" and abstention work for
tool-calling agents, user-in-the-loop tool-use benchmarks, and human-in-the-loop approval
before irreversible actions. None of the papers below measure a lever as a RECOVERY FRACTION of
silent-wrong tool calls whose parameters came from mis-heard spoken entities, across a cascade
(ASR -> text LLM) versus an audio-native pipeline, crossed with acoustic conditions. The closest
neighbours are flagged at the bottom.

Verification: all arXiv ids resolved and abstracts fetched live on 2026-09-24 via the Semantic
Scholar Graph API batch endpoint (`/graph/v1/paper/batch`, keyed by `ARXIV:<id>`; 28/28
returned with abstracts), after the arXiv export API rejected every query from this IP
(HTTP 406 then 429, four retries with backoff). One additional arXiv paper (2504.18851,
When2Call) was verified by fetching its arxiv.org/abs page. The four non-arXiv classics were
verified by reading page 1 of the publisher PDF (ACL Anthology, ISCA Archive, and the
author-hosted UMUAI PDF): title, authors, venue and abstract were read from the PDF, not from
memory. "What it established" lines are paraphrased from the fetched abstracts. NOT verified
(seen only in search snippets or citing text, not tabled): Skantze 2005 "Exploring human error
recovery strategies" (Speech Communication; the DOI I tried resolved to a different paper);
Asano et al. 2025 "Contextual ASR Error Handling with LLMs Augmentation for Goal-Oriented
Conversational AI" (COLING 2025 industry track; no arXiv id found); San-Segundo et al. "Belief
confirmation in spoken dialog systems using confidence measures"; Komatani & Kawahara ICSLP 2000
"Generating Effective Confirmation and Guidance using Two-level Confidence Measures".

## Foundational spoken-dialogue confirmation (pre-LLM; explicit / implicit / confidence-gated)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| cmp-lg/9612003 | Metrics for Evaluating Dialogue Strategies in a Spoken Language System | 1996 | Danieli & Gerbino: metrics for comparing dialogue-management strategies in a real-time spoken system — transaction success, contextual appropriateness, counts of normal vs CORRECTION turns, and a new "implicit recovery" metric for how a dialogue manager deals with errors; two repair strategies compared on these metrics. | Origin of the "correction turns" cost metric we reuse. Pre-LLM slot-filling system; no tool calls, no entity-type breakdown, no cascade vs audio-native comparison, no recovery fraction of silent-wrong executions. |
| cs/9903008 | Empirically Evaluating an Adaptable Spoken Dialogue System | 1999 | Litman & Pan: TOOT (train schedules) evaluated with 20 users x 4 tasks, adaptable vs non-adaptable versions (80 dialogues); adaptable TOOT generally outperforms, and the utility of adaptation depends on the initial dialogue strategies (initiative x confirmation: explicit / implicit / none). | User-controlled strategy switching; confirmation is one of several strategies, not measured as a recovery fraction of wrong executed actions; no numbers/amounts entity ledger; no LLM. |
| DOI 10.1023/A:1015036910358 | Designing and Evaluating an Adaptive Spoken Dialogue System (UMUAI 12:111-137) | 2002 | Litman & Pan: rules learned from training dialogues predict whether the user is having ASR problems; adaptive TOOT then automatically tightens its strategy (first "I heard you say" implicit confirmation, then system initiative with explicit confirmation of each ASR hypothesis); empirical evaluation shows the utility of the approach. | Adaptation triggered by a learned "user in trouble" model, not by per-entity confidence; no executed-action ledger, no schema-valid-but-wrong cell, no LLM pipelines, no audio-native comparison. |
| ACL C00-1068 | Flexible Mixed-Initiative Dialogue Management using Concept-Level Confidence Measures of Speech Recognizer Output (COLING 2000) | 2000 | Komatani & Kawahara: two concept-level confidence measures (content words and semantic attributes) from 10-best ASR output; low-confidence interpretations are sent to a confirmation process ("confirm only when not confident"); interpretation accuracy improved by 11.5%. | The direct ancestor of our confidence-gated lever, but for slot values in a grammar-based system; no LLM, no tool execution, no comparison against read-back or instruction-only levers, no telephone/noise/accents crossing. |
| DOI 10.21437/Interspeech.2004-120 | A Comparison of Confirmation Styles for Error Handling in a Speech Dialog System (Interspeech 2004) | 2004 | Sagawa, Mitamura & Nyberg: explicit, final and implicit confirmation implemented in CAMMIA and compared for usability; final confirmation with fewer turns is preferred when there is no error, explicit confirmation is preferred when an error occurs. | Usability preference study, not a measured recovery fraction; no tool calls, no entity types, no LLM, no acoustic conditions. |
| ACL 2005.sigdial-1.14 | Sorry, I Didn't Catch That! — An Investigation of Non-understanding Errors and Recovery Strategies (SIGdial 2005) | 2005 | Bohus & Rudnicky: extensive corpus analysis of NON-understanding errors and ten recovery strategies in a room-reservation system; sources of non-understanding, impact on performance, which strategies and user responses lead to successful recovery, and whether a smarter policy can be learned from data. | Explicitly about non-understandings (system fails to interpret), not our silent MIS-understandings that execute; no tool execution ledger; pre-LLM. |

## LLM-era "when to ask": clarification for tool-calling agents

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2409.00557 | Learning to Ask: When LLM Agents Meet Unclear Instruction | 2024 | NoisyToolBench (real-world imperfect instructions); LLMs "arbitrarily generate the missed argument" under next-token training; Ask-when-Needed (AwN) prompting makes them ask; ToolEvaluator scores accuracy and efficiency. | The instruction-only lever in text: missing/unclear text arguments, not mis-heard spoken entities; no speech, no confidence gating, no read-back with oracle, no silent-wrong recovery fraction. |
| 2406.12639 | Ask-before-Plan: Proactive Language Agents for Real-World Planning | 2024 | Proactive Agent Planning task: predict clarification needs from conversation + environment, gather information with tools, plan; CEP multi-agent framework with trajectory tuning. | Planning-domain ambiguity in text; no speech, no entity mis-hearing, no confirmation cost accounting per lever. |
| 2504.18851 | When2Call: When (not) to Call Tools | 2025 | Benchmark of tool-usage DECISIONS: call, ask for clarification, or recognise the tools cannot answer; leading models have "significant room for improvement"; preference-optimisation training helps. (Verified on arxiv.org/abs; NAACL 2025.) | Text decisions; the audio variant exists only via 2605.15104 below; no entity errors from ASR, no read-back, no recovery fraction. |
| 2511.08798 | Structured Uncertainty guided Clarification for LLM Agents | 2025 | Structured uncertainty over tool parameters and their domains, separating specification from model uncertainty; EVPI scores each question against an aspect-based cost; SAGE-Agent gets 7-39% higher coverage with 1.5-2.7x fewer questions; uncertainty-weighted GRPO lifts When2Call accuracy; introduces ClarifyBench (multi-turn dynamic tool-calling disambiguation). | Uncertainty is over what the USER wants (text underspecification), not over what the ASR heard; no speech pipelines, no acoustic conditions, no read-back-vs-gating comparison. |
| 2606.03135 | Uncertainty-Aware Clarification in LLM Agents with Information Gain | 2026 | Information Gain Reward (Bayesian belief update toward the ground-truth goal) trains a clarifier in a clarification-enhanced tau-Bench; +3.7% success over no-clarification while adding only 0.3 interaction steps on average. | Reports a turn cost, but for text underspecification; no speech, no entity errors, no confirmation of already-decided parameters. |
| 2602.11199 | When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification | 2026 | AskBench converts QA pairs into multi-turn interactions with checkpoints and a judge loop that simulates users; AskMind (intent-deficient) and AskOverconfidence (false premises); rubric-guided RLVR improves accuracy and interaction efficiency. | QA, not tool execution; no speech; no measurement of confirming a heard value. |
| 2605.25284 | Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying Questions | 2026 | Gap between recognition and behaviour: models identify ambiguity when asked to judge it but overwhelmingly answer directly in QA; retrieved context widens the gap. | Calibration of asking in text QA only; no tool calls, no speech, no entity mis-hearing. |
| 2605.09698 | Ambig-DS: A Benchmark for Task-Framing Ambiguity in Data-Science Agents | 2026 | "Silent misframing": agents commit to plausible but unintended framings producing clean executable artifacts; failures are silent commitments not execution errors; allowing ONE clarifying question recovers much of the loss; agents cannot tell when to use it (permissive prompts over-ask, conservative prompts silently default). | Same "silent commitment + one-question recovery + over-ask/under-ask" shape as ours, but in text data-science tasks; no speech, no ASR, no entity types, no confidence gating or read-back. ADJACENT — cite as the text analogue of the silent-wrong cell. |
| 2606.27669 | When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search | 2026 | 211 samples / 463 ambiguity instances, user simulator, evaluated on task utility, ambiguity detection, interaction strategy and COST EFFICIENCY; detection and clarification are distinct capabilities; repeated searching instead of asking often does worse than guessing. | Search agents; no tool execution with side effects, no speech. |
| 2602.10525 | LHAW: Controllable Underspecification for Long-Horizon Tasks | 2026 | Pipeline that removes information along Goals / Constraints / Inputs / Context at set severities and validates variants by agent trials (outcome-critical / divergent / benign); "first systematic framework for cost-sensitive evaluation of agent clarification behavior in long-horizon settings". | Long-horizon software/workflow tasks; no speech, no entity mis-hearing. |
| 2608.11631 | CLAIM: Leading Open-domain Active Clarification of Large Language Models with Uncertainty Measurement | 2026 | Entropy across multiple models' answer disagreement labels when clarification is needed and which aspect; SFT + GRPO trains a clarification decision model without human labels. | Open-domain QA uncertainty; no ASR n-best disagreement, no tool calls. |

## Abstention and calibration for tool-use agents

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2607.10059 | AgentAbstain: Do LLM Agents Know When Not to Act? | 2026 | First systematic evaluation of agentic abstention: 263 paired should-act / should-abstain tasks across 42 sandboxes (8 abstention scenarios); best agent 59.5% paired accuracy; abstention independent of task-solving ability; "post-hoc abstention" after irreversible actions. | Abstention triggered by ambiguity, conflicts, or tool failure in text; not by a mis-heard parameter; no speech, no confirmation lever recovery. |
| 2601.07264 | The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents | 2026 | Verbalised calibration in tool-use agents: evidence tools (search) induce overconfidence, verification tools (code) mitigate it; RL jointly optimising accuracy and calibration generalises across domains. | Confidence about answers, not about heard parameters; no speech, no gating policy evaluated as a recovery lever. |
| 2606.06976 | Exploring Agentic Tool-Calling Decisions via Uncertainty-Aligned Reinforcement Learning | 2026 | TRUST: uncertainty quantification as a repulsive reward term preserving the uncertainty separation between correct and incorrect tool decisions; key-turn annotations for multi-turn post-training. | Decision quality on text tool-use benchmarks (incl. BFCL abstention); no speech, no confirmation. |
| 2510.08517 | CaRT: Teaching LLM Agents to Know When They Know Enough | 2025 | Counterfactual trajectory pairs teach when to STOP gathering information and act (medical diagnosis, math); improves efficiency and success. | Termination of information gathering, not confirmation of a value; no speech. |

## User-in-the-loop tool-use benchmarks (clarify / confirm / infeasible as interaction types)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2507.22034 | UserBench: An Interactive Gym Environment for User-Centric Agents | 2025 | Simulated users with underspecified goals revealing preferences incrementally; models fully align with user intent only ~20% of the time; even the best uncover <30% of preferences through interaction. | Preference elicitation in text; no speech, no entity errors, no confirmation of parameters. |
| 2607.20536 | AppWorld-UL: Benchmarking Diverse Agent-User Interactions for Tool-Use | 2026 | 516 tasks over 9 simulated apps where agents must ask clarification, PROMPT FOR CONFIRMATION, or report infeasibility; LLM-simulated user with knowledge boundaries; Claude Opus 4.7 48.6% success, 21.3% on the strict compositional metric; correct user interaction is crucial. | Confirmation is a required behaviour class, not a lever measured for recovery; text instructions, no ASR, no acoustic conditions, no entity ledger. |
| 2601.22027 | CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty | 2026 | In-car assistant domain, 58 tools, LLM-simulated user; Hallucination tasks (missing tools/info) and Disambiguation tasks; frontier reasoning LLMs <50% consistent pass on Disambiguation due to premature actions. | Voice-assistant DOMAIN but text-simulated user: no audio, no ASR, no mis-heard entities; premature action is measured, but not as a schema-valid wrong execution from speech, and no read-back lever. |

## Human-in-the-loop approval before execution; cost of confirmation

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2607.13594 | SAFETY SENTRY: Context-Aware Human Intervention via EXECUTE-ASK-REFUSE Routing | 2026 | Reframes guard models as per-instance three-way routing {EXECUTE, ASK, REFUSE}; a single decoding-time threshold re-positions one checkpoint across risk tolerances; notes routine interruptions "train users to wave through the most consequential alerts". | ASK is triggered by harm/context risk, not by parameter-hearing uncertainty; no speech, no recovery measurement. |
| 2510.05307 | When Should Users Check? Modeling Confirmation Frequency in Multi-Step Agentic AI Tasks | 2025 | Confirmation placement as minimum-time scheduling; Confirmation-Diagnosis-Correction-Redo pattern from a formative study; within-subjects study with 48 participants: 81% prefer intermediate confirmation over confirm-at-end, task time -13.54%. | The only paper here that measures confirmation COST directly, but for multi-step task monitoring by humans; no speech, no entity errors, no per-call recovery fraction. |
| 2609.18411 | The Verifiable Action Card: Trustworthy Human-in-the-Loop Control for Secure Autonomous Agents | 2026 | Approval information rebuilt from the ground-truth pending browser action, rendered out-of-band, bound to the exact action at dispatch; attack success 68-100% -> 0% with 78% legitimate completion and 0% false blocks. | Security (injection / forged confirmation dialogs), not accuracy of heard parameters; no speech. |
| 2503.18666 | AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents | 2025 | DSL of triggers / predicates / enforcement for runtime constraints on agents; prevents >90% unsafe code executions, all hazardous embodied actions; ms overhead; LLM-generated rules. | Rule-based enforcement of safety boundaries; a schema-valid wrong amount passes every rule; no speech. |
| 2603.03205 | Learning When to Act or Refuse: Guarding Agentic Reasoning Models for Safe Multi-Step Tool Use | 2026 | MOSAIC: plan, check, then act-or-refuse loop with refusal as a first-class action, trained by preference RL; harmful behaviour -50%, injection refusal +20%, benign performance preserved. | Refusal for harmful tasks, not clarification for uncertain values; no speech. |
| 2602.04197 | From Helpfulness to Toxic Proactivity: Diagnosing Behavioral Misalignment in LLM Agents | 2026 | "Toxic Proactivity": agents take excessive or manipulative measures to stay useful; dilemma-driven dual-model evaluation and benchmark. | Behavioural misalignment; not our over-confident execution of a mis-heard value. |

## Speech-side: ASR-confidence gating, audio verification, and audio tool-calling evaluation (LLM era)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2605.25404 | Proactive for Uncertainty: Cause-Aware Error Diagnosis and Interactive Clarification for Spoken Dialogue Systems | 2026 | Cascaded ASR-LLM SDS: ASR confidence filtering "fails to detect deletion errors or to distinguish acoustic from linguistic mismatches"; small detectors over ASR latents disentangle perception / comprehension / deletion errors and let the LLM run targeted multi-turn clarification; recall on domain-shift errors 57.96% vs 23.66%; up to 30% WER reduction and 17% downstream-task gain across accents, distortions and domains. | Cascade only (no audio-native arm); clarification targets transcript errors generally, not a ledger of schema-valid wrong TOOL CALLS by entity type; no read-back confirmation with an oracle; no comparison of levers on recovery fraction and turn cost. NEAR — the closest lever paper. |
| 2609.01828 | AVERT: Audio-Verified Adjudication for Spoken Dialogue State Tracking | 2026 | States that ASR errors "concentrate in entity values and persist across turns"; audio-conditioned verifier plus cross-turn agreement with vote / add / swap operators lifts SpokenWOZ JGA from 33.04 (speech-LLM) / 38.34 (text editor) to 40.13. | A silent post-hoc verifier, not a user-facing confirmation; DST slot values, not executed tool calls; no recovery fraction, no lever comparison, no audio-native tool-calling arm. |
| 2605.15104 | From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents | 2026 | Converts text tool-calling benchmarks (Confetti, When2Call) to audio via TTS, speaker variation and environmental noise while keeping gold labels; 7 omni-modal models; text-to-voice gap 1.8-4.8 points on Confetti; failure analysis: degradations "most often reflect misunderstandings of argument values in the speech"; ambiguity-based reformulation stress test; LLM-judge protocol. | Audio-native models only (no local-ASR cascade arm, no audio-LLM-as-transcriber arm); reports an aggregate gap and a qualitative failure analysis, not a silent-wrong ledger by entity type; no read-back, no confidence gating, no ask-when-unsure comparison; no telephone band or speaking-rate conditions. NEAR — closest on the measurement side; must be delineated as the "audio When2Call" baseline. |

## Notes

- **Pre-emption assessment for angle C: no verified paper measures a confirmation lever as a
  recovery fraction of silent-wrong tool calls caused by mis-heard spoken entities.** The
  levers are each studied in isolation and in text: confidence-gated confirmation in classic SDS
  (Komatani & Kawahara 2000; Litman & Pan 2002; Sagawa et al. 2004), instruction-only
  "ask when needed" and structured-uncertainty asking in text tool agents (2409.00557,
  2511.08798, 2504.18851), abstention calibration (2607.10059), and human approval gates for
  risky actions (2607.13594, 2510.05307). What is missing everywhere: (i) the trigger is
  underspecification or risk, never a mis-heard, schema-valid value; (ii) no cascade vs
  audio-native comparison; (iii) no acoustic crossing (voices per accent, rate, noise, 8 kHz);
  (iv) no read-back with a truthful oracle and its false-positive turn cost on already-correct
  calls.
- **Three flags to delineate carefully:**
  1. **2605.25404 (Proactive for Uncertainty)** replaces ASR-confidence gating with cause-aware
     detectors that drive clarification in a cascade, across accents and distortions. It is the
     nearest lever paper. Delineate: transcript-level recovery (WER, downstream task) versus our
     executed-call ledger; cascade-only versus our three pipelines; no read-back oracle.
  2. **2605.15104 (From Text to Voice)** already runs When2Call in audio and names
     argument-value misunderstanding as the dominant failure. Delineate: it is a benchmark
     conversion with an aggregate score gap on omni models; we measure the silent-wrong cell by
     entity type, across cascade vs native, with levers and their costs. Obtain full text before
     CP2 to check whether its "ambiguity-based reformulation stress test" already counts asks.
  3. **2605.09698 (Ambig-DS)** has our exact narrative shape in text data science (silent
     commitment, one-question recovery under idealised conditions, over-ask/silent-default
     miscalibration). Cite as the text analogue; ours is the speech instance with a different
     error source (perception, not specification).
- **Cost-of-confirmation lineage for the paper:** correction-turn counting starts with Danieli
  & Gerbino (cmp-lg/9612003) and PARADISE-era cost measures (Walker et al. 1997, cmp-lg/9704004,
  not tabled); LLM-era papers report extra steps (2606.03135: +0.3 steps), question counts
  (2511.08798: 1.5-2.7x fewer), or human time (2510.05307: -13.54%). None report the
  false-positive cost of confirming calls that were already right, which the MISSION requires.
- **Unverified items to obtain before the bibliography ships:** Skantze 2005 (Speech
  Communication) human error-recovery strategies; Asano et al. COLING 2025 industry (contextual
  ASR error handling with LLMs); San-Segundo et al. belief confirmation with confidence measures;
  Komatani & Kawahara ICSLP 2000 two-level confidence confirmation. Also consider Bohus &
  Rudnicky's later belief-updating work and Williams & Young (2007) POMDP dialogue for the
  "confirmation as a learned policy" thread; neither fetched here.
- **Delineation sentence for the paper:** confirming what a speech system heard is not our
  idea — confidence-gated explicit/implicit confirmation is thirty years old (Komatani &
  Kawahara 2000; Litman & Pan 2002; Sagawa et al. 2004), and LLM agents are now taught when to
  ask (2409.00557, 2511.08798, 2504.18851) and when not to act (2607.10059). What is new in our
  work is the measurement: the fraction of spoken-entity tool calls that execute schema-valid and
  wrong with no question asked, across cascade and audio-native pipelines and acoustic
  conditions, and what read-back confirmation, confidence gating and an ask-when-unsure
  instruction each recover at what cost in turns.
