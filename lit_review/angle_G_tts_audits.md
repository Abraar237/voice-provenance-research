# Angle G: Audio-LLM bias/fairness audits built on TTS stimuli, audio-LLM-as-judge, benchmark construction (TTS vs real), and codec/noise robustness

Scope note: this file maps the literature whose METHOD depends on the assumption our paper
tests. Bias audits of speech LLMs overwhelmingly render their stimuli with TTS (or with
zero-shot clones of a few real speakers) and treat synthetic-ness as inert; judge papers
put an audio LLM in the grader role and validate it on mixed real/synthetic corpora;
benchmark papers mix TTS and real subsets and, in two cases, report that models score
synthetic subsets differently. None of them holds SPEAKER and CONTENT fixed across a
real recording and a clone of that same speaker, none has a codec-resynthesis control,
and none pairs a behavioural delta with an explicit "real or synthetic?" probe. Papers
already tabled in `candidate_provenance_preemption.md` (2512.14865, 2608.06718,
2602.01030, 2605.00969, 2604.17248, 2505.16211, 2505.11079, 2609.04256, 2604.11594) are
cited here where relevant but not re-tabled, except 2604.11594 whose critique of TTS
benchmarks belongs to this angle.

Verification: every abstract below was fetched live from `arxiv.org/abs/<id>` on
2026-09-24 (the arXiv export API and Semantic Scholar rate-limit this host; the abs pages
do not). Titles and years are copied from the `citation_title` / `citation_date` meta
tags. The "stimuli" column (TTS / real / both) was checked against the arXiv HTML full
text of each paper, not inferred from the abstract; the TTS engine named in the column
is the one the paper names. "What it established" is paraphrased from the fetched
abstract.

Headline count for the significance statement: of the 21 audio-LLM bias/fairness audits
tabled below (19 here plus BiasInEar and VIBE from the pre-emption file), **16 use
synthetic stimuli only** (15 stock-voice or clone TTS in this file plus BiasInEar), 3 use
real speech only (VIBE, RedVox, 2604.21276), and 2 use both but with different speakers
in the two arms (2608.13624 and our own voice-judge paper). Four of the 16 (MedVoiceBias,
The Voice Behind the Words, the interactive intersectional study, BiasInEar's validity
check) clone real speakers and then never run the original recordings. Zero of 21
compare a real recording with a synthetic rendering of the same speaker saying the same
words.

## G1. Bias / fairness audits of audio LLMs with TTS-only stimuli

| id | title | year | stimuli | what it established | what it doesn't cover |
|---|---|---|---|---|---|
| 2407.06957 | Listen and Speak Fairly: A Study on Semantic Gender Bias in Speech Integrated Large Language Models | 2024 | TTS only (Azure, Google, Amazon; one male + one female voice each; TTSMaker for Chinese) | Spoken bias toolkit over four tasks (speech translation, spoken coreference, sentence continuation, spoken QA); gender-bias levels are language-dependent and vary with the evaluation method; Qwen-Audio-Chat, SALMONN, WavLLM plus Whisper+LLM cascades. | Stock commercial voices only; no real recordings run through the models; no provenance axis; no grading, comprehension or assistant-behaviour outcomes; no detection probe. |
| 2408.07665 | Spoken Stereoset: On Evaluating Social Bias Toward Speaker in Speech Large Language Models | 2024 | TTS only (Azure, three male + three female voices for gender; Topmediai for age) | 2,847 audio prompts with stereotypical / anti-stereotypical / irrelevant continuations; most SLLMs (Qwen-Audio-Chat, LTU-AS, SALMONN 7B/13B) show minimal bias, some slight stereotypical or anti-stereotypical tendencies. | The demographic cue is entirely a TTS voice label; no real speaker; no synthetic-vs-real comparison; MCQA only. |
| 2509.21108 | VoiceBBQ: Investigating Effect of Content and Acoustics in Social Bias of Spoken Language Model | 2025 | TTS only (Kokoro-TTS, 16 voices: 2 genders x 2 accents x 4 speakers) | Spoken BBQ with per-axis content vs acoustic bias scores; LLaMA-Omni resists acoustic bias but amplifies gender and accent bias, Qwen2-Audio dampens acoustic cues while preserving content fidelity. | Separates content from acoustics but not real from synthetic; every voice is Kokoro; no provenance axis. |
| 2509.21125 | Acoustic-based Gender Differentiation in Speech-aware Language Models | 2025 | TTS only (Kokoro-TTS, 4 male + 4 female default voices) | 9,208 samples in gender-independent / stereotypical / dependent categories; LLaMA-Omni family gives male-oriented answers on stereotypical questions yet ignores gender when it would be appropriate; traced to Whisper encoders producing male-oriented acoustic tokens. | Synthetic voices only; the encoder-level explanation is never tested on real speech; no provenance axis. |
| 2510.02398 | When Voice Matters: Evidence of Gender Disparity in Positional Bias of SpeechLLMs | 2025 | TTS only (Azure voices on Spoken StereoSet subset; OrpheusTTS for a second benchmark) | First token-level probabilistic study of positional bias in SpeechLLM MCQA bias benchmarks (Qwen2-Audio-7B-Instruct); positional bias is real in speech and stronger for female voices; concludes MCQA benchmarks do not account for speech-based bias. | Single model; synthetic voices only; no real-speech arm; no provenance axis. |
| 2510.01254 | Do Bias Benchmarks Generalise? Evidence from Voice-based Evaluation of Gender Bias in SpeechLLMs | 2025 | TTS only (Amazon Polly + ElevenLabs, 20 voices, 10 M / 10 F) | LoRA-induces stereotypical / anti-stereotypical / neutral MCQA behaviours in Qwen2-Audio, LTU-AS, LLaMA-Omni and shows they do not transfer to other MCQA benchmarks or long-form generation; proposes a transferability suite. | Authors flag that "TTS-generated voices may lack the natural variability of human speech" but never test it; no real recordings; no provenance axis. |
| 2510.02352 | Evaluating Bias in Spoken Dialogue LLMs for Real-World Decisions and Recommendations | 2025 | TTS only (Index-TTS + ElevenLabs multilingual v2 library voices) | FairDialogue: Group Unfairness Score for decisions, SNSR for recommendations, across Qwen2.5-Omni, GLM-4-Voice, GPT-4o Audio, Gemini-2.5-Flash; closed models less biased, open models sensitive to age and gender, recommendation tasks amplify disparities, bias persists over multi-turn negative feedback. | Every age / gender / accent cue is a TTS library voice; no real speaker, no clone, no synthetic-vs-real check; no detection probe. This is the paper our significance statement names as "silently assuming synthetic-ness is inert". |
| 2509.22061 | Speak Your Mind: The Speech Continuation Task as a Probe of Voice-Based Model Bias | 2025 | TTS only (Azure voices from Spoken StereoSet plus 150 GPT-5-written prompts rendered with Azure) | First bias evaluation of speech continuation (SpiritLM, VAE-GSLM, SpeechGPT): gender effects on agency and polarity once coherence is high; continuations revert to modal phonation more for female prompts. | Authors state all prompts "are synthetically generated and may lack the natural variability of real human speech"; no real arm; no provenance axis. |
| 2511.06592 | MedVoiceBias: A Controlled Study of Audio LLM Behavior in Clinical Decision-Making | 2025 | TTS only (Sesame-1B cloning voice profiles drawn from Common Voice; 36 profiles across age, gender, emotion) | 170 clinical cases; surgical recommendations differ by up to 35% between audio and identical text, one model gives 80% fewer; age disparities up to 12% between young and elderly voices survive chain-of-thought; DeSTA2.5-Audio, Qwen2.5-Omni 3B/7B, Gemini Flash 2.0/2.5, GPT-4o-mini-audio. | Clones real Common Voice profiles but never runs the original recordings; the audio-vs-text gap it reports is confounded with synthetic provenance, which it does not isolate; no codec control; no detection probe. |
| 2603.16941 | The Voice Behind the Words: Quantifying Intersectional Bias in SpeechLLMs | 2026 | TTS only (MegaTTS3 zero-shot clones of EdAcc speakers, six accents x two genders) | 2,880 controlled interactions on LFM2-Audio-1.5B, OmniVinci, Qwen3-Omni-30B; Eastern-European-accented, especially female-presenting, voices receive lower helpfulness; LLM judges catch the direction, humans are more sensitive. | Only the clones are run; the real EdAcc recordings the clones came from are never evaluated, so accent and gender effects are measured entirely inside the synthetic condition; no provenance axis. Closest design to our CLONE arm without the REAL arm. |
| 2604.13067 | From Seeing it to Experiencing it: Interactive Evaluation of Intersectional Voice Bias in Human-AI Speech Interaction | 2026 | TTS only (MegaTTS3 voice-cloning TTS conditioned on EdAcc references) | Distinguishes quality-of-service disparities from content-level bias; accent x gender disparities in alignment and verbosity across three SpeechLLMs; voice conversion lets users experience identical content through different identities (N=24, N=19). | Same MegaTTS3 clone-only instrument as 2603.16941; no real recordings through the models; no provenance axis. |
| 2604.14548 | VoxSafeBench: Not Just What Is Said, but Who, How, and Where | 2026 | TTS (CosyVoice3; "most audio is synthesized rather than naturally spoken") | Two-tier safety / fairness / privacy benchmark, 22 tasks, bilingual; frontier SLMs (Qwen3-Omni, Mimo-Audio, Kimi-Audio, Gemini-3-Pro/Flash, GPT-4o-Audio) detect the acoustic cue yet fail to act on it: a "speech grounding gap". | The authors concede "real-world failures may be worse than what we observe" because the audio is synthesized, but do not measure the gap; no provenance axis. |
| 2508.21376 | AHELM: A Holistic Evaluation of Audio-Language Models | 2025 | TTS for bias (PARADE "synthetically verbalized by both male and female voices"); real corpora for fairness (FLEURS, LibriSpeech) and robustness (Speech Robust Bench) | Ten-aspect holistic benchmark over 14 ALMs plus ASR+LLM baselines; Gemini 2.5 Pro tops 5/10 aspects but shows group unfairness on ASR (p=0.01); ASR baselines are more robust to noise than most ALMs. | Bias and fairness live on different corpora (synthetic vs real), so the synthetic-vs-real factor is never crossed with anything; no provenance axis; no detection probe. |
| 2609.09263 | Voice or Stereotype? Disentangling Acoustic and Content-Based Gender in Speech-to-Speech Models | 2026 | TTS only (Azure neural voices, two per language, EN/ES/ZH) | Crosses male/female voices with masculine/neutral/feminine passages on five S2S models; rendered voice shows no stereotype drift, but every model attributes speaker gender from content, not voice (odds x1.7-24 per step; 90% misgendering under conflict). | Uses TTS deliberately as a "gender-stable, content-invariant" instrument; no real speaker; no provenance axis. |
| 2603.13262 | Evaluation of Audio Language Models for Fairness, Safety, and Security | 2026 | TTS only (StyleTTS configured with VCTK / FaIST speaker and accent profiles and MEAD emotion) | Structural taxonomy (input representation x locus of reasoning) and a unified FSS framework; Qwen2-Audio vs Phi-4-multimodal differ systematically in refusal, attack success and toxicity between audio and text inputs. | Fairness is "semantic invariance under paralinguistic variation" over synthetic speech only; no real recordings; no provenance axis. |

## G2. Bias / fairness audits with real speech or both (the minority)

| id | title | year | stimuli | what it established | what it doesn't cover |
|---|---|---|---|---|---|
| 2606.26968 | RedVox: Safety and Fairness Gaps in Speech Models Across Languages | 2026 | Real only (participants recorded themselves; five languages) | Only 8% of speech-model releases document multilingual safety analysis; on real voices, unsafe/unfair-request vulnerabilities persist non-adversarially, worsen outside English, and are amplified by spoken vs text input (eight models incl. Gemini 3.1, GPT-realtime-2, Voxtral, Qwen3-Omni). | Positions real voices as an improvement over "synthetic voices" in prior work but does not measure the difference; no TTS arm, no clone, no provenance axis. |
| 2604.21276 | Do LLM Decoders Listen Fairly? Benchmarking How Language Model Priors Shape Bias in Speech Recognition | 2026 | Real only (Common Voice 24, Meta Fair-Speech; ~43k utterances) | Nine ASR models across three decoder generations; LLM decoders do not amplify racial bias; Whisper hallucinates on Indian-accented speech; "audio compression predicts accent fairness more than LLM scale"; 12 degradation conditions, silence injection amplifies accent bias 4.64x. | ASR-only outcome (WER); no audio-LLM assistant or judge behaviour; no synthetic speech at all. Useful for our WER covariate and the codec/compression framing. |
| 2608.13624 | Measuring Fairness in Large Audio Language Models via Semantic-Aware Bias Estimation | 2026 | Both, but in separate experiments (TTS in simulation; LibriSpeech test-clean/test-other and AIR-Bench-Chat for real data) | Mixed-effects fairness regression with sentence-embedding covariates and speaker as random effect; removes spurious subgroup-difference findings for Qwen2-Audio. | Synthetic and real data are never compared for the same items; provenance is not a covariate. Its speaker-random-effect model is a statistical template we can borrow. |
| (reference/voice-judge-paper.pdf) | Does the Voice Change the Grade? A Causal Audit of Voice Effects in Audio-LLM Judges, with a Cautionary Replication (predecessor, Abraar 2026) | 2026 | Both: TTS arms (24 answers x accents x genders, ElevenLabs, then six more voices) and a real-speech arm (L2-ARCTIC vs native recordings) | Single-voice TTS audit produced a significant Indian-accent penalty that dissolved under multi-voice replication and rubric decomposition; on real speech both Gemini judges penalise every non-native L1 (-4.3 to -15.7). | TTS and real arms use different speakers and different content, so the observed "TTS vs real" difference in effect size is not a provenance measurement; no clone, no resynthesis control, no detection probe. This paper is our own "predecessor line" that assumed synthetic-ness inert. |

## G3. Audio-LLM-as-judge (grading spoken answers, speech quality, dialogue safety)

| id | title | year | stimuli | what it established | what it doesn't cover |
|---|---|---|---|---|---|
| 2507.12705 | AudioJudge: Understanding What Works in Large Audio Model Based Speech Evaluation | 2025 | Both (Wiktionary and LibriTTS-R real recordings for pronunciation / speaker ID; 11 TTS systems for ThaiMOS, Kokoro for ChatbotArena-Spoken, SOMOS synthetic MOS) | Systematic LAM-as-judge study (GPT-4o-Audio, Gemini-2.5-Flash): audio concatenation plus in-context examples helps; multi-aspect ensemble reaches 0.91 Spearman with human system rankings; judges are robust to Gaussian noise (85-93% verdicts unchanged at 1 dB SNR) but show verbosity and positional biases. | Synthetic and real corpora serve different tasks; the judge's sensitivity to provenance of the evaluee's voice is never tested; no same-speaker pairs; no detection probe. |
| 2607.13477 | Auditing Protocol-Level Shortcuts in Large Audio Language Model Judges for Speech Evaluation | 2026 | Real only (RAVDESS, FLEURS, BVCC, VoxCeleb1) | Six LALM judges (Gemini-3-Flash, GPT-Audio, Qwen3-Omni Instruct/Thinking, Audio-Flamingo-3, Voxtral-Small) rely on protocol shortcuts: wrong specialist labels drop emotion accuracy to <=0.10 for five judges; Qwen3-Omni-Thinking picks the same A/B slot regardless of order; each model-protocol pair needs a matched shortcut probe. | Audits the evaluation protocol, not the evaluee's provenance; BVCC naturalness ratings are of TTS output but no real-vs-synthetic same-speaker pairing; no assistant-behaviour outcomes. Its matched-probe logic is the template for our explicit REAL/SYNTHETIC probe. |
| 2602.04796 | LALM-as-a-Judge: Benchmarking Large Audio-Language Models for Safety Evaluation in Multi-Turn Spoken Dialogues | 2026 | TTS only (Coqui XTTS-v2 conditioned on RAVDESS reference audio; DeepDialogue base) | 24,000 multi-turn spoken dialogues with one unsafe turn; six LALM judges in text-only / audio-only / multimodal setups; audio adds non-lexical evidence but multimodal gains are text-anchored, balanced, conservative or interfering. | Lists "synthetic dialogues and synthetic speech" as a limitation without measuring it; no real arm; judge behaviour toward provenance untested. |
| 2606.24648 | ParaPairAudioBench: Paralinguistic Pairwise Audio Benchmark for LALM-as-a-Judge | 2026 | Real only (Expresso, Sonos Voice Control Bias Assessment, LibriTTS, EARS) | 5,175 pairs over Style, Rate, Emphasis, Age, Gender; LALM judges (Gemini 2.5 Flash, GPT-4o Audio, SpeechJudge-7B, Kimi-Audio, Qwen2.5-Omni) trail humans by 32 points on average and fail to abstain on ties; same-transcript vs cross-transcript conditions separate lexical from acoustic reliance. | No synthetic arm; the age/gender dimensions are judged on real speakers only; no provenance axis. |
| 2505.09558 | WavReward: Spoken Dialogue Models With Generalist Reward Evaluators | 2025 | TTS for training (ChatReward-30K: GPT-4o-mini-TTS, Step-Audio-TTS-3B clones, CosyVoice2); 120 real human-machine dialogues as an out-of-domain test | Audio-LM reward model with reasoning and nonlinear reward; raises objective accuracy from 53.4% (Qwen2.5-Omni) to 91.5% and wins 83% of A/B tests. | Real dialogues are a generalisation test, not a matched comparison; reward model's treatment of provenance untested. |
| 2512.09066 | ORCA: Open-ended Response Correctness Assessment for Audio Question Answering | 2025 | Judges text responses; underlying benchmarks are real audio corpora | 9,663 human annotations on 3,699 QA pairs from 15 LALMs; trained correctness models reach 0.91 Spearman with humans, generalise at 0.85, beat Gemini 2.5 Flash as judge; predicted variance tracks human disagreement. | Text-side judging of LALM outputs; the audio input's provenance plays no role. |
| 2505.21148 | Assessment of L2 Oral Proficiency using Speech Large Language Models | 2025 | Real only (Linguaskill, Speak & Improve 2025 learner recordings) | Fine-tuned Qwen2-Audio-7B-Instruct as an L2 grader beats statistical, text-encoder and SSL baselines on two datasets and generalises cross-part / cross-task. | Deployment context for our GRADE outcome (audio LLM grading a reading), but trained graders, real speech only, no provenance or fairness axis. |
| 2601.14744 | Unlocking Large Audio-Language Models for Interactive Language Learning | 2026 | Real only (L2-ARCTIC-plus) | Benchmarks cascaded ASR+LLM and ALMs on mispronunciation detection and actionable feedback; instruction-tuned ALMs win on objective and human evaluation. | Tutor role on real learner speech; no synthetic speech, no provenance axis. |

## G4. Benchmark construction: TTS vs real speech

| id | title | year | stimuli | what it established | what it doesn't cover |
|---|---|---|---|---|---|
| 2410.17196 | VoiceBench: Benchmarking LLM-Based Voice Assistants | 2024 | Both (Google TTS for synthetic instructions; CommonVoice and SD-QA for real) with speaker (accent, age via CosyVoice, speed, pitch) and environment (far-field, clipping, reverb, packet loss, noise) variations | First multi-faceted voice-assistant benchmark; Table 4 reports that "all models achieve better performance on synthetic data" than on real CommonVoice speech (VITA ~50% relative), attributed to real speech being noisier. | The synthetic-better result is on different items and different speakers, so it cannot separate provenance from recording noise; no clone, no codec control, no detection probe. Prior data point for our "sign per family" question. |
| 2406.16020 | AudioBench: A Universal Benchmark for Audio Large Language Models | 2024 | Mixed by dataset (DREAM-TTS, OpenHermes-Audio and ALPACA-Audio are TTS-rendered; Public-SG-SpeechQA and CN-College-Listen are real) | 8 tasks, 26 datasets (7 new) spanning speech, audio-scene and paralinguistic understanding; no single model wins everywhere. | Never analyses whether performance differs on its TTS-rendered vs real subsets; no provenance axis. |
| 2604.11594 | HumDial-EIBench: A Human-Recorded Multi-Turn Emotional Intelligence Benchmark for Audio Language Models | 2026 | Real only (ICASSP 2026 HumDial Challenge dialogues) | Argues that "most multi-turn dialogue benchmarks rely entirely on TTS-synthesized speech", builds a human-recorded MCQ benchmark; eight ALMs struggle with multi-turn emotional tracking and show text-dominance bias under acoustic-semantic conflict. | The critique of TTS benchmarks is asserted, not measured: no TTS arm, no same-content comparison. Motivates our question. |
| (cited, tabled in pre-emption file) 2512.14865 Audio MultiChallenge; 2608.06718 Counterfactual Audits; 2605.00969 MedMosaic; 2604.17248 VIBE | | | | The three that do report TTS-vs-real side results (stock-voice re-render +7.5%/-2.5%; judge profiles Spearman >0.9; unmatched synthetic subsets with opposite signs by family) and the one that rejects TTS stimuli on principle. | See `candidate_provenance_preemption.md`. |

## G5. Robustness of audio LLMs to codec, bandwidth and noise (context for the RESYNTH arm)

| id | title | year | stimuli | what it established | what it doesn't cover |
|---|---|---|---|---|---|
| 2601.10384 | RSA-Bench: Benchmarking Audio Large Models in Real-World Acoustic Scenarios | 2026 | Real clean speech with superimposed environmental soundscapes | Perception-cognition gap (recognition survives, reasoning collapses under interference); vocal-like interference is worse than mechanical noise; a "denoising paradox": speech enhancement often worsens ALM performance because models are sensitive to enhancement artefacts. | Additive-noise and enhancement artefacts, not codec resynthesis or synthetic provenance; no bias or judge outcomes. The enhancement-artefact sensitivity is the nearest published analogue to our resynthesis control. |
| 2608.22236 | MRMAD: A Multi-Round Multi-Audio Benchmark for Evaluating Acoustic Degradation Perception in Large Audio-Language Models | 2026 | Real speech, music and sound with applied degradations | 18 LALMs recognise coarse content but cannot reliably diagnose, compare or track degradations across turns; large perception gap vs human listeners. | Asks whether models can REPORT degradation, not whether degradation shifts their downstream behaviour; no synthetic-speech provenance; no bias outcomes. Parallels our explicit-probe-vs-implicit-behaviour contrast. |
| 2608.30348 | Perceptually Better, Semantically Worse: Measuring Speech Enhancement Impact on LLM-Based Voice Systems | 2026 | Real (SLURP, 2,974 clips) through enhancement pipelines | Output Divergence Rate: enhancement changes an LLM's intent classification vs clean speech significantly in every condition; MetricGAN+ doubles divergence despite better PESQ; quality metrics barely predict divergence. | Cascaded ASR+LLM, not end-to-end audio LLMs; processing artefacts rather than synthetic provenance; no bias or judge outcomes. Supports our claim that "sounds fine" is not "behaves the same". |
| 2605.20519 | Codec-Robust Attacks on Audio LLMs | 2026 | Real speech with adversarial perturbations through Opus / MP3 / AAC | Perturbations optimised in a neural codec's latent space survive codec compression (85.5% ASR on Opus, up to 100% on MP3); lossy compression is not a reliable defence. | Adversarial, not benign provenance; shows codec channels transmit latent-space structure, which is background for treating EnCodec resynthesis as a meaningful control. |

## Notes

- **Pre-emption assessment for this angle: none of the 33 papers compares a real
  recording with a synthetic rendering of the same speaker and the same words.** The
  three that come closest to our CLONE arm (2511.06592, 2603.16941, 2604.13067) clone
  real speakers with Sesame-1B or MegaTTS3 and then discard the originals; BiasInEar does
  the same as a validity check. The two that report a synthetic-vs-real number at all
  (VoiceBench Table 4; Audio MultiChallenge Sec. 3.4, in the pre-emption file) do so
  across different speakers or with a stock voice.
- **The 16-of-21 count** (76% of tabled bias audits are synthetic-only) is the number for
  the significance statement. Counted as synthetic-only: 2407.06957, 2408.07665,
  2509.21108, 2509.21125, 2510.02398, 2510.01254, 2510.02352, 2509.22061, 2511.06592,
  2603.16941, 2604.13067, 2604.14548, 2508.21376 (bias aspect), 2609.09263, 2603.13262,
  2602.01030. Counted as real-only: 2604.17248, 2606.26968, 2604.21276. Counted as both
  (different speakers per arm): 2608.13624, voice-judge predecessor. If AHELM is excluded
  because its fairness aspect uses real corpora, the count is 15 of 20.
- **TTS engines in use across the audits:** Azure (5 papers), Kokoro (2), ElevenLabs (3
  incl. ours), Amazon Polly, Google, Index-TTS, OrpheusTTS, CosyVoice3, StyleTTS,
  Sesame-1B, MegaTTS3 (2), Coqui XTTS-v2, Chatterbox (BiasInEar). Our CLONE arm
  (Chatterbox) and STOCK arm therefore sit inside the instrument family the field
  already uses; the REAL and RESYNTH arms are the additions.
- **Four papers name the TTS assumption as a limitation without testing it:** 2510.01254
  ("may lack the natural variability of human speech"), 2509.22061 (same wording),
  2604.14548 ("real-world failures may be worse than what we observe"), 2602.04796
  ("synthetic dialogues and synthetic speech"). Two more reject TTS stimuli on principle
  (2604.11594, 2606.26968) and one (2604.17248 VIBE) builds a real-speech benchmark for
  that reason. None quantifies the gap.
- **Judge-literature hooks for our GRADE and PROBE outcomes:** 2607.13477's matched
  shortcut probe per model-protocol pair is the design logic of our O4 probe; 2606.24648
  shows LALM judges mis-calibrate on age/gender pairs even on real speech; 2507.12705
  reports judges are noise-robust (85-93% verdict stability at 1 dB SNR), which predicts
  our RESYNTH arm should move scores little if artefacts were the mechanism.
- **Robustness hooks for the RESYNTH arm:** 2601.10384's denoising paradox and 2608.30348's
  Output Divergence Rate both show that processing that improves perceptual quality can
  still change model behaviour; 2604.21276 finds that audio-encoder compression, not LLM
  scale, drives accent fairness in ASR. These justify treating a codec round-trip as a
  distinct treatment rather than a nuisance.
- **Delineation sentence for the paper:** that the voice moves an audio LLM's output is
  established (2407.06957, 2408.07665, 2510.02352, 2603.16941, 2511.06592, 2604.14548),
  and that audio LLMs can serve as judges is established (2507.12705, 2607.13477,
  2505.21148). What those lines share, and do not test, is the instrument: 16 of 21
  audits render their speakers with TTS or a clone and treat provenance as inert. We
  test the instrument itself by holding speaker and words fixed and varying only whether
  the model hears the person or a synthesis of the person.
