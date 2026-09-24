# Angle B: ASR errors on spoken entities and their downstream effect

Scope note: this file maps the ENTITY-ERROR channel, which is prior work we delineate, not
claim. That ASR mis-hears numbers, digit strings, amounts, dates and names, that those errors
propagate into slot filling, dialogue state tracking and LLM-based understanding, and that WER
is a weak proxy for the damage, is established below. Our paper's contribution is elsewhere:
the SILENT-WRONG ledger for spoken-entity tool calls (schema-valid call, no error surfaced, no
question asked, wrong semantics executed against a mock backend), measured across three
pipelines (local Whisper -> text LLM; audio-LLM-as-transcriber -> text LLM; audio-native LLM
calling tools directly), crossed with acoustic conditions (voices per accent, rate, babble
noise, 8 kHz telephone band), with read-back confirmation measured as a recovery lever against
ASR-confidence / n-best gating and an ask-when-unsure instruction. None of the papers below
measure that ledger; the closest neighbours are flagged at the bottom.

Verification: every id below was resolved and its abstract fetched live on 2026-09-24. The
first 28 ids resolved through the Semantic Scholar Graph API batch endpoint
(`/graph/v1/paper/batch`, keyed `ARXIV:<id>`; 28/31 returned, then the endpoint began
returning HTTP 429). The three S2 misses (2603.25727, 2507.16456, 2506.22858) and six later
additions (2609.20152, 2402.01931, 2606.18659, 2407.21414, 2502.13446, 2606.23060) were
fetched from `export.arxiv.org/abs/<id>` (the `export.arxiv.org/api/query` endpoint returned
429 for the whole session and `arxiv.org` did not resolve from this host). "What it
established" lines are paraphrased from the fetched abstracts, not from memory. Ids that could
NOT be verified: none. Seven ids were verified but left out of the tables as tangential:
2409.02449 (Indic normalisation pitfalls), 2606.23060 (Whisper hallucination detection),
2507.16835 (STT x LLM x TTS interview stacks), 2410.15609 (speech noise injection for SLU
training), 2508.20700 (generative NE correction), 2409.08107 (WhisperNER), 2404.09754 (LLM
resilience to noisy instructions incl. ASR errors). One caveat: the web-search snippet for
2608.05126 says ASR misrecognitions of proper nouns and numerical values are the primary
bottleneck; that sentence is NOT in the fetched abstract and must be checked in the full text
before we cite it that way.

## Numeric / digit / named-entity transcription errors and their correction

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2408.00004 | Handling Numeric Expressions in Automatic Speech Recognition | 2024 | Correct formatting of numeric expressions (years, timestamps, currency amounts, quantities) depends on context (1945 vs 19:45); compares cascaded and end-to-end approaches, with LLM+TTS-generated adaptation data; LLM-based approaches do well on formatted numerics, adapted end-to-end models are competitive at lower latency. | Formatting of numerics on a transcript, scored by transcript metrics. No tool call, no executed-wrong-semantics cell, no pipeline-vs-audio-native comparison, no confirmation lever. |
| 2402.01931 | Digits micro-model for accurate and secure transactions | 2024 | Financial-domain multi-digit number recognition: a small specialised "micro" model reaches 1.8% digit error vs 5.8% for Whisper, handling diverse real-world ways of speaking digit strings, on-premise with a small memory footprint. | Reports digit error rate of the ASR only. Does not follow a mis-heard digit string into a downstream call, does not compare pipelines or acoustic conditions systematically, no confirmation. Useful as a baseline number for Whisper digit error. |
| 2506.22858 | Mind the Gap: Entity-Preserved Context-Aware ASR Structured Transcriptions | 2025 | Whisper-class ASR "struggles with named entities and numerical data, especially when proper formatting is required" (legal, financial, medical); overlapping 5 s context windows during training plus entity-labelled training data improve NER and entity formatting on Spoken Wikipedia. | ASR-side fix evaluated on NER/formatting; nothing downstream, no tool calls, no acoustic-condition grid, no lever comparison. |
| 2409.06062 | Retrieval Augmented Correction of Named Entity Speech Recognition Errors | 2024 | End-to-end ASR still has a significant error rate on rare entity names; a RAG-like corrector (vector DB of entities, queries from errorful hypotheses, LLM adapted to correct) yields 33-39% relative WER reduction on synthetic voice-assistant queries of rare music entities without regressing on STOP. | Correction of names via a known entity catalogue; amounts, digit strings and dates have no catalogue. No executed-call ledger, no audio-native comparison, no confirmation lever. |
| 2603.16411 | RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery | 2026 | Entity errors in finance, medicine and ATC are costly and hard to fix when the entity is absent from the 1-best; an agentic corrector uses multiple ASR hypotheses (1-best, entity-aware select, ROVER, LLM-select) plus retrieval and constrained LLM correction; 8-46% relative entity-phrase WER reduction and up to +22 pp recall across five datasets. | Uses n-best as evidence for CORRECTION, not as a gate that forces a clarification question; scored by E-WER/recall, not by executed-call semantics; no pipeline or acoustic comparison. |
| 2507.05727 | ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark | 2025 | Large benchmark (40k entries, 300k+ named entities, 10+ domains) for the linguistic competence of ASR on entity-rich speech with three context-exploitation modes; LALMs outperform conventional ASR by a large margin thanks to world knowledge, with room remaining. | Entity recognition accuracy of the transcriber; entities are domain terms, not amounts/digits/dates; no tool call, no silent-wrong labelling, no confirmation. Relevant as evidence that audio-LLMs transcribe entities better (bears on D2). |
| 2501.06129 | Contextual ASR Error Handling with LLMs Augmentation for Goal-Oriented Conversational AI | 2025 | Ranks n-best ASR hypotheses by similarity to dialogue-state context and ranks context by phonetic correspondence to hypotheses; in home-improvement and cooking domains with real users, correction recall +34% and F1 +16% at held precision, and users rate the system higher when correction works. | Correction inside a goal-oriented assistant, not measurement of the executed-wrong cell; no audio-native arm, no acoustic grid, no read-back confirmation as a lever. |

## WER vs downstream damage: decoupling and entity-aware metrics

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2507.16456 | An approach to measuring the performance of Automatic Speech Recognition (ASR) models in the context of Large Language Model (LLM) powered applications | 2025 | With LLMs as the core downstream component, the significance of different ASR error types for the downstream task needs re-examination; analyses LLMs' ability to correct ASR errors and proposes a new ASR measure for LLM-powered applications. | Proposes a metric; does not run a tool-calling agent, does not isolate entity errors as the failure class, no pipeline or acoustic comparison, no lever. |
| 2608.30348 | Perceptually Better, Semantically Worse: Measuring Speech Enhancement Impact on LLM-Based Voice Systems | 2026 | Output Divergence Rate (how often preprocessing changes an LLM's intent decision vs clean speech) on 2,974 SLURP clips with Whisper large-v3 and wav2vec2 cascades: MetricGAN+ doubles ODR despite better PESQ; echo reaches ODR 0.836 via speaker substitution, "a failure WER cannot capture"; audio-quality metrics correlate weakly with ODR. | Intent classification, not entity arguments in tool calls; the "divergence" is not partitioned into silent-wrong vs surfaced vs asked; no audio-native arm, no confirmation lever. Strong methodological precedent for "WER is not the right covariate". |
| 2406.12387 | Performant ASR Models for Medical Entities in Accented Speech | 2024 | On clinical English across 93 African accents, models with low overall WER still show higher error on clinical entities (drugs, diagnoses, lab results), "potentially posing substantial risks to patient safety"; introduces entity alignment, medical NE recall, medical WER and CER; fine-tuning improves medical WER 25-34% relative. | Entity error measured on the transcript; never executed as an action; accent is the only condition; no LLM downstream, no pipelines, no confirmation. Direct precedent for D4/D5 (entity error decouples from WER; accent raises it). |
| 2609.20828 | Beyond WER: Entity and Disfluency Recall in Accented Conversational ASR | 2026 | ASR optimised for WER misses named entities in accented conversational English (India, Indonesia, Latin America): entity recall 53-55% baseline, raised to 80-85% with entity-dense curation and regional LoRA adapters on Qwen2.5-Omni-3B; six-category error taxonomy with LLM judge (83.8% agreement on 210 human-labelled samples). | Language-learning feedback setting; entities are names, not amounts/digits; no downstream action or tool call; no telephone band or noise; no confirmation. |
| 2605.17443 | Analyzing Error Propagation in Korean Spoken QA with ASR-LLM Cascades | 2026 | Downstream semantic failures from ASR errors that conventional ASR metrics miss; relative downstream degradation is consistent across LLMs (cascade degradation tracks ASR-stage information loss); single-character ASR errors are a salient source; a large audio LM beats a matched-backbone cascade in noisy Korean SQA. | Question answering, not tool calls; no entity-type ledger, no silent-vs-asked partition, no confirmation lever. Its cascade-vs-audio-native finding in noise points the OPPOSITE way to our D2 and must be cited. |
| 2502.13645 | Measuring the Effect of Transcription Noise on Downstream Language Understanding Tasks | 2025 | A configurable framework for assessing task models under different transcript-noise severities and types and for examining transcript-cleaning; on three SLU tasks and four models, task models tolerate a certain noise level and are affected differently by error types. | Text-side noise injection on summarisation-style SLU tasks; no spoken entities, no executed calls, no pipeline comparison, no confirmation. |

## Acoustic conditions: accent, noise, telephone band

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2603.25727 | Back to Basics: Revisiting ASR in the Age of Voice Agents | 2026 | WildASR, a four-language diagnostic benchmark of real speech factorising ASR robustness along environmental degradation, demographic shift and linguistic diversity; seven ASR systems degrade severely and unevenly, robustness does not transfer across languages/conditions, and models "hallucinate plausible but unspoken content under partial or degraded inputs, creating concrete safety risks for downstream agent behavior". | Stops at the transcript; the safety risk to agent behaviour is asserted, not measured as executed tool calls; no entity-type breakdown, no pipelines, no confirmation lever. The "plausible but unspoken" observation is the ASR-side seed of our silent-wrong mechanism. |
| 2606.18659 | Responsible ASR: Overcoming Challenges of Foundational Models in Narrow-Band and Low-Resource Settings | 2026 | Open-source and commercial foundation ASR evaluated zero-shot on narrow-band (telephony) spontaneous Hindi and Indian-accented English customer-support calls; performance is suboptimal across the board; fine-tuning on limited real recordings helps unevenly depending on pretraining exposure. | WER on telephony audio only; no entity-level analysis, no downstream LLM or tool call, no comparison to wide-band under controlled conditions, no confirmation. |

## SLU / spoken task-oriented dialogue robustness to ASR errors (foundational and LLM-era)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 1909.10861 | Learning ASR-Robust Contextualized Embeddings for Spoken Language Understanding | 2019 | Confusion-aware fine-tuning: pre-trained LMs are tuned to give similar representations to acoustically confusable words from word confusion networks, significantly improving SLU on ASR transcripts. | Pre-LLM classification/slot SLU; no tool execution, no entity ledger, no audio-native arm, no lever. Foundational for the "acoustically confusable entities" framing. |
| 2108.13048 | ASR-GLUE: A New Multi-task Benchmark for ASR-Robust Natural Language Understanding | 2021 | Six NLU tasks under ASR error across 3 background-noise levels and 6 speakers; systematically studies the effect of noise intensity, error type and speaker variants; correction-based and augmentation-based robustness methods help "to some extent" but remain far from human. | NLU classification tasks, not slot values feeding an action; no entities as the unit, no LLM tool calling, no telephone band, no confirmation. Foundational precedent for crossing noise x speaker. |
| 2011.13205 | SLURP: A Spoken Language Understanding Resource Package | 2020 | Largest and most diverse English SLU dataset at release (18 domains), baselines with SOTA NLU+ASR, and a transparent entity-labelling metric (SLU-F1) enabling detailed error analysis. | Scenario/action/entity labels on a transcript; no execution, no silent-wrong concept, no LLM tool calling. The standard corpus our entity-slot framing descends from. |
| 2207.10643 | STOP: A Dataset for Spoken Task Oriented Semantic Parsing | 2022 | Largest public spoken semantic-parsing dataset, with human-recorded and TTS-generated audio, low-resource splits; motivated by end-to-end SLU "preventing cascading errors from ASR". | Semantic parse accuracy; no executed calls, no entity-type ledger, no LLM comparison, no confirmation. Precedent for TTS-rendered spoken benchmarks. |
| 2305.13040 | SpokenWOZ: A Large-Scale Speech-Text Benchmark for Spoken Task-Oriented Dialogue Agents | 2023 | 249 h human-to-human spoken TOD across 8 domains; introduces cross-turn slot and reasoning slot detection; best DST reaches only 25.65% joint goal accuracy and best end-to-end model completes 52.1% of requests, including ChatGPT baselines. | Dialogue state tracking, not tool execution; no partition of slot errors into surfaced vs silent; no audio-native LLM with tools, no acoustic grid, no confirmation lever. |
| 2311.07418 | Speech-based Slot Filling using Large Language Models | 2023 | LLMs (GPT-3.5, GPT-4, LLaMA-13B, Vicuna) on slot filling with noisy ASR transcriptions via in-context learning and fine-tuning on SLURP at different ASR error rates; prompt design plus linearised knowledge injection gives +8.3 absolute SLU-F1 over Flan-T5. | Slot F1 on transcripts; no executed call, no silent-wrong vs asked partition, no audio-native arm, no acoustic conditions beyond ASR error rate, no confirmation. Closest LLM-era SLU precedent. |
| 2310.06504 | Revisit Input Perturbation Problems for LLMs: A Unified Robustness Evaluation Framework for Noisy Slot Filling Task | 2023 | Noise-LLM: five single and four mixed input perturbations for slot filling, multi-level augmentation and demonstration strategies; open-source LLMs show limited perturbation robustness. | Text perturbations, not real audio; slot extraction, not tool execution; no pipelines, no acoustic grid, no lever. |
| 2401.02921 | Towards ASR Robust Spoken Language Understanding Through in-Context Learning with Word Confusion Networks | 2024 | Feeding LLMs word confusion networks from ASR lattices instead of the 1-best, in ICL for spoken QA and intent classification, bridges much of the gap to an oracle transcript and probes robustness across ASR conditions. | Uses n-best/WCN to IMPROVE the answer, not to decide whether to ask; no tool execution, no entity ledger, no audio-native arm, no confirmation. Direct precedent for our n-best-disagreement gate. |

## ASR confidence, n-best, and clarification as levers

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2407.21414 | Towards interfacing large language models with ASR systems using confidence measures and prompting | 2024 | Post-hoc LLM correction of ASR transcripts with confidence-based filtering so that likely-correct transcripts are not damaged; improves weaker ASR systems. | Confidence gates a corrector, not a clarification question; scored by WER; no tool calls, no entity focus, no pipeline comparison. |
| 2502.13446 | Adopting Whisper for Confidence Estimation | 2025 | Fine-tunes Whisper itself to emit word-level confidence scores; Whisper-tiny matches a strong CEM in-domain and beats it on eight out-of-domain sets; Whisper-large outperforms substantially everywhere. | Confidence quality (calibration of word errors), not the downstream decision it should drive; no gating experiment, no entities, no tool calls. Justifies using Whisper-derived confidence as a gate. |
| 2605.25404 | Proactive for Uncertainty: Cause-Aware Error Diagnosis and Interactive Clarification for Spoken Dialogue Systems | 2026 | Cascaded ASR-LLM SDS suffer error propagation; plain ASR confidence filtering "fails to detect deletion errors or to distinguish acoustic from linguistic mismatches"; small detectors on ASR latents classify token errors into perception/comprehension/deletion and let the LLM run targeted multi-turn clarification; recall on domain-shift errors 57.96% vs 23.66%, up to -30% WER and +17% downstream across accents, distortions and domains. | The lever is a learned error detector driving clarification; it is not compared with read-back confirmation, and the downstream metric is not an executed-tool-call ledger partitioned into silent-wrong / surfaced / asked. No audio-native arm, no entity-type breakdown, no false-positive (asked-when-right) cost reported in the abstract. CLOSEST on the lever side. |

## Cascade vs audio-native LLMs and spoken tool calling (closest to the candidate)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2602.17598 | The Cascade Equivalence Hypothesis: When Do Speech LLMs Behave Like ASR->LLM Pipelines? | 2026 | Matched-backbone testing separates the speech LLM from its text backbone; logit-lens/LEACE show the literal transcript emerging in hidden states and text representations being causally necessary; in most deployed use cases speech LLMs are "expensive cascades, and under noise, they are worse ones", clean advantages reversing by up to 7.6% at 0 dB. | General task accuracy, not tool-call argument semantics; no silent-vs-asked partition; no confirmation lever. Bears directly on D2 and must be cited: it predicts P3 will not beat P1/P2 in noise. |
| 2608.05126 | Spoken Function Calling: A New Perspective on Spoken Language Understanding for Large Audio Language Models | 2026 | Reframes SLU as spoken function calling with structured rule definitions; extends SLU datasets into a suite of spoken functions, synthesises SFC-Bench with a multi-agent system, evaluates LLMs and LALMs, and post-trains LALMs; SFC outperforms traditional SLU on semantic extraction accuracy. | Function-call accuracy as an SLU metric; the abstract does not partition errors into schema-valid-but-wrong vs surfaced vs clarified, does not execute calls against a backend, does not cross acoustic conditions (accent, rate, noise, telephone band), and measures no confirmation or confidence lever. (Search snippet claims ASR errors on proper nouns and numbers are the bottleneck; not in the abstract, verify in full text.) |
| 2605.15104 | From Text to Voice: A Reproducible and Verifiable Framework for Evaluating Tool Calling LLM Agents | 2026 | Converts verified text tool-calling benchmarks (Confetti, When2Call) into paired audio via TTS, speaker variation and environmental noise while keeping schema and gold labels; 7 omni-modal models; text-to-voice gap 1.8-4.8 points on Confetti; failure analysis: "degradations most often reflect misunderstandings of argument values in the speech"; plus ambiguity stress test and validated LLM-judge protocol. | Only omni-modal (audio-native) models: no local-Whisper cascade or audio-LLM-as-transcriber arm, so no pipeline comparison. Argument-value errors are noted in a failure analysis, not tabulated as a silent-wrong ledger by entity type; calls are scored against gold, not executed against a backend with a "no error, no question" criterion; no telephone band, speaking rate or per-accent voice spread; no read-back confirmation, confidence gating or ask-when-unsure lever; no WER covariate. CLOSEST NEIGHBOUR. |
| 2609.20152 | MTVA-Bench: Evaluating the Language Model Inside Cascaded Voice Agents | 2026 | Evaluates the LM inside a cascaded voice agent under the conditions it actually faces (transcription issues, caller speech split across messages, language/script rules); 49 agents, 490 scenarios, 7 languages; LLM-played caller, mock backend responding to the arguments actually sent, deterministic tool-call checks plus two citing LLM judges; across seven models, tool selection is within 6.4 points but overall scores span 24.4 points, with "most of the gap" from argument values, action ordering and rule compliance. | Text-simulated transcription issues, no real audio, so no ASR/acoustic conditions and no audio-native arm; argument-value errors are not traced to a mis-heard spoken entity or partitioned into silent-wrong vs asked; no confirmation or confidence lever measured. SECOND-CLOSEST. |

## Notes

- **Pre-emption assessment: no verified paper measures the silent-wrong ledger.** The pieces
  exist separately: ASR mis-hears numerics and names (2408.00004, 2402.01931, 2506.22858);
  entity error decouples from WER, especially under accent (2406.12387, 2609.20828,
  2608.30348); ASR errors propagate into slot filling and DST (2108.13048, 2305.13040,
  2311.07418); confidence and n-best can drive correction or clarification (2401.02921,
  2407.21414, 2605.25404); and spoken tool calling has just started to be benchmarked
  (2608.05126, 2605.15104, 2609.20152). Nobody joins them into: executed call, schema-valid,
  no error, no question, wrong entity, by pipeline x condition, with a confirmation lever.
- Closest neighbours, with distance labels:
  1. **2605.15104 (From Text to Voice) — NEAR.** Same object (spoken tool calls, TTS voices,
     noise, argument-value failures) but omni-models only, gold-label scoring rather than an
     executed ledger, no entity-type partition, no silent-vs-asked criterion, no telephone
     band, no lever. We must cite it as the benchmark-conversion precedent and state exactly
     which cells we add.
  2. **2609.20152 (MTVA-Bench) — NEAR.** Mock backend executing the arguments actually sent,
     and "most of the gap comes from argument values"; but text-simulated transcription
     issues, no audio, no pipeline comparison, no lever. Cite for the mock-backend scoring
     precedent.
  3. **2605.25404 (Proactive for Uncertainty) — ADJACENT (lever side).** Clarification driven
     by learned error detectors, explicitly positioned against confidence filtering; but no
     read-back confirmation arm, no tool-call ledger, no audio-native arm.
  4. **2608.05126 (Spoken Function Calling) — ADJACENT.** Function calling as the SLU target
     with LLM vs LALM evaluation, but no acoustic grid, no executed ledger, no lever.
  5. **2602.17598 (Cascade Equivalence) and 2605.17443 (Korean SQA) — ADJACENT for D2.**
     They disagree with each other on whether audio-native beats the cascade under noise;
     our D2 must be positioned against both.
- Delineation sentence for the paper: that ASR mis-hears spoken numbers and names, that those
  errors propagate through slot filling and dialogue state tracking, and that WER understates
  the damage is not ours (2402.01931, 2408.00004, 2406.12387, 2108.13048, 2311.07418,
  2608.30348). That spoken tool calling degrades relative to text mostly through argument
  values is also not ours (2605.15104, 2609.20152). What is new in our work is the ledger:
  how often a mis-heard entity becomes a schema-valid call that executes with wrong semantics
  while no error is surfaced and no question asked, how that cell varies across three
  pipelines and a controlled acoustic grid (voices per accent, rate, noise, 8 kHz), whether
  it decouples from WER, and how much read-back confirmation recovers compared with
  confidence/n-best gating and an ask-when-unsure instruction, at what cost in turns.
- Full-text reads required before CP2: 2605.15104 (check whether any table breaks argument
  errors down by numeric vs name and whether any confirmation prompt is used), 2609.20152
  (check how "transcription issues" are simulated and whether any scenario scores a
  confirmation turn), 2608.05126 (check the entity-error claim from the search snippet),
  2605.25404 (check whether a read-back/echo baseline appears).
