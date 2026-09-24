# Angle A: Spoken / voice tool calling and voice-agent benchmarks

Scope note: this file maps the EVALUATION-OF-TOOL-CALLING-FROM-SPEECH channel: benchmarks and
systems where a spoken (or audio) request drives an LLM function/tool call, plus the general
voice-assistant benchmarks that a reviewer will expect us to cite. It is prior work we
delineate, not claim. Our candidate contribution is the SILENT-WRONG ledger: the fraction of
spoken-entity tool calls (amounts, digit strings, dates, times, quantities, names/emails)
that execute schema-valid but semantically wrong, with no error and no question, measured
across three pipelines (local Whisper -> text LLM; audio-LLM-as-transcriber -> text LLM;
audio-native LLM with tools), crossed with acoustic conditions (voices per accent, rate,
noise, 8 kHz telephone band), with read-back confirmation (scripted oracle) compared against
ASR-confidence / n-best gating and an ask-when-unsure instruction as recovery levers.

Verification: all arXiv ids below were resolved and abstracts fetched live on 2026-09-24 via
the Semantic Scholar Graph API batch endpoint (`/graph/v1/paper/batch`, keyed by
`ARXIV:<id>`), after `export.arxiv.org/api/query` returned HTTP 429 on every call from this
machine (the arXiv listing-search pages at `arxiv.org/search` did work and were used for
discovery). One id (2603.25727) is not indexed by Semantic Scholar; its abstract was fetched
from `arxiv.org/abs/2603.25727` directly (HTTP 200). One paper (BFCL Audio, ICML 2026) has
no arXiv id: its abstract was fetched live from the OpenReview API (`api2.openreview.net/notes/search`,
note `pgwHOpKkOp`, venue "ICML 2026 regular") and cross-checked against the ICML virtual
poster page (icml.cc/virtual/2026/poster/61489); its PDF is behind an OpenReview browser
challenge and was NOT read in full. Two full texts were read in full from `arxiv.org/html`:
2609.13602 (τ-Elicitation) and 2605.15104 (From Text to Voice). "What it established" lines
are paraphrased from the fetched abstracts (and, for those two, the full text), not from memory.

Not verifiable / not tabled: nothing from the candidate list failed verification. The
desk-rejected ICLR 2026 predecessor of BFCL Audio ("MFCL: A Multi-modal Function Calling
Evaluation for Large Language Models", OpenReview 8yWECy22Zi) exists but its PDF was likewise
challenge-gated; treat BFCL Audio (ICML 2026) as the citable version.

## Spoken / audio tool-calling benchmarks (the exact channel)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2609.13602 | τ-Elicitation: Benchmarking multi-turn entity extraction in voice agents | 2026 (Sep 11) | 200-task voice benchmark, 10 entity types (dates, phones, times, person names, codes, properties, addresses, emails, coined names, medications), controlled difficulty, caller realisms, three environments (regular / noise-heavy 10 dB / speech-heavy). Deterministic database comparison, no LLM judge. Matched text agent passes all tasks; four voice configurations (gpt-realtime-2 minimal/xhigh, gemini-3.1-flash-live, grok-voice) reach robust exact success (Pass^3) of only 0.14-0.41. Initial captures wrong for 42-69% of fields; agents verify more for hard entities but only 24-37% of verified errors are repaired. A scaffold prescribing spelling, read-back, correction and confirmation raises Pass^3 by 14-31 points at 21-28 s per call. Field-by-field validate-and-retry lifts multi-field task Pass@1 from 0.64 to 0.82. Per-voice spread 15-28 points; agents do not raise verification for their weakest voice. | ONLY audio-native realtime models; the paper states "We intentionally omit caller-side ASR", so there is no cascade (Whisper -> text LLM) arm and no cascade-vs-native comparison. Task is ELICITATION (agent asks for a missing field, caller supplies it), not a user-initiated action request whose argument is the entity ("send fifty dollars to Priya"); no amounts or quantities. No 8 kHz telephone band, no speaking-rate factor, no WER covariate, so WER-vs-silent-wrong decoupling is untested. No ASR-confidence / n-best gating lever. The scaffold is a full protocol (spell + read-back + confirm), not isolated read-back with a truthful oracle. Does not frame the schema-valid "silent-wrong" cell explicitly, although its "initial capture wrong and not verified" numbers are that cell in disguise. CLOSEST NEIGHBOUR. |
| (no arXiv id; OpenReview pgwHOpKkOp) | BFCL Audio: An Audio Function Calling Evaluation for Large Language Models | 2026 (ICML; blog Aug 2025) | 6.2K expert-verified audio function-calling tasks in two suites mirroring deployments: BFCL Text Audio (pipelined ASR -> LLM -> tools via transcripts) and BFCL True Audio (end-to-end audio-in -> tool calls). Controlled perturbations: accent, speaking rate, content disfluencies, background noise, via a controllable synthesis/augmentation pipeline. Automatic AST grading of function names AND argument values (single-turn) and state-based metrics (multi-turn), no LLM judge. Proposes a failure-mode taxonomy and analyses which speech/noise factors hurt most. Abstract motivation: "perception errors (e.g., homophones, noise, disfluencies) can corrupt entities and arguments, and natural interactions often require clarification that changes the tool-calling protocol." ICML lay summary: "the worst mistakes are quiet ones, mishearing names or numbers, or babbling instead of acting." | Measures aggregate tool-call accuracy under perturbation; it does not report a ledger that separates schema-valid silent-wrong calls from surfaced errors from clarification requests, nor per-entity-type (amount / digit-string / date / time / name) silent-wrong rates. No 8 kHz telephone band, no per-voice-within-accent spread. No recovery lever: clarification is ALLOWED (spelling clarifications whitelisted for the judge, per the Salesforce blog) but read-back confirmation, confidence gating and ask-when-unsure are not compared for recovery fraction or cost. No local open-weight ASR arm (Whisper) named in the abstract. Full text not read (challenge-gated); must be read before CP2. NEAR neighbour. |
| 2605.15104 | From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents | 2026 (May) | Converts verified text tool-calling benchmarks (Confetti, When2Call) into paired text-audio instances via TTS, speaker (gender) variation and DEMAND environmental noise, preserving gold labels. 7 omni-modal models (GPT-Realtime, Gemini Live, Qwen3-Omni...). Text-to-voice gap 1.8-4.8 points on Confetti; a counterfactual analysis of text-pass/audio-fail cases shows "audio-induced failures often preserve the broad tool-call structure but fail on argument values"; decision errors (call vs. not call) also 26-37%. Also a cascade-vs-omni comparison, a text-LLM scaling analysis for cascade back-ends, an ambiguity reformulation stress test, and a reference-free LLM-judge protocol. | Argument-value failure is observed in an error analysis, not measured as a per-entity-type silent-wrong ledger; no distinction between schema-valid wrong values and malformed calls; no clarification/confirmation lever; no telephone band, accent or rate factor (two voices per TTS provider); no WER covariate. NEAR neighbour on the cascade-vs-omni axis. |
| 2604.22821 | Audio2Tool: Speak, Call, Act - A Dataset for Benchmarking Speech Tool Use | 2026 (Apr) | ~30K spoken queries for SpeechLM tool calling in Smart Car, Smart Home, Wearables; multi-tier complexity (direct commands to multi-intent and needle-in-a-haystack extraction); zero-shot voice-cloning TTS and diverse noise profiles; evaluates SpeechLMs and ASR-LLM pipelines, showing strong performance on simple commands and significant degradation under compositional and acoustic challenge. | Device-control domain with few high-stakes spoken entities (no money, phone numbers, spelled emails); reports tool-calling accuracy, not a silent-wrong / asked / errored ledger; no confirmation lever; no telephone band. |
| 2608.05126 | Spoken Function Calling: A New Perspective on Spoken Language Understanding for Large Audio Language Models | 2026 (Aug) | Reframes SLU as Spoken Function Calling (SFC): spoken functions built from traditional SLU datasets, a multi-agent pipeline synthesising SFC-Bench, evaluation of LLMs and LALMs, and post-training (SpokenFC-7B) that beats GPT-4o-Audio on SFC. | Semantic-extraction accuracy on SLU-derived slots; no entity-error ledger, no acoustic-condition crossing, no cascade-vs-native pipeline ledger, no confirmation lever. |
| 2510.07978 | VoiceAgentBench: Are Voice Assistants ready for agentic tasks? | 2025 (Oct) | 6,000+ synthetic spoken queries (English + six Indic languages) covering single-tool, multi-tool, multi-turn and safety; speaker diversity via embedding-based voice-conversion sampling; measures tool selection, structural consistency, correctness of invocations and adversarial robustness. ASR-LLM pipelines beat end-to-end SpeechLMs (up to 60.6% parameter-filling accuracy in English); SpeechLMs degrade sharply on Indic languages. | Reports parameter-filling accuracy as an aggregate; does not separate silent schema-valid wrong values from structural failures or clarification; no controlled noise / telephone / rate conditions; no recovery lever. Useful as the "cascade beats native on argument filling" prior for D2. |
| 2608.26432 | SpeechGym: An Audio-Native Gym for Training Voice Agents via Reinforcement Learning | 2026 (Aug) | Audio-native RL environment: two omni-modal models converse in native audio over an unmodified text agentic benchmark, so modality is the only variable. Names the mechanism exactly: "the agent picks the right tool and the right argument slot but fills it with a value misheard from the waveform, and that single error cascades into a failed call." Per-turn process reward fixes GRPO gradient starvation; trained agent more than doubles task success on an independent voice benchmark. | A TRAINING paper: the misheard-argument failure is a reward signal, not a measured ledger by entity type, pipeline or acoustic condition; no cascade arm; no acoustic perturbations; no confirmation lever. Cite as the sharpest prior statement of the mechanism. NEAR on framing only. |
| 2605.06897 | MIST: Multimodal Interactive Speech-based Tool-calling Conversational Assistants for Smart Homes | 2026 (May) | Synthetic multi-turn voice-driven code-generation task over IoT devices with spatiotemporal constraints, dynamic state and mixed-initiative interaction; large open/closed-weight gap and headroom for frontier models. | IoT code generation; no entity-error ledger, acoustic conditions, pipeline comparison or confirmation lever. |
| 2609.20152 | MTVA-Bench: Evaluating the Language Model Inside Cascaded Voice Agents | 2026 (Sep 17) | Evaluates the text LLM under the conditions it faces inside a cascade (transcription issues, split turns, script constraints); 49 agents, 490 scenarios, 7 languages; LLM caller, mock backend responds to the arguments actually sent; deterministic tool-call checks plus two citing LLM judges. Six of seven models pick the correct tool within 6.4 points, but overall scores span 24.4 points, mostly from "argument values, action ordering, rule compliance". | Text-side only (no audio, no ASR run, no audio-native arm); transcription issues are simulated in text; no per-entity silent-wrong rates, no acoustic conditions, no confirmation lever. |

## Grounded / full-duplex voice-agent benchmarks (task completion, not entity ledgers)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2603.13686 | τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains | 2026 (Mar) | Extends τ²-bench to full-duplex voice with a controllable LLM user simulator (diverse accents, realistic audio environments, turn-taking, decoupled from wall clock); 278 tasks; text GPT-5 85% pass@1 vs voice agents 31-51% clean and 26-38% with noise and accents (30-45% of text capability); 79-90% of failures attributed to agent behaviour. | End-to-end pass@1; entity capture (authentication) is noted as a bottleneck but not isolated by entity type or by silent-vs-surfaced; no cascade arm; no confirmation lever measured. |
| 2604.04847 | Full-Duplex-Bench-v3: Benchmarking Tool Use for Full-Duplex Voice Agents Under Real-World Disfluency | 2026 (Apr) | Real human audio annotated for five disfluency categories, chained API calls across four domains; six configurations (GPT-Realtime, Gemini Live 2.5/3.1, Grok, Ultravox, Whisper -> GPT-4o -> TTS cascade) scored on accuracy, latency, turn-taking. GPT-Realtime leads Pass@1 (0.600); cascade has perfect turn-take rate but 10.12 s latency. Self-correction handling and multi-step reasoning are the consistent failure modes. | Includes one cascade baseline but reports Pass@1, not an argument-level silent-wrong ledger; disfluency, not entity type or acoustic band, is the manipulated factor; no confirmation lever. |
| 2605.13841 | EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents | 2026 (May) | Bot-to-bot audio simulation with automatic simulator validation; EVA-A (accuracy) and EVA-X (experience) composites; 213 enterprise scenarios; controlled accent and noise perturbation suite; multi-trial pass@k vs pass^k. 12 systems across all three architectures; no system > 0.5 on both; accent/noise deltas up to 0.314 vary by architecture. | Task-level accuracy across architectures with perturbations, but no entity-type ledger, no silent-vs-surfaced distinction, no confirmation lever; no telephone band. |
| 2607.27453 | VAmoS Bench: Voice Agent Simulation Bench | 2026 (Jul) | End-to-end phone-call simulation: agent "Riley" (credit-card support, five SQL tools against a seeded Postgres backend), 100 scenarios, ~1/3 adversarial; grader checks binary assertions against the full trace incl. tool arguments and returned rows, catching agents that claim a change without writing it. Containment framing. | Whole-call correctness in one banking task; does not isolate spoken-entity argument errors, acoustic conditions or pipeline architecture; no confirmation lever. |
| 2608.10716 | DuplexWorld: Can voice agents help you get through the day? | 2026 (Aug) | Six "worlds" (banking, insurance, travel, healthcare, logistics, pathfinding), 156 scenarios, 350+ hours; agentic, conversational and speech-naturalness metrics; best Pass@1 0.490. | Holistic; explicitly moves away from "tests of agentic tool calling against a database"; no entity ledger, no acoustics, no lever. |
| 2510.21244 | VoiceAgentEval / OutboundEval: A Dual-Dimensional Benchmark for Expert-Level Intelligent Voice-Agent Evaluation | 2025 (Oct) | Outbound-calling benchmark: six domains, 30 sub-scenarios, LLM-driven persona-rich user simulator, dynamic scoring of task execution, knowledge, adaptability and UX; 12 LLMs. | Evaluates the LLM in outbound-call scripts; no audio pipeline comparison, no entity error ledger, no acoustic conditions, no confirmation lever. |
| 2604.16456 | EchoChain: A Full-Duplex Benchmark for State-Update Reasoning Under Interruptions | 2026 (Apr) | Controlled interruption injection; three failure patterns (contextual inertia, interruption amnesia, objective displacement); half-duplex control cuts failures 40.2%; no real-time model > 50%. | Interruption handling, not entity capture or tool arguments. |
| 2609.24812 | MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents | 2026 (Sep 21) | 1,152 multi-party audio scenes (EN/ZH) with expected tool calls and atomic rubrics; best 66.8% EN; open-weight models bottlenecked by the multi-speaker audio front-end. | Multi-speaker perception; no per-entity argument ledger, no acoustic band, no lever. |
| 2608.24314 | Benchmarking LLM Judges for Voice-Agent Evaluation: Reliability, Calibration, and Human Oversight | 2026 (Aug) | Human vs GPT-4.1/GPT-5 judges on telecom and retail voice-agent conversations under three configurations; reliability is metric- and configuration-dependent; motivates hybrid pipelines. Notes error propagation across ASR, reasoning and tool-calling stages as a pipeline factor. | Judge reliability study; no controlled measurement of entity errors or levers. |
| 2609.04206 | Auditing Bias and Safety in Voice AI Customer Care | 2026 | Validation-gated audit framework for stateful, tool-mediated customer-care voice agents that separates native S2S, cascaded ASR->LLM->TTS and hybrid architectures, uses matched service facts across caller-presentation conditions, and records path-to-service burden; synthetic worked example only. | Fairness/safety audit design, no results; no entity-error ledger or levers. |

## Systems that emit tool calls from speech (models / architectures; cite as the deployment landscape)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2605.20755 | DuplexSLA: A Full-Duplex Spoken Language Model with Synchronized Speech, Language, and Action | 2026 (May) | Native full-duplex model decoding assistant audio plus a rate-limited textual action channel on a shared 160 ms clock; in-conversation planning and tool calls without halting speech; DuplexSLA-Bench covers pause/interrupt/backchannel and three styles of in-conversation tool calling. | Architecture paper; no entity-error ledger, no acoustic crossing, no confirmation lever. |
| 2609.19334 | A frontend-backend architecture for tool calls in full-duplex speech models | 2026 (Sep 16) | Duplex speech-to-text frontend emits a delegation token and forwards streaming ASR transcripts to a text backend LLM for tool calls; 92-97% tool-call recall, 81.2% irrelevant-call rejection; competitive on FDB-v3 and EVA-Bench. | Hybrid cascade design; reports recall / selection, not argument-value silent-wrong rates; no acoustic conditions or lever. |
| 2609.21967 | NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities | 2026 (Sep 18) | Open full-duplex S2S model with parallel output streams for agent text and structured function calls plus an RNN-T transcription branch; 82.5% tool-selection F1 on FDB 3.0 "while argument accuracy and end-to-end tool execution remain areas for improvement." | Model release; argument-accuracy gap acknowledged but not dissected; no ledger, no lever. |
| 2609.25176 | Qwen-Audio-3.1-Realtime: Towards Reliable Agentic Voice Interaction | 2026 (Sep 21) | Think / Act / Speak-and-Coordinate training (M²-OPD distillation, GRPO in self-evolving executable environments); task success 78.4% -> 82.0% on a half-duplex speech-to-text adaptation of τ-Voice; background-speech response rate 73% -> 13% on FDB v1.5. | Model report; no entity ledger, no acoustics crossing, no lever. |
| 2510.02044 | Stream RAG: Instant and Accurate Spoken Dialogue Systems with Streaming Tool Usage | 2025 (Oct) | First tool use directly inside speech-in speech-out systems; predicts tool queries in parallel with user speech; AudioCRAG benchmark; QA accuracy 11.1% -> 34.2%, tool latency -20%. | Retrieval tools for factual QA; no argument-entity errors, no acoustics, no lever. |
| 2604.15710 | VoxMind: An End-to-End Agentic Spoken Dialogue System | 2026 (Apr) | 470-hour AgentChat data, Think-before-Speak, multi-agent dynamic tool management decoupling latency from toolset size; task completion 34.88% -> 74.57%, beating Gemini-2.5-Pro on spoken agent tasks. | System paper; no ledger, no acoustics, no lever. |
| 2512.20156 | Fun-Audio-Chat Technical Report | 2025 (Dec) | Dual-resolution speech representations and Core-Cocktail training; reports competitive "Speech Function Calling" among other capabilities; open-source 8B and duplex variant. | Model report; speech function calling is one aggregate score. |
| 2601.07367 | FOCAL: A Novel Benchmarking Technique for Multi-modal Agents | 2026 (Jan) | Framework to benchmark end-to-end reasoning and component-wise error propagation through cascaded voice agents (voice-to-voice + text), with Reasoning and Semantic scores for voice output. | Framework proposal; no entity-type ledger, no controlled acoustic crossing, no confirmation lever. |

## ASR entity exactness and input-channel robustness (adjacent; the "known" half of our story)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2608.28916 | VoiceCodeBench: Evaluating Exact Structured-Token Recovery in Automatic Speech Recognition | 2026 (Aug) | 300 human-recorded workplace segments, 85 speakers, 1,482 audited entities across 26 types; 19 ASR systems scored by WER, Canonical Token/Entity Match and strict Task Success Rate; WER has little rank agreement with CTEM (rho = -0.28) or TSR (-0.22); best TSR 68.7%, so ~1/3 of recordings keep an unrecovered critical value. | ASR-only: no LLM, no tool call, no execution, no clarification; establishes WER-vs-entity decoupling at the ASR stage, which our D4 extends to executed calls. |
| 2603.25727 | Back to Basics: Revisiting ASR in the Age of Voice Agents | 2026 (Mar) | WildASR: four-language diagnostic benchmark of real speech factorising robustness along environmental degradation, demographic shift and linguistic diversity; seven ASR systems degrade severely and unevenly; models "often hallucinate plausible but unspoken content under partial or degraded inputs, creating concrete safety risks for downstream agent behavior." | ASR-only; downstream agent behaviour is motivated, not measured; no tool calls or levers. |
| 2603.16411 | RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery | 2026 (Mar) | Post-ASR entity correction using n-best hypotheses (1-best, entity-aware select, ROVER, LLM-select) plus retrieval and constrained LLM correction; 8-46% relative entity-WER reduction. | Correction at the transcript level using n-best; not a clarification/confirmation lever measured on executed tool calls; no pipeline comparison. Relevant prior for our n-best-disagreement gate. |
| 2605.17443 | Analyzing Error Propagation in Korean Spoken QA with ASR-LLM Cascades | 2026 (May) | Downstream degradation tracks ASR-stage information loss consistently across LLMs; single-character ASR errors are salient; an audio LLM beats a matched-backbone cascade in noisy Korean SQA. | QA, not tool execution; no entity ledger or lever. |
| 2608.03970 | Should We Type or Talk to LLM Agents? A Comprehensive Study of Voice and Keyboard Input Perturbations | 2026 (Aug) | HIVE perturbation suite: voice-transcription perturbations lower accuracy across all instruction-tuned models (structure, not fillers, carries the cost); keyboard noise costs less; harm traces to token survival; a thinking budget recovers the keyboard channel but not spoken registers. | Text-level perturbations of QA prompts, no audio, no tool calls, no entity ledger. |
| 2602.11348 | AgentNoiseBench: Benchmarking Robustness of Tool-Using LLM Agents Under Noisy Condition | 2026 (Feb) | Categorises user-noise and tool-noise; automated pipeline injects controllable noise into agent benchmarks while preserving solvability; consistent sensitivity across models. | Text-channel noise on tool agents; no speech, no acoustics, no confirmation lever. |

## General voice-assistant / spoken-dialogue benchmarks (checked for pre-emption; none measure tool arguments)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2410.17196 | VoiceBench: Benchmarking LLM-Based Voice Assistants | 2024 | 6,783 synthetic and real spoken instructions across eight tasks (knowledge, instruction following, safety) with speaker, environment (reverberation) and content (mispronunciation) variations. | No tool calling, no entity arguments, no lever. |
| 2406.16020 | AudioBench: A Universal Benchmark for Audio Large Language Models | 2024 | 8 tasks, 26 datasets for speech, audio-scene and paralinguistic understanding of AudioLLMs. | No tool calling. |
| 2509.22651 | VoiceAssistant-Eval: Benchmarking AI Assistants across Listening, Speaking, and Viewing | 2025 (Sep) | 10,497 examples across 13 categories; 21 open models + GPT-4o-Audio; models excel at speaking, lag on audio understanding. | No tool calling. |
| 2510.15406 | VocalBench-DF: A Benchmark for Evaluating Speech LLM Robustness to Disfluency | 2025 (Oct) | 22 Speech-LLMs degrade substantially under a disfluency taxonomy; phoneme-level processing and long-context modelling are the bottlenecks. | Disfluency, not entity arguments or tools. |
| 2603.16783 | SpokenUS: A Spoken User Simulator for Task-Oriented Dialogue | 2026 (Mar) | SpokenTOD (52,390 dialogues, 1,034 h) with cross-turn slots, barge-in, disfluency, emotional prosody; SpokenUS simulator with turn-taking head discloses slot values gradually. | Simulator for TOD; no tool-execution ledger, no acoustic band, no lever. Useful if we later want a spoken user simulator instead of a scripted oracle. |
| 2305.13040 | SpokenWOZ: A Large-Scale Speech-Text Benchmark for Spoken Task-Oriented Dialogue Agents | 2023 | 249 h human-to-human spoken TOD, 8 domains; cross-turn and reasoning slot detection; best DST joint goal accuracy 25.65%. | Slot-tracking accuracy under real ASR, no executed tool calls, no pipeline comparison, no confirmation lever. |
| 2207.10643 | STOP: A Dataset for Spoken Task Oriented Semantic Parsing | 2022 | Largest public end-to-end SLU dataset with semantic parses, human and TTS audio, low-resource splits; motivates E2E SLU to avoid cascading ASR errors. | Parsing accuracy; no execution ledger, no lever. |
| 2608.19515 | Hear2Act: Benchmarking When Prosody Should Change What an Assistant Does | 2026 (Aug) | 480 scenarios varying whether a concern is lexical or prosodic; audio-capable LLMs recover prosodic information but do not carry it into action without an explicit intermediate representation. | Prosody-to-action, not entity capture. |

## Notes

- **Pre-emption assessment: no verified paper measures the silent-wrong ledger for spoken-entity
  tool calls across cascade vs audio-native pipelines crossed with acoustic conditions with
  read-back confirmation compared against confidence gating.** But the niche is crowded and moving
  fast (four of the papers above appeared in the last 14 days), and two neighbours each own one
  axis of the candidate:
  1. **τ-Elicitation (2609.13602, Sep 11 2026, Sierra/Mercor)** owns the CONFIRMATION-RECOVERY
     axis: read-back/spelling/confirmation scaffold measured for exact-entity success (+14-31
     Pass^3 points, +21-28 s), verification effort, repair rate of verified errors (24-37%),
     per-voice spread. It deliberately has no ASR/cascade arm, no telephone band, no rate factor,
     no WER covariate, no confidence-gating comparator, no amounts/quantities, and its task is
     elicitation rather than argument-bearing action requests. Our D3 (read-back recovers >80%
     with a truthful oracle) must be positioned against their 24-37% repair rate when the agent
     chooses to verify, and their 14-31 point scaffold gain; our oracle is more cooperative than
     theirs in one respect (corrects once from ground truth) and their caller "confirms or
     corrects read-backs" too, so the designs are close. Distance: EXACT-NICHE on the lever axis,
     NEAR overall.
  2. **BFCL Audio (ICML 2026; no arXiv id)** owns the PIPELINE x ACOUSTICS axis: pipelined
     ASR->LLM vs true-audio suites, accent / rate / disfluency / noise perturbations, AST grading
     of argument values, failure taxonomy that (per the ICML lay summary) singles out "quiet"
     mishearing of names and numbers. It does not compare recovery levers and does not report an
     entity-type-resolved silent-wrong ledger; full text unread. Distance: NEAR.
  3. **From Text to Voice (2605.15104)** is NEAR on the cascade-vs-omni comparison with the
     explicit finding that audio failures "preserve the broad tool-call structure but fail on
     argument values"; **SpeechGym (2608.26432)** states the mechanism in one sentence ("fills it
     with a value misheard from the waveform") but only as an RL reward.
- **What remains unclaimed if the above holds:** (a) the four-way ledger CORRECT / SILENT-WRONG
  / ERROR-SURFACED / ASKED per entity type x pipeline (P1 local Whisper, P2 audio-LLM
  transcriber, P3 audio-native), with the "by construction" schema-valid cells labelled;
  (b) the acoustic crossing including 8 kHz mu-law telephone band and speaking rate with WER
  reported per voice and condition as a covariate (D4: WER poorly predicts silent-wrong, the
  executed-call analogue of VoiceCodeBench's ASR-stage finding); (c) three levers compared on
  the same silent-wrong cell: read-back confirmation with oracle vs ASR-confidence / n-best
  gating vs ask-when-unsure instruction, with recovery fraction, false-positive confirmation
  cost on already-correct calls, extra turns and tokens; (d) clarification calibration
  (asked-and-wrong / asked-and-right / silent-and-wrong / silent-and-right) across pipelines
  (D2), which τ-Elicitation reports only for native realtime models.
- **Actions before CP2:** obtain and read the BFCL Audio ICML PDF (OpenReview note
  pgwHOpKkOp; challenge-gated from this machine) to confirm it has no confirmation-lever
  comparison and no per-entity-type silent-wrong table; re-read τ-Elicitation Table 3
  (validate-and-retry) since it is the nearest thing to a recovery-vs-cost number; check
  whether τ-Elicitation's released code includes a cascade option. If BFCL Audio's failure
  taxonomy already contains a "silent wrong-argument" category with per-condition rates, our
  contribution narrows to the lever comparison and the telephone/WER-decoupling axis.
- Non-arXiv classics to cite for the confirmation lever's lineage: Skantze, "Error Handling in
  Spoken Dialogue Systems" (PhD thesis, KTH 2007) and Bohus & Rudnicky on explicit vs implicit
  confirmation in RavenClaw-era systems (τ-Elicitation cites "Error Detection and Recovery in
  Spoken Dialogue Systems" as its repair-strategy reference); Salesforce blog "BFCL Audio: A
  Benchmark for Audio-Native Function Calling" (22 Aug 2025) documents the whitelisted
  spelling-clarification rule.
- Year caveats: Semantic Scholar dates 2609.04206 as 2026-05-18 despite the 2609 id; the arXiv
  listing gives 2608.24314 as submitted 16 Sep 2026 (v2) vs S2 2026-08-25. Re-check before the
  bibliography ships.
- Delineation sentence for the paper: that voice agents mis-hear spoken entities and that the
  mis-heard value lands in a tool argument is not ours: BFCL Audio and From Text to Voice
  (2605.15104) show argument values are where audio tool calling degrades, SpeechGym
  (2608.26432) names the misheard-slot mechanism, VoiceCodeBench (2608.28916) shows WER does not
  track exact-entity recovery at the ASR stage, and τ-Elicitation (2609.13602) shows a
  read-back scaffold lifts exact entity capture in audio-native agents. What is new in our work
  is the ledger and the lever comparison: the fraction of executed calls that are schema-valid
  and semantically wrong with no error and no question, by entity type across cascade and
  audio-native pipelines and acoustic conditions including the telephone band, and how much of
  that cell read-back confirmation, confidence gating and an instruction each recover at what
  cost.
