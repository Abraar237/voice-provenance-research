# Pre-emption check: "Retracted values: do voice agents execute what the user took back?"

Date: 2026-09-24. Method: four parallel search angles (ASR handling of self-repairs; self-repair in
SLU/DST/tool calling; audio-native vs cascade on disfluent speech; Jan 2025–Sep 2026 recency sweep
including a disfluency check of every voice-agent benchmark we know of), over arXiv listing search,
the arXiv export API, Semantic Scholar and WebSearch. Semantic Scholar and the arXiv export API
rate-limited this host for most of the session (HTTP 429), so every abstract below was verified live
from the arXiv abs page (or the ISCA / medRxiv page where noted); nothing is from memory. The five
closest papers were read in full text (HTML/PDF), and the FDB-v3 PDF was extracted locally with
pdftotext so the quotes are exact.

---

## VERDICT: ALIVE-BUT-CROWDED (the phenomenon is published; the mechanism, the ledger and the levers are not)

The one-sentence version of our hypothesis ("cascades break on mid-utterance self-corrections in
tool calls, audio-native models do better") is already one row of one table in
**Full-Duplex-Bench-v3 (arXiv 2604.04847, posted 2026-04-06)**: on 21 real-audio self-correction
scenarios, the Whisper→GPT-4o cascade scores Pass@1 0.176 against GPT-Realtime's 0.588, and the
case study shows the cascade booking the retracted destination ("Rome"). Two more tool-calling
benchmarks carry a correction condition (Audio2Tool 2604.22821 Tier 6; τ-Elicitation 2609.13602
"self-correction" realism), and two chat benchmarks name the phenomenon exactly (Audio
MultiChallenge 2512.14865 "Voice Editing": "filter out retracted content"; VocalBench-DF
2510.15406 "Correction": "No, wait, I mean").

What nobody has done, verified against all five full texts:

1. **The ledger.** No paper separates "executed the RETRACTED value" from "other wrong" from
   "asked for clarification". Every existing result is a binary pass/fail (Pass@1, EM, Tool-Acc,
   rubric pass). The retracted-value execution rate, the quantity a payments or booking deployer
   actually needs, has never been reported.
2. **The mechanism.** FDB-v3 attributes its cascade failure to streaming endpointing ("Whisper may
   finalize the original (incorrect) transcription before the user's correction arrives"), not to
   transcript normalisation. Nobody has run a whole-utterance (non-streaming) transcript and asked
   whether the reparandum, the repair, or both survive, and which one the LLM then executes. The
   ASR-flattening hypothesis is untested and the streaming confound is unseparated.
3. **The direction is contested, which is good for us.** VocalBench-DF finds the Whisper+GPT-4o
   cascade is MORE robust than 22 Speech-LLMs on its Correction/Restart/Reback items (relative
   accuracy 0.99 vs 0.74/0.48/0.90 average); VoiceBench's "repairs" perturbation costs the naive
   cascade 2.8% vs 18–25% for end-to-end models; Audio2Tool's Tier 1→Tier 6 EM drop is −38.8 for
   text Qwen-8B, −43.6 for Whisper+Qwen-8B, but −67.6 for Qwen-3-Omni-30B; and τ-Elicitation finds
   scripted self-corrections do not detectably change exact success for three audio-native realtime
   agents. FDB-v3 says the opposite. A controlled study that adjudicates this (streaming vs
   whole-utterance, real vs TTS repairs, QA vs executed tool arguments) is open.
4. **The audio-LLM-as-transcriber cascade arm** appears in no paper.
5. **The levers.** No paper tests verbatim-transcription prompting of the ASR stage, a "the user may
   correct themselves; use the final value" instruction, or isolated read-back, on self-repairs.
   (τ-Elicitation's scaffold bundles spelling + read-back + confirm and is not decomposed; Uh-Mazing
   tests ICL/prompt levers but for translation preservation, not execution.)
6. **Repair typology × acoustic condition.** No paper crosses repair type (number / date / name
   replacement, insertion, abandoned-then-restart, late repair after the sentence) with accent,
   telephone band or noise. FDB-v3 has one "self-correction" bucket; Audio2Tool has one tier with no
   breakdown; τ-Elicitation pools six realisms.

The title and abstract must cite FDB-v3 as the origin of the observation and position this as the
mechanism-and-lever study. "Do voice agents execute what the user took back?" is still ours as a
measured quantity; "cascades fail on self-corrections" is not.

---

## Verified papers (23)

| id | title | year | what it established | what it does NOT cover (vs. this candidate) |
|---|---|---|---|---|
| 2604.04847 | Full-Duplex-Bench-v3: Benchmarking Tool Use for Full-Duplex Voice Agents Under Real-World Disfluency (Lin, Chen, Chen, Lee) | 2026-04 | 100 real recordings, 12 speakers, five disfluency categories incl. self-corrections (21/100 scenarios, "updating parameters mid-sentence"); chained mock-API calls in 4 domains; GPT-Realtime, Gemini Live 2.5/3.1, Grok, Ultravox, Whisper→GPT-4o→TTS cascade via LiveKit. Self-correction Pass@1: 0.588 / 0.471 / 0.353 / 0.294 / 0.353 / **0.176**. "Across all systems, self-correction handling ... remain the most consistent failure modes." | (a) Binary Pass@1 only; retracted-value execution appears in one case study (travel_19), never as a rate. (b) Cascade vs native yes, but one cascade, streaming, and the deficit is blamed on endpointing timing; no whole-utterance transcript condition; no audio-LLM-transcriber arm. (c) No levers. No repair typology, no controlled acoustics (telephone band absent), n=21. |
| 2512.14865 | Audio MultiChallenge: A Multi-Turn Evaluation of Spoken Dialogue Systems on Natural Human Interaction (Gosai et al., Scale; ACL 2026) | 2025-12 | New "Voice Editing" axis: "mid-utterance speech repairs and backtracking"; 83 VE conversations of 452, 47 real speakers; rubrics keyed to the corrected value; VE is the hardest axis (avg APR 17.99%; best Gemini 2.5 Flash Thinking 54.22, GPT Realtime 22.89, Qwen3-Omni 30.12). Cascade ablation with whisper-large-v3 + GPT-5 / Claude Opus 4.5 / GPT-4o; TTS ablation (Whisper transcript → gpt-4o-mini-tts) raises VE for text output. | (a) Chat-reply rubric grading, not executed tool arguments; no retracted / other-wrong / asked split. (b) Cascade ablation is aggregate, no VE-specific cascade number; its TTS ablation implies Whisper's transcript makes edits EASIER for text models (opposite sign). (c) No levers, no acoustic manipulation, no repair typology. |
| 2510.15406 | VocalBench-DF: A Benchmark for Evaluating Speech LLM Robustness to Disfluency (Liu et al.) | 2025-10 | Taxonomy incl. Utterance Modification: Reback / Restart / **Correction** ("What is the capital of Italy? No, wait, I mean, what is the capital of France?"); CosyVoice TTS on OpenAudioBench QA; 22 Speech-LLMs. Relative accuracy Correct/Reback/Restart: Whisper+GPT-4o 0.99/1.01/0.99, Speech-LLM avg 0.74/0.90/0.48; failure = "anchoring early to false starts". | (a) QA accuracy; no tool calls, no slot values, no retracted-answer category (one qualitative case). (b) One cascade, and the result is cascade-robust / native-fragile, the reverse of our hypothesis. (c) Component swaps only (ASR, LLM size), no prompting or read-back. Synthetic speech only. |
| 2604.22821 | Audio2Tool: Speak, Call, Act: A Dataset for Benchmarking Speech Tool Use | 2026-04 | 30k TTS (Qwen3TTS, CosyVoice-3 voice clones) queries, 7 tiers; **Tier 6 Correction** ("Set an alarm for 7...wait, make it 8"), 4,560 items. Tier 6 Tool-Acc/EM: text Qwen-8B 75.2/46.8, whisperv3+Qwen-8B 61.8/34.5, whisperv3+Gemma-27B 77.1/44.1, Qwen-2.5-Omni-7B 68.3/42.0, Qwen-3-Omni-30B 81.5/24.8; noise ablations (babble/hum/impulsive at +15/+5/−5 dB). | (a) Tool-Acc / EM / Slot-F1 only; no analysis of whether the wrong slot was the retracted value; clarification not scorable. (b) Whisper cascade vs SpeechLM rows exist but the correction-specific loss is not isolated from general ASR loss, and the largest collapse is the audio-native Qwen-3-Omni (EM 92.4→24.8). (c) No mitigations; Tier 6 not crossed with noise; no real repairs, no prosody. |
| 2609.13602 | τ-Elicitation: Benchmarking Multi-Turn Entity Extraction in Voice Agents | 2026-09 | 200 elicitation tasks, 10 entity types, six scripted caller realisms incl. "self-correction supplies a wrong value and immediately repairs it" and "falter-and-restart"; gpt-5.5 caller + ElevenLabs; agents gpt-realtime-2, gemini-3.1-flash-live, grok-voice. "No assigned realism detectably changes exact success" (−3.6, CI [−10.4, 3.0]). Scaffold (ask/spell/read back/confirm/correct) +14–31 Pass³. | (a) Exact-entity success; no retracted-vs-repaired ledger; realisms pooled. (b) "intentionally omit caller-side ASR": no cascade of any kind. (c) Read-back only inside a bundle; no verbatim prompting or final-value instruction. Elicitation loop with spelling, not single-utterance commands. |
| 2410.17196 | VoiceBench: Benchmarking LLM-Based Voice Assistants | 2024-10 | Content variations incl. "repairs" ("What's the nocebo... I mean, the placebo phenomenon?"), GPT-4o rewrite + Google TTS. Repairs are the most damaging content perturbation: Naive cascade −2.76%, DiVA −5.99%, Qwen2-Audio −10.4%, LLaMA-Omni −17.9%, Mini-Omni −18.1%, VITA −24.6%. | (a) QA scores; no check of retracted vs corrected content, no tool calls. (b) Cascade is one "naive" baseline; again cascade-robust. (c) No mitigation. Older open models. |
| 2510.07838 | Full-Duplex-Bench-v2 (ACL 2026) | 2025-10 | Four task families incl. **correction** (cross-turn revisions, "make it hot"), TTS examiner, rubric 1–5; full-duplex systems "struggle to handle corrections smoothly"; GPT-Realtime 4.02 vs Moshi 2.88. | Cross-turn, not within-utterance repairs; no tool calls; no cascade; pacing is the only factor. |
| 2603.16783 | SpokenUS: A Spoken User Simulator for Task-Oriented Dialogue | 2026-03 | SpokenTOD 52k dialogues / 1,034 h with disfluency templates incl. Correction ("book it for Monday, [COR] Tuesday") and Restart, placed "in a local window around slot values"; agents GPT-4.1-mini cascade and Qwen2.5-Omni-7B; cascade final slot F1 −24.3 on SpokenUS input; "agents tend to accept ASR's erroneous transcription of slot values rather than requesting confirmation, especially when those values are accompanied by disfluencies." | (a) Slot F1 aggregate; no retracted-vs-repaired split; disfluency not isolated from barge-in/cross-turn/emotion. (b) Two agents, no per-behaviour cascade-vs-native contrast. (c) None. Reusable as a source of templated slot repairs. |
| 2608.03970 | Should We Type or Talk to LLM Agents? (HIVE) | 2026-08 | Text-only verbalizer perturbations; spoken-casual register carries "false starts and self-corrections"; "it is the structure of the transcription rather than its fillers that carries the cost"; thinking budget does not rescue spoken registers; LoRA adaptation trades clean accuracy. | Text only ("acoustic branch ... not in the reported runs"); QA benchmarks, "nothing in the suite exercises a multi-turn or tool-using agent"; no retracted-value analysis; levers are thinking/LoRA. |
| 2609.20152 | MTVA-Bench: Evaluating the Language Model Inside Cascaded Voice Agents | 2026-09 | LM tested under cascade conditions (transcription issues, split turns), mock backend executes the arguments actually sent; "most of the gap comes from argument values". | Text-simulated caller; 0 hits for self-correction/repair; no audio-native arm; no lever. Instrumentation model for our executed-argument checks. |
| 2605.15104 | From Text to Voice: Evaluating Tool Calling LLM Agents | 2026-05 | TTS of Confetti/When2Call with speaker variation + 5–20 dB noise; 7 omni models; argument-value errors 39–57% of failures; clean text / direct voice / ASR cascade compared. | No self-correction condition at all (0 hits); no levers on repairs. |
| 2608.05126 | Spoken Function Calling (SFC-Bench) | 2026-08 | SLU as function calling; synthetic data where a "speech agent" injects "spoken language features (e.g., redundancy, self-corrections)". | Self-corrections injected but never analysed; no retracted-value measure; no cascade-vs-native on corrections; no lever. |
| 2608.02138 | The Role of Disfluencies in Speech Translation (Uh-Mazing) (Züfle et al.) | 2026-08 | Switchboard EDITED/INTJ/PRN into 8 languages; "false starts and self-repairs ... drive most of the translation-quality loss"; "models which fail to preserve a disfluency tend to omit it rather than mistranslate it" (1,098 deletion spans vs 446 mistranslations); cascades (Whisper/Canary + Llama/Tower) beat OWSM, Phi-4, Qwen2.5-Omni; ICL raises chrF up to 5 pts, disfluency-aware prompt has minimal effect. | Target is preservation of the disfluency, not resolution; does not distinguish reparandum from repair; translation, no tool calls; levers tested on text MT models, not on the ASR stage. |
| 2607.18934 | Transcription Policy as a Latent Variable: Controllable Verbatim ASR (Wagner, Zusag, Thallinger) | 2026-07 | ASR models "treat transcription style (verbatim vs. intended) as an uncontrolled latent variable", causing beam divergence and "up to 60% of reported WER attributable to style mismatch"; task tokens raise disfluency F1 10%→79%. | Self-corrections lumped as "other" with no score; no downstream LLM; control via training tokens, not prompting a deployed Whisper / GPT-4o-transcribe. Mechanistic support for our ASR-stage premise. |
| 2408.16589 | CrisperWhisper: Accurate Timestamps on Verbatim Speech Transcriptions | 2024-08 | Whisper fine-tuned "to produce more verbatim speech transcriptions"; SOTA on verbatim transcription and filler detection. | Verbatimness measured on fillers/segmentation, not reparandum+repair survival; no downstream. A ready-made verbatim-ASR arm. |
| 2505.23627 | Prompting Whisper for Improved Verbatim Transcription and End-to-end Miscue Detection | 2025-05 | "incorporating reading text through prompting benefits verbatim transcription performance over fine-tuning" (children's read-aloud, atypical adult speech). | Prompt is the target reading text, not a style instruction; no free-form repairs; no downstream. Precedent that Whisper prompting shifts verbatimness (our lever). |
| 2307.09378 | Adapting an ASR Foundation Model for Spoken Language Assessment (Cambridge) | 2023-07 | Whisper "designed to be human readable ... these models have a tendency to skip disfluencies and hesitations in the output"; fine-tuning and soft-prompt tuning make it "generate the exact words spoken". | Assessment use; no self-repair category, no downstream action, no audio-native comparison. The canonical citation for "Whisper normalises". |
| 2503.06924 | ASR for Non-Native English: Accuracy and Disfluency Handling (McGuire) | 2025-03 | Five ASR systems on L2-ARCTIC; "revisions" transcribed verbatim with accuracy ~0.81 (RevAI, Deepgram, Whisper-large-v3), 0.77 Speechmatics, 0.61 AssemblyAI; a "um, uh" initial prompt to Whisper caused a hallucination. | Verbatim-fidelity of revisions in L2 speech, not which value survives into an action; no LLM, no native arm. Useful prior: stock Whisper often keeps BOTH reparandum and repair, so the downstream LLM sees "fifty fifteen". |
| 2508.13060 | Evaluating ASR robustness to spontaneous speech errors: WhisperX on SFUSED | 2025-08 | ~5,300 annotated slips with intended vs actual production and speaker corrections; WhisperX (large-v2) outputs classified Corrected / Faithful / Incorrect; for word errors human correction raised Corrected +10.9% but Incorrect +13.3%. | Slips of the tongue, not deliberate value changes; ASR only. |
| 2606.31112 | What Counts as an Error? Dual-Reference Benchmarking for Atypical ASR | 2026-06 | 11 ASR models scored against verbatim and intended references; "Most ASR evaluations ... reward systems that delete disfluencies"; rankings flip by reference. | Stuttering, not lexical self-repairs; no downstream. Supports the framing that evaluation norms reward deletion. |
| 2509.20321 | Conversational Speech Reveals Structural Robustness Failures in SpeechLLM Backbones (DRES) | 2025-09 (v2 2026-03) | Gold Switchboard deletion-only probe of text backbones; "reasoning models systematically over-delete fluent content"; fine-tuning hurts generalisation. | Human verbatim transcripts as input (ASR flattening excluded by design); deletion P/R, not executed values; no audio. The "text LLM can in principle repair" baseline. |
| 2106.04016 | Disfl-QA (Gupta et al.) | 2021-06 | Human-inserted contextual disfluencies (incl. corrections) into SQuAD; SOTA QA "degrades significantly" zero-shot; augmentation partially recovers. | Text-only, pre-LLM, no audio, no tool calls. Foundation citation for "text LLM must resolve repairs". |
| 2601.12973 | Pardon? Evaluating Conversational Repair in Large Audio-Language Models (Findings ACL 2026) | 2026-01 | "Repair" = model-initiated clarification on unanswerable audio; EAR score; most LALMs fail to initiate repair. | Different sense of repair (other-initiated); relevant only to our "asked for clarification" cell. Name-collision risk in related work. |
| cs/0008016 | Processing Self Corrections in a speech to speech system (Spilker et al., Verbmobil) | 2000 | Acoustic-first repair hypothesis generation, stochastic correction, lattice parser accepts the repair. | Pre-neural; establishes that acoustics carry repair cues and that a system must delete the reparandum before acting. Historical anchor for the prosody arm. |

Also verified live but peripheral (not in table): 2601.19952 LTS-VoiceAgent (Pause-and-Repair benchmark stresses streaming cascades; no slot outcome), 2607.28175 AgenticASR (audio-to-clean-text that "resolves self-corrections"; a candidate baseline transcriber, no downstream eval), 2605.12242 Mind the Pause (Indic disfluency rewrite), 2606.19595 IHBench (agent-turn interruptions), 2604.16456 EchoChain (interruptions), 2603.13686 τ-Voice (no repair condition), 2510.07978 VoiceAgentBench (no disfluency), 2311.00867 Romana et al. (Whisper drops disfluencies; acoustic detection beats transcript), 2510.10444 LISTEN (audio LLMs are lexically dominated: a caution for the prosody hypothesis), 2506.04076 hesitation tagging, Interspeech 2025 J-j-j-just Stutter, DiSS 2025 Ferreira et al., medRxiv 10.64898/2026.08.21.26360471 (self-repair detection on DementiaBank transcripts, GPT-5 F1 0.73), FluencyBank Timestamped (JSLHR 2024).

Benchmarks checked for a self-correction condition: YES: FDB-v3, Audio2Tool (Tier 6), τ-Elicitation (realism), VocalBench-DF, VoiceBench, Audio MultiChallenge, FDB-v2 (cross-turn), SpokenUS, SFC-Bench (injected, unanalysed). NO: VoiceAgentBench, BFCL Audio, AudioBench, VocalBench, SpeechGym, From Text to Voice, MTVA-Bench, τ-Voice, EVA-Bench.

UNVERIFIED (search snippets only, excluded): "AgentChangeBench (Rana et al., 2025)" cited in FDB-v3 for text-based goal shifts; Lacuna/Tiptree "speech-first repair detection" web page; HuggingFace blog "FluentWhisper" (2026-06-15, LoRA disfluency-removing Whisper; states "self-repairs are fixed correctly only about 40% of the time, and the model often keeps both the false start and the correction", but this describes the fine-tuned adapter, not stock Whisper, and is not peer-reviewed).

---

## Full-text notes on the closest papers

### 1. Full-Duplex-Bench-v3 (2604.04847), Lin, Chen, Chen, Lee; posted 2026-04-06, "work in progress"

Setup (verbatim, from the PDF): "Consider a user who says, 'Book me a flight um... to New York—actually, wait... make that Boston.' A robust agent must discard the earlier destination and update its internal state before issuing the booking call." "Twenty-one of our 100 scenarios test whether models can recognise a mid-utterance change of intent and correctly update downstream API parameters." All six systems "are deployed through the LiveKit Realtime Voice Agent framework for streaming audio and real-time tool use"; the cascade is "OpenAI Whisper for speech recognition, GPT-4o for reasoning and tool use, and OpenAI TTS" (checkpoint unspecified). Recordings: 12 speakers (native, Korean- and Russian-accented), built-in microphones, "quiet rooms to settings with mild background noise". Metrics: Tool Selection F1, Argument Accuracy ("semantic correctness of generated arguments, judged by GPT-4o"), Pass@1 (all tools exact and perfect argument accuracy).

Self-correction result (Table 3, Pass@1 on the 21 items): GPT-Realtime 0.588, Gemini Live 2.5 0.471, Gemini Live 3.1 0.353, Grok 0.294, Ultravox 0.353, Cascaded 0.176. "The core challenge is that models commit intermediate parameters before the correction arrives, and reliable rollback requires distinguishing provisionally set values from explicitly confirmed ones." Cascade paragraph: "The gap is starkest on self-corrections: Cascaded scores only 0.176—the lowest of all systems—versus GPT-Realtime's 0.588. Because Whisper may finalize the original (incorrect) transcription before the user's correction arrives, the downstream LLM has no opportunity for state rollback."

Case study travel_19 (Rome→Milan, June 1→June 3): "Only GPT-Realtime correctly applies both corrections." "Gemini Live 3.1's ... tool-call latency of −2.27 s means the API was invoked before the user finished correcting, locking in destination='Rome' (the original, uncorrected value). The Cascaded pipeline also uses 'Rome,' but for a different reason: Whisper finalizes the initial transcription before the correction arrives, so the downstream LLM never receives the updated intent."

(a) Retracted vs repaired execution measured? **No.** Binary Pass@1; the retracted value is shown only in one case study. No count of how many of the 17 cascade failures (or 7 GPT-Realtime failures) executed the retracted value vs something else vs asked. (b) Cascade vs audio-native? **Yes**, but one streaming cascade, and the paper's own explanation is endpointing/finalisation timing, which is a streaming-architecture artefact, not ASR normalisation. There is no whole-utterance transcript, no transcript-level analysis, no audio-LLM transcriber. (c) Levers? **None.** No prompting variants, no verbatim mode, no confirmation. Limitations section is about latency and mock APIs only. Also: no repair typology, no telephone band, no SNR, no per-accent split, no prosody discussion.

### 2. Audio MultiChallenge (2512.14865), Gosai et al. (Scale AI); ACL 2026

"Voice Editing" = "the model's ability to recognize and apply immediate, spontaneous speech repairs, such as mid-utterance self-corrections or implemented planned edits that span multiple turns"; models must "dynamically filter out retracted content". 83 of 452 conversations; unscripted real speakers (47), 48 kHz, no post-processing; example "Let's make it four yuccas, hmm no six"; resort-booking example corrects a departure date 13th→12th and switches resorts, rubric "Mentions check-in date is Friday 11/14". Scoring: binary rubric pass on the spoken/text reply, LLM judge. VE is the hardest axis (avg 17.99% APR); best models 40–54%; VE degrades with history length (17.5% at 3–5 min → 0% at 8+ min). Cascade: "For all cascaded experiments, we use the same transcripts obtained from whisper-large-v3 as the text input to the LLMs" (GPT-5, Claude Opus 4.5, GPT-4o); "cascading reduces performance for Gemini 3 Pro Preview and Gemini 2.5 Pro, with relative drops of 10.3% and 4.9%, while Gemini 2.5 Flash Thinking improves by 10.0%" (aggregate, not VE-specific). TTS ablation: "synthetic versions of our human user audio, generated by first performing ASR using whisper-large-v3 followed by TTS"; VE gains +11.5% relative under text output, which they attribute to "the inability of ASR and TTS to fully capture human-like hesitations and unintelligible segments".

(a) **Partial.** Rubrics require the repaired value but there is no retracted / other / asked ledger, and no tool calls. (b) **Partial.** Cascade vs E2E only in aggregate; the TTS ablation actually suggests a Whisper-cleaned rendition makes edits easier for text-output models, which cuts against our hypothesis and must be engaged. (c) **No levers.** No acoustic manipulation, no repair typology, no prosody analysis.

### 3. VocalBench-DF (2510.15406), Liu et al.

Text-level edits then CosyVoice TTS on 2,300 OpenAudioBench QA items; nine subtypes. Correction = "What is the capital of Italy? No, wait, I mean, what is the capital of France?"; Restart = irrelevant content then "Let's start over"; Reback = return to an earlier question. Table 4 relative accuracy (Correct / Reback / Restart): Whisper+GPT-4o 0.99 / 1.01 / 0.99; Speech-LLM average 0.74 / 0.90 / 0.48. "Whisper+GPT-4o maintains accuracy across all three modification types, with performance comparable to the normal setting, whereas Speech-LLMs degrade under the same conditions." Failure described as "anchoring early to false starts rather than reconciling them with the final query"; one case (VocalNet-1B) answers the retracted question. Interventions: swapping ASR (Wav2Vec vs Whisper-large-v3) and LLM (GPT-4o-mini vs GPT-4o) only.

(a) **No.** QA accuracy, no tool calls, no retracted-answer category beyond one example. (b) **Yes, one cascade, opposite direction**: whole-utterance Whisper on a TTS-rendered "No, wait, I mean" keeps the structure and GPT-4o resolves it. This is the strongest published evidence that ASR normalisation does NOT delete a clearly-voiced repair when the whole utterance is transcribed at once; it was obtained with synthetic speech and a question-level swap, not a value-level repair inside a command. (c) **No levers.**

### 4. Audio2Tool (2604.22821)

30k LLM-generated queries rendered with Qwen3TTS / CosyVoice-3 voice clones; Tier 6 Correction "Handling mid-utterance revisions and state corrections; e.g., 'Set an alarm for 7...wait, make it 8.'", 4,560 items. Table 3 Tier 1 → Tier 6 (Tool-Acc / EM): text Qwen-8B 85.6/85.6 → 75.2/46.8; whisperv3+Qwen-8B 78.1/78.1 → 61.8/34.5; whisperv3+Gemma-27B 87.9/87.9 → 77.1/44.1; Qwen-2.5-Omni-7B 79.5/79.5 → 68.3/42.0; Qwen-3-Omni-30B 92.4/92.4 → 81.5/24.8. The paper does not state whether text rows receive the correction text verbatim. Noise ablations (babble, hum, impulsive at +15/+5/−5 dB) are not crossed with Tier 6.

(a) **No.** Tool-Acc/EM/Slot-F1; no analysis of which value was executed; no clarification path. (b) **Rows exist, no isolation.** The extra EM loss of the Whisper cascade over text on Tier 6 (−43.6 vs −38.8) is about 5 points, while the audio-native Qwen-3-Omni loses 67.6; the correction-specific cascade penalty is small and unanalysed. (c) **None.** All TTS; no real repairs; no prosody.

### 5. τ-Elicitation (2609.13602), posted 2026-09-11 (short note; full read in `preemption_fulltext.md`)

Six scripted caller realisms include "self-correction supplies a wrong value and immediately repairs it" and "falter-and-restart" (mid-string correction while spelling). "No assigned realism detectably changes exact success in either arm ... −3.6 points (95% CI [−10.4, 3.0])". Agents are audio-native realtime only; "intentionally omit caller-side ASR". The scaffold (ask / spell or read back / confirm / correct) is not decomposed. No retracted-value analysis.

(a) No. (b) No cascade. (c) Read-back only inside a bundle. Their null result for scripted TTS self-corrections on audio-native agents is a prior we must either replicate or overturn in the single-utterance command regime.

---

## Novelty delineation (what is known vs what is ours)

We want to be clear about what is already known. That self-corrections are the hardest disfluency
class for voice agents is not ours: FDB-v3 shows it on real audio with tool calls, Audio
MultiChallenge shows it in multi-turn chat, VoiceBench and VocalBench-DF show it in spoken QA, and
Uh-Mazing shows self-repairs drive most of the loss in speech translation. That a streaming cascade
can commit the retracted value is not ours: FDB-v3's travel_19 case shows the cascade and Gemini
Live 3.1 both booking "Rome". That Whisper's transcription style is an uncontrolled verbatim vs
intended latent (2607.18934) and that Whisper tends to skip disfluencies (2307.09378) are known.
That read-back scaffolds recover entity errors in audio-native agents is τ-Elicitation's.

What is new here:

1. **The retracted-value ledger as a rate.** Per call: executed repaired value / executed RETRACTED
   value / other wrong / asked for clarification, on executed, schema-checked mock tools. No paper
   reports the second cell. It is the number a payments or booking deployer needs and the number that
   distinguishes "the agent heard a correction and got confused" from "the agent did exactly what the
   user withdrew".
2. **Mechanism isolation.** The same clip through (i) whole-utterance Whisper (no endpointing),
   (ii) streaming Whisper with VAD endpointing, (iii) an audio-LLM transcriber (GPT-4o-transcribe /
   Gemini as ASR), (iv) audio-native tool calling. Transcript-level scoring of whether the reparandum,
   the repair, both, or neither survive, paired with what the LLM then executes. This separates
   FDB-v3's timing explanation from the normalisation hypothesis, and adjudicates the contradiction
   between FDB-v3 (cascade worst) and VocalBench-DF / VoiceBench / Audio2Tool (cascade fine or best).
   The audio-LLM-transcriber arm is absent from every paper.
3. **Repair typology.** Replacement of number / date / name, insertion, abandoned-then-restart, and
   late repair after the sentence ("...to Priya. Sorry, fifteen."), with the editing term present or
   absent ("fifty, fifteen" vs "fifty, no wait, fifteen"). FDB-v3, Audio2Tool and τ-Elicitation each
   have a single undifferentiated bucket.
4. **Acoustic crossing.** Repair type × accent (multiple voices per accent, two TTS families, plus a
   real-speaker subset) × telephone band (8 kHz mu-law, absent everywhere) × fixed-SNR noise. Only
   Audio2Tool has controlled SNR and it is not crossed with corrections.
5. **Levers on the repair problem specifically.** Verbatim-transcription prompting of the ASR stage
   (keep disfluencies), a "the user may correct themselves; use the final value" instruction to the
   LLM, and isolated read-back confirmation, each scored on recovery fraction AND on the bill for
   calls that were already right. No paper tests any of these on self-repairs.
6. **Prosody test for the audio-native arm.** Whether audio-native models use the acoustic cue at all:
   the same text with the editing term removed and only the prosodic break marking the repair, with
   LISTEN (2510.10444) as the caution that audio LLMs are lexically dominated.

---

## Counter-signals the design must absorb

- The published direction is split. FDB-v3 (streaming, real speech, tool calls): cascade worst.
  VocalBench-DF (whole-utterance, TTS, QA): cascade best. Audio2Tool (whole-utterance, TTS, tool
  calls): cascade penalty small, audio-native collapse large. VoiceBench (TTS, QA): cascade barely
  affected. The likely reconciliation is that whole-utterance Whisper keeps a clearly voiced
  "no wait" and text LLMs resolve it, while streaming endpointing and unvoiced (prosody-only) repairs
  are where the retracted value leaks. Pre-register this as the primary hypothesis rather than the
  bare "ASR deletes repairs" claim, which McGuire 2025 (revisions transcribed ~81% verbatim by
  Whisper-large-v3) already makes unlikely as a blanket statement.
- τ-Elicitation's null for scripted self-corrections on audio-native realtime agents means the
  audio-native arm may show a small effect; the interesting cells are then the streaming cascade,
  the editing-term-absent repairs, and the telephone band.
- Audio MultiChallenge's TTS ablation (Whisper transcript → TTS improves Voice Editing for text
  output) suggests ASR can act as a cleaner that helps. Our verbatim-prompting lever might therefore
  hurt: report it either way.
- "Repair" collides with 2601.12973's usage (model-initiated clarification). Use "self-repair" and
  "retracted value" consistently.

## Must be cited on the first page

FDB-v3 (2604.04847), Audio MultiChallenge (2512.14865), VocalBench-DF (2510.15406), Audio2Tool
(2604.22821), τ-Elicitation (2609.13602), VoiceBench (2410.17196) for the repairs perturbation,
2607.18934 and 2307.09378 for the ASR-style premise, Disfl-QA (2106.04016) and Shriberg-style
reparandum/repair structure (via DRES 2509.20321 / Uh-Mazing 2608.02138) for terminology.

## Working title proposal (needs user approval)

"Did You Mean Fifteen? Where Voice Agents Execute the Value the Caller Took Back." Headline order:
(A) the retracted-value ledger across four pipelines on the same clips, with the
whole-utterance vs streaming split that reconciles FDB-v3 with VocalBench-DF; (B) repair type ×
telephone band × noise; (C) the three levers with recovery fraction and false-positive bill.
