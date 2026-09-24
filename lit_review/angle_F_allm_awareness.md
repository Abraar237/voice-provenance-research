# Angle F: What audio LLMs KNOW about synthetic speech (detection, calibration, implicit vs explicit sensitivity)

Scope note: this file maps the AWARENESS side, which is prior work we cite and delineate, not
claim. Our paper's contribution is elsewhere: a matched real-vs-clone audit (same speaker, same
words; REAL / CLONE / RESYNTH / STOCK arms) that measures BEHAVIOURAL provenance deltas
(WER, reading grade, comprehension, assistant reply) alongside an explicit "real or synthetic?"
probe on the same pairs. The papers below tell us (a) how well LALMs can report provenance when
asked (mostly: not, zero-shot), (b) how badly calibrated their confidence is, (c) that LALMs
encode acoustic information they do not act on or report, and (d) how sensitive their judge
behaviour is to paralinguistic cues. None of them measures whether the same model treats a
cloned voice differently from the same speaker's real recording. Papers already tabled in
`candidate_provenance_preemption.md` (ALLM4ADD 2505.11079, AudioTrust 2505.16211, HIR-SDD
2603.10725, LALM spoof-aware ASV 2607.14753, AffectDF 2608.05507, VoxENES 2607.11706,
DETECT-3B-Omni 2607.03418, I Hear Therefore I Trust 2605.28064, Counterfactual Audits
2608.06718) are not duplicated here but are referenced where they anchor a group.

Verification: all 20 ids resolved and abstracts fetched live on 2026-09-24 from
`arxiv.org/abs/<id>` (curl, `citation_title` / `citation_date` meta tags and the abstract
block parsed from the HTML). The arXiv export API and Semantic Scholar rate-limit this host,
so no API batch was used. Titles below are the exact `citation_title` strings. "What it
established" lines are paraphrased from the fetched abstracts, not from memory. One full-text
check was made (TriDF 2512.10652, arxiv.org/html, Sec. on interpretable audio detection) to
confirm the load-bearing "Gemini 2.5-Pro near chance" sentence.

## Group 1: LALMs as deepfake / spoof detectors (zero-shot fails, fine-tuning works)

Anchors already tabled elsewhere: ALLM4ADD 2505.11079 (Qwen-Audio zero-shot 6-18%, SFT to
99.4% on 19LA), AudioTrust 2505.16211 (GPT-4o refuses the task), HIR-SDD 2603.10725, and
2607.14753 (pretrained LALMs near chance on spoof-aware ASV zero-shot).

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2601.00777 | Investigating the Viability of Employing Multi-modal Large Language Models in the Context of Audio Deepfake Detection | 2026 | Qwen2-Audio-7B-Instruct and SALMONN evaluated zero-shot and fine-tuned with binary and question-answer prompts; models "perform poorly without task-specific training and struggle to generalise to out-of-domain data" but reach good in-domain accuracy with minimal supervision. | Detection accuracy only, on standard spoof corpora; no matched real/clone pairs, no behavioural outcome, no comparison of detection with the model's own downstream treatment of the audio. Direct baseline for our O4 probe on Qwen2-Audio. |
| 2602.04535 | HoliAntiSpoof: Audio LLM for Holistic Speech Anti-Spoofing | 2026 | First ALLM framework casting anti-spoofing as text generation over spoofing method, affected attributes and semantic impact; introduces DailyTalkEdit; in-context learning improves OOD generalisation. | A trained detector, not an audit of off-the-shelf models; no measure of whether an untrained assistant's behaviour shifts with provenance. |
| 2603.28021 | Audio Language Model for Deepfake Detection Grounded in Acoustic Chain-of-Thought | 2026 | CoLMbo-DF injects textual low-level acoustic features (prosodic, spectral, physiological) into the prompt so a small open ALLM reasons over evidence; outperforms ALLM baselines; releases a CoT-annotated pair dataset. | Fine-tuned detection with feature scaffolds; nothing on zero-shot deployed models or on implicit behavioural sensitivity. |
| 2601.02983 | Interpretable All-Type Audio Deepfake Detection with Audio LLMs via Frequency-Time Reinforcement Learning | 2026 | SFT with binary labels turns ALLMs into black-box classifiers; vanilla RFT hallucinates rationales; FT-GRPO with ~340K frequency-time CoT demonstrations gives SOTA all-type ADD with grounded rationales. | Training method; no evaluation of untuned models' behaviour; speech is one of four audio types. |
| 2601.23066 | Towards Explicit Acoustic Evidence Perception in Audio LLMs for Speech Deepfake Detection | 2026 | Audio-LLM detectors are "biased toward semantically correlated cues" and overlook fine-grained acoustic artifacts; fake speech with natural semantics bypasses them; SDD-APALLM adds structured spectrograms to expose acoustic evidence. | Establishes semantic dominance in the detection route, not in judging/assisting; no same-speaker same-words pairs. Supports our D5 logic (content held fixed isolates the acoustic channel). |
| 2607.26553 | ThinkOmni: A Reasoning-Driven Omni-Modal LLM Framework for Audio Forgery Detection and Localization | 2026 | Omni-modal LLM with 100K forensic CoT (FACoT), modality-incremental learning and a multi-task loss; joint detection plus temporal localisation with strong cross-dataset generalisation. | Trained forensic system; no audit of deployed assistants; no behavioural outcomes. |
| 2601.03615 | SARA: Stress Test Reasoning in Audio Deepfake Detection | 2026 | Five open ALMs tested under acoustic and linguistic adversarial attacks; acoustic attacks cut reasoning-verdict coherence by 14.2% on average; reasoning-trace coherence detects perturbed audio at 0.78 F1 without the waveform. | Reasoning faithfulness of detectors, not provenance effects on non-detection tasks; no matched clone pairs. |
| 2512.10652 | TriDF: Evaluating Perception, Detection, and Hallucination for Interpretable DeepFake Detection | 2025 | Benchmark of 16 deepfake types across image, video and audio with perception, detection and hallucination axes on frontier MLLMs. Full text (audio section): SALMONN-7B has the highest audio detection accuracy with almost no interpretability; Gemini 2.5-Pro "detection accuracy is nearly at chance levels" while giving the best explanations; Qwen3-Omni-30B-A3B and Phi-4 in between. | Detection only; no behavioural task; forgery types are generic not same-speaker clones. Closest published number for a closed model on the explicit probe: Gemini near chance, which is our D4 baseline. |
| 2608.09593 | MADBench: A Benchmark for Modality-Aware Audio Deepfake Detection | 2026 | Separates speech from environmental-audio forgery; benchmarks SOTA detectors and multimodal LLMs under one protocol; synthetic speech is harder to detect than manipulated background audio, and pretrained detectors fail on both. | Detection accuracy on video-borne audio; no LALM behavioural outcome; no clone-vs-real matched pairs. |

## Group 2: Detection corpora and human baselines relevant to our arms (RESYNTH, STOCK, CLONE)

Anchors already tabled elsewhere: 2605.28064 (humans as detectors), 2607.11706 (VoxENES:
detectors vs LLM-era TTS/VC), 2607.03418 (demographic invariance of a dedicated detector).

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2507.21463 | SpeechFake: A Large-Scale Multilingual Speech Deepfake Dataset Incorporating Cutting-Edge Generation Methods | 2025 | 3M+ samples, 3,000+ h, 40 generators (TTS, VC, neural vocoder), 46 languages; baselines generalise to unseen sets; ablations on generation method, language and speaker variation. | Dedicated detectors, not LALMs; no behavioural or judge outcomes. Its "neural vocoder" partition is the closest precedent for treating RESYNTH as its own arm. |
| 2501.08238 | CodecFake+: Codec-Based Resynthesized Data as a Proxy for Detecting CodecFake Speech | 2025 | Codec re-synthesised speech (31 open codecs) is a valid training proxy for detecting codec-based TTS; taxonomy of codec components predicts detectability. | Detector training; no LALM behaviour. Establishes that codec round-trips carry detectable artefacts, which is why our RESYNTH control is needed and why a null RESYNTH delta would be informative. |
| 2605.26136 | Eroding Trust in Real Speech: A Large-Scale Study of Human Audio Deepfake Perception | 2026 | 35,532 judgments, 1,768 listeners, 138 TTS/VC systems: human accuracy on fakes flat (72.9% to 71.2%) but on REAL speech fell 72.7% to 64.1% since 2021 (skepticism shift); autoregressive LM-based and commercial systems hardest (61-66%); a reference ML detector stays >94.5%. | Humans, not models. Provides the human-side comparator for our O4 probe and the "real speech penalised" framing. |

## Group 3: Calibration, uncertainty and refusal in LALMs

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2604.25591 | Walking Through Uncertainty: An Empirical Study of Uncertainty Estimation for Audio-Aware Large Language Models | 2026 | First systematic UE study for ALLMs: five methods (predictive entropy, length-normalised, semantic entropy, discrete semantic entropy, P(True)) across models; semantic and verification methods beat token-level on general reasoning, but rankings become model- and benchmark-dependent on hallucination / unanswerable settings. | No provenance or deepfake task; no matched pairs. Tells us the O4 probe's verbal confidence cannot be taken at face value and that P(True)-style scoring is the defensible option for the open models. |
| 2604.19300 | HalluAudio: A Comprehensive Benchmark for Hallucination Detection in Large Audio-Language Models | 2026 | 5K+ human-verified QA over speech, sound and music; measures hallucination rate, yes/no bias, error type and refusal rate; broad deficiencies in acoustic grounding. | No synthetic-vs-real axis. Its yes/no-bias and refusal-rate protocol is the template for scoring a binary REAL/SYNTHETIC probe fairly. |
| 2606.24648 | ParaPairAudioBench: Paralinguistic Pairwise Audio Benchmark for LALM-as-a-Judge | 2026 | 5,175 pairs over style, rate, emphasis, age, gender; LALM judges trail humans by 32 points on average with "severe calibration failures" especially on ties; same-transcript vs cross-transcript conditions separate lexical from acoustic reliance. | Judges paralinguistics, not provenance; no real-vs-clone pairs. Same-transcript design is the methodological precedent for our content-fixed pairs. |

## Group 4: Implicit vs explicit: models encode or act on cues they do not report

Anchor already tabled elsewhere: Counterfactual Audits 2608.06718 (judge profiles stable
across TTS vs CAVA human speech, rank-order only).

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2605.13737 | Senses Wide Shut: A Representation-Action Gap in Omnimodal LLMs | 2026 | IMAVB (500 clips, 2x2 modality x premise): hidden states reliably encode premise-perception mismatches even when outputs almost never reject the false claim; gap is audio-worse than vision and prompt-resistant; probe-guided logit adjustment improves rejection. | Premise conflicts, not provenance; no clone pairs. This is the conceptual template for D1/D4: implicit encoding without explicit report. |
| 2609.00727 | Heard but Not Heeded: Paralinguistic Information Encoding and Loss in Audio-Language Models | 2026 | Whisper-large-v2, Qwen2-Audio-7B, Qwen2.5-Omni-7B, Chroma-4B on Expresso: speaking style is strongly encoded in late encoder layers but degraded before output; models split into content-driven and acoustic-driven output behaviour; a leakage metric quantifies the gap between what is encoded and what is used. | Speaking style, not synthetic-ness; no behavioural task. Supplies the mechanism story for a family-dependent sign (content-driven vs acoustic-driven families) and the probing method for a follow-up. |
| 2606.10581 | ParaBridge: Bridging Paralinguistic Perception and Dialogue Behavior in Speech Language Models | 2026 | SLMs recognise paralinguistic cues but ignore them in open dialogue; an inference-time scaffold narrows the perception-behaviour gap, showing the cues are latent; on-policy self-distillation makes it stable (VoxSafeBench SAR 14.6% to 40.3%). | Cues are child voice, fear, noise, not provenance; no real-vs-clone. Documents the "perception-behavior gap" vocabulary we can borrow. |
| 2503.07513 | Language Models Fail to Introspect About Their Knowledge of Language | 2025 | Across 21 open LLMs, prompted metalinguistic answers do not predict the model's own string probabilities beyond what a near-identical model predicts: no privileged self-access; prompted responses should not be conflated with internal knowledge. | Text-only, grammaticality. Cited as the reason an explicit probe is not the same measurement as a behavioural delta. |

## Group 5: LALMs as quality / naturalness judges (what they can say about synthetic speech)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2501.17202 | Audio Large Language Models Can Be Descriptive Speech Quality Evaluators | 2025 | "Most audio LLMs remain unaware of the quality of the speech they process"; first natural-language speech-quality corpus from human MOS; ALLD alignment gives MSE 0.17 MOS and 98.6% A/B accuracy. | Quality, not provenance; needs alignment training. Motivates O2 (grade) as a channel where synthetic artefacts could leak into judgment. |
| 2606.10147 | From Senses to Decisions: The Information Flow of Auditory and Visual Perception in Multimodal LLMs | 2026 | Traces how audio and visual tokens route through Qwen2.5-Omni and Video-SALMONN2 Plus; audio contribution flows in proportion to task reliance; tokens can be dropped after transfer to the LLM with little loss. | Interpretability of routing, no provenance axis. Tooling precedent (attribution of an answer to audio tokens) for a mechanistic follow-up to a positive delta. |

## Closest neighbours (cite and delineate)

1. **TriDF 2512.10652** plus **ALLM4ADD 2505.11079** and **2601.00777** together fix the
   explicit-probe baseline: open ALLMs zero-shot are at or below chance, Gemini 2.5-Pro is
   "nearly at chance", GPT-4o refuses (AudioTrust). Our O4 probe reproduces this on matched
   pairs; the new quantity is the comparison of that near-chance detection with the
   behavioural delta on the same clips (D1, D4).
2. **Senses Wide Shut 2605.13737** and **Heard but Not Heeded 2609.00727** establish the
   "encoded but not used / not reported" pattern for premise conflicts and speaking style.
   Neither touches synthetic provenance. Our claim is the behavioural analogue: the model's
   grade or reply moves with provenance even when its explicit report does not.
3. **ParaPairAudioBench 2606.24648** is the closest judge-audit design (same-transcript pairs,
   calibration-aware scoring) but its axes are style/rate/emphasis/age/gender, never real vs
   synthetic.
4. **CodecFake+ 2501.08238** is the reason the RESYNTH control exists: codec round-trips are
   themselves detectable by trained detectors, so a real-vs-clone delta must be shown to
   exceed the resynthesis delta (D2).
5. **Eroding Trust 2605.26136** gives the human comparator: listeners now misjudge REAL
   speech at 36%, so a model that penalises or flags real speech would be mirroring a
   documented human shift.

## Notes

- Pre-emption assessment for angle F: no verified paper compares an LALM's explicit
  provenance report against its implicit behavioural treatment of the same audio, and no
  detection paper uses same-speaker zero-shot clones of the exact real utterance as the fake
  class. The detection literature evaluates on ASVspoof / SpeechFake-style corpora where the
  bona fide and spoof items differ in content and often in speaker.
- Refusal handling: AudioTrust (GPT-4o) and HalluAudio's refusal-rate axis both argue for
  scoring "refuse" as its own outcome on O4 rather than as an error.
- Seen but not tabled: LOKI 2410.09732 (2024 LMM synthetic-data benchmark incl. audio;
  superseded for our purpose by TriDF), SONAR 2410.04324 (foundation-model detectors
  generalise better than classical ones), 2408.10853 (codec-trained countermeasures reach
  0% EER on ALM-generated audio, relevant to RESYNTH detectability), RTCFake 2604.23742
  (codec/platform distortions in real-time communication), Evaluation of ALMs for Fairness,
  Safety and Security 2603.13262 (taxonomy, semantic invariance under paralinguistic
  variation), the LALM trustworthiness survey 2605.20266 (authentication pillar), and the
  AI-voice detection survey 2608.15411. All abstracts fetched live 2026-09-24.
- Delineation sentence for the paper: that audio LLMs cannot reliably report whether speech
  is synthetic is not ours: ALLM4ADD (2505.11079), 2601.00777 and TriDF (2512.10652) show
  zero-shot detection at or near chance for open and closed models, AudioTrust (2505.16211)
  shows refusal, and the representation-action line (2605.13737, 2609.00727) shows LALMs
  encode acoustic facts they do not act on. What is new in our work is the matched
  measurement: whether the same model's grading, comprehension and assistant behaviour move
  with provenance when speaker and words are held fixed, whether that movement exceeds the
  codec-resynthesis control, and how it compares with the model's own explicit detection
  accuracy on the identical clips.
