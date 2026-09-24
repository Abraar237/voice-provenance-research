# Angle H: Zero-shot voice cloning and its evaluation; human perception of synthetic voices; deployment stakes; LibriSpeech as source

Scope note: this file maps the INSTRUMENT (how clones are made and judged), the HUMAN
baseline (how people react to synthetic voices), the STAKES (who is already speaking to
audio LLMs through a synthetic voice) and the SOURCE CORPUS. None of it is prior work on
our claim; it is what our arms, metrics and motivation rest on. The behavioural
audio-LLM neighbours (Audio MultiChallenge, MedMosaic, BiasInEar, Counterfactual Audits)
and the two stakes papers already in hand ("I Hear, Therefore I Trust" 2605.28064; "The
Machines Are Calling" 2609.11137) live in `candidate_provenance_preemption.md` and are
not repeated here.

Verification: every arXiv abstract below was fetched live on 2026-09-24 from
`arxiv.org/abs/<id>` (curl, `citation_title` / `citation_date` / `og:description` meta
tags; the arXiv export API and Semantic Scholar search were not used because they
rate-limit this host). Non-arXiv items were resolved through the Crossref works API by
DOI (title, venue, year, authors confirmed); abstracts came from Crossref where present,
otherwise from the open-access PDF (Cambre 2020 from the author copy; Yamagishi 2012 from
J-STAGE) or Semantic Scholar's DOI lookup (Dubiel 2020). The LibriSpeech licence line was
read live from `openslr.org/12` ("License: CC BY 4.0"). The Chatterbox README was read
live from the resemble-ai/chatterbox GitHub repository. "What it established" lines are
paraphrased from the fetched text, not from memory.

## H1. Zero-shot voice cloning systems (our CLONE and STOCK arms)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2605.30748 | Chatterbox-Flash: Prior-Calibrated Block Diffusion for Streaming Zero-Shot TTS | 2026 | Resemble AI's only arXiv paper in the Chatterbox line (Seo, Park, Nam; code at github.com/resemble-ai/chatterbox-flash). Fine-tunes a pretrained autoregressive TTS decoder into a block-diffusion decoder for streaming; "high-fidelity synthesis comparable to strong autoregressive and non-autoregressive baselines" on standard zero-shot TTS benchmarks. The original Chatterbox (0.5B, MIT licence, 5-20 s reference, "63.75% of blind evaluators preferred Chatterbox over ElevenLabs" per the vendor page) has no paper; the README states every generated file carries the PerTh neural watermark and does not disclose training data. | Describes the model, not its downstream effect on listeners or on audio LLMs. Training data undisclosed, so overlap with LibriSpeech speakers cannot be ruled out (flag as limitation). The PerTh watermark is a systematic difference between CLONE/STOCK and REAL/RESYNTH that no listener perceives but that we cannot exclude a model from picking up; report it. |
| 2410.06885 | F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching | 2024 | Fully non-autoregressive flow-matching DiT TTS; text padded with filler tokens, no duration model or phoneme alignment; Sway Sampling; RTF 0.15; trained on 100K hours multilingual public data; "highly natural and expressive zero-shot ability". Its evaluation protocol (LibriSpeech-PC test-clean, WER via ASR, SIM via WavLM-SV) is the de-facto zero-shot standard we copy. | Alternative clone engine, not used in our arms; no listener or audio-LLM study. |
| 2406.04904 | XTTS: a Massively Multilingual Zero-Shot Text-to-Speech Model | 2024 | Builds on Tortoise; multilingual zero-shot cloning in 16 languages, SOTA in most; publicly released. | Same: an engine, no behavioural downstream measurement. Useful as a second clone engine if we test engine-generality. |
| 2412.10117 | CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models | 2024 | Supervised discrete speech tokens with FSQ; pre-trained LLM backbone; chunk-aware causal flow matching for streaming; claims "human-parity naturalness" and "virtually lossless synthesis quality in the streaming mode". | Engine only. The "human parity" claim is on MOS/SIM, never on how a downstream model treats the output. |
| 2301.02111 | Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers | 2023 | VALL-E: TTS as conditional language modelling over EnCodec tokens, 60K hours; in-context cloning from a 3-second prompt; "significantly outperforms" prior zero-shot TTS on naturalness and speaker similarity; preserves prompt emotion and acoustic environment. | Origin of the codec-token cloning paradigm; codec artefacts inherited by clones are why our RESYNTH arm exists. No downstream behavioural study. |
| 2406.02430 | Seed-TTS: A Family of High-Quality Versatile Speech Generation Models | 2024 | Autoregressive and DiT variants "virtually indistinguishable from human speech"; speaker similarity and naturalness "matches ground truth human speech in both objective and subjective evaluations"; introduces the reference-prompt / target-utterance zero-shot protocol on LibriSpeech test-clean that later systems adopt. | Establishes that the instrument reaches human parity on perceptual metrics; that is exactly the regime where an audio-LLM provenance delta, if any, would be informative. Nothing measured on model behaviour. |

## H2. Speaker-similarity, naturalness and quality metrics (our stimulus-validity checks)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2110.13900 | WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing | 2021 | Masked speech prediction plus denoising, 94k hours; SOTA on SUPERB including speaker verification. The fine-tuned WavLM-SV model is the source of the speaker-embedding cosine ("SIM") used by every zero-shot TTS paper above. | A representation model; SIM measures identity retention, not provenance. High SIM between REAL and CLONE is our precondition, not our result. |
| 2204.02152 | UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022 | 2022 | Ensemble of SSL-fine-tuned strong learners and feature-based weak learners predicting MOS; top system on several VoiceMOS 2022 metrics for in-domain and OOD tracks. The standard automatic naturalness score for TTS outputs. | Predicts human naturalness ratings, not machine treatment; trained on Blizzard/VCC listening tests, so its absolute scale on 2026-era clones is uncalibrated. Use only for within-study arm comparison. |
| 2110.01763 | DNSMOS P.835: A Non-Intrusive Perceptual Objective Speech Quality Metric to Evaluate Noise Suppressors | 2021 | Non-intrusive predictor of ITU-T P.835 SIG/BAK/OVRL scores; PCC 0.94 (SIG), 0.98 (BAK, OVRL) with human ratings. | Designed for noise-suppressor output, not synthetic speech; use as a quality covariate only, and expect RESYNTH and CLONE to differ on it for different reasons. |
| 2402.13071 | Codec-SUPERB: An In-Depth Analysis of Sound Codec Models | 2024 | Benchmark ecosystem for neural codecs across application tasks (content, paralinguistics, speaker, audio) and signal-level metrics; argues the ideal codec "should preserve content, paralinguistics, speakers, and audio information" and that prior codec papers compared only signal-level numbers. | Measures what a codec loses for downstream classifiers; does not ask whether a generative audio LLM changes behaviour toward codec-resynthesised speech. Supplies the expectation that RESYNTH degrades paralinguistics slightly at fixed content. |

## H3. Neural codecs (our RESYNTH control) and the codec-artefact literature

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2210.13438 | High Fidelity Neural Audio Compression | 2022 | EnCodec: streaming encoder-decoder with quantised latent, single multiscale spectrogram adversary, loss balancer; MUSHRA-superior to baselines at 24 kHz mono and 48 kHz stereo across speech and music. The codec we push REAL audio through. | A codec paper; no study of how a listener or model treats re-encoded speech relative to the original. Our RESYNTH arm supplies that measurement. |
| 2306.06546 | High-Fidelity Audio Compression with Improved RVQGAN | 2023 | DAC: ~90x compression of 44.1 kHz audio at 8 kbps; universal single model across speech, music, environment; outperforms competing codecs; open weights. | Alternative control codec if EnCodec-specific artefacts are suspected; otherwise as above. |
| 2406.07237 | CodecFake: Enhancing Anti-Spoofing Models Against Deepfake Audios from Codec-Based Speech Synthesis Systems | 2024 | First codec-based deepfake dataset: SOTA codecs used to re-create speech; anti-spoofing models trained on ASVspoof-style data "cannot detect synthesized speech from current codec-based speech generation systems" until trained on CodecFake. | Shows that codec resynthesis alone is a distinct, detectable artefact class for dedicated detectors, which motivates our RESYNTH arm; does not test generalist audio LLMs or any behavioural outcome. |

## H4. "Highly intelligible but detectable": human and machine detection of cloned speech

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2107.09667 | Human Perception of Audio Deepfakes | 2021 | Game-framed study, 472 users, 14,912 rounds, humans vs a SOTA detector: both "share similar strengths and weaknesses"; IT professionals no better; native speakers better; older participants more susceptible. | Human explicit detection only; no synthesis of what listeners DO with the speech (trust, grading). Our O4 probe is the machine analogue. |
| 10.1371/journal.pone.0285333 | Warning: Humans cannot reliably detect speech deepfakes | 2023 | n = 529, English and Mandarin: listeners spot deepfakes 73% of the time; no language difference; showing examples "only improves results slightly". | Human, explicit, 2023-era synthesis; nothing on implicit behavioural treatment or on audio LLMs. Supplies the "humans are near-ceiling-poor" comparison for D4. |
| 2502.08857 | ASVspoof 5: Design, Collection and Validation of Resources for Spoofing, Deepfake, and Adversarial Attack Detection Using Crowdsourced Speech | 2025 | Crowdsourced ~2,000-speaker database, 32 attack algorithms mixing legacy and contemporary TTS/VC, adversarial attacks for the first time, surrogate-detector-optimised attacks; speaker-disjoint protocols. | Dedicated detector evaluation; no generalist audio-LLM, no matched behavioural outcomes. Anchors the "detectable by specialists" half of the claim. |
| 2603.15037 | PhonemeDF: A Synthetic Speech Dataset for Audio Deepfake Detection and Naturalness Evaluation | 2026 | Parallel real (LibriSpeech subset) and synthetic speech from 4 TTS and 3 VC systems, phoneme-aligned with MFA; KL divergence between real and synthetic phoneme distributions predicts detector performance; identifies the most discriminative phonemes. | Closest in construction to our stimulus set (parallel real/synthetic from LibriSpeech) but the outcome is detector accuracy and phoneme fidelity, not audio-LLM behaviour. Worth citing as evidence that residual phoneme-level differences exist even in "natural" clones. |

## H5. Human perception of synthetic voices: trust, likability, credibility (HCI)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 10.1145/3313831.3376789 | Choice of Voices: A Large-Scale Evaluation of Text-to-Speech Voice Quality for Long-Form Content (CHI 2020) | 2020 | 18 TTS voices, 3 human voices, text-only control, ~1,090 crowd participants rating listening experience, clarity/quality and comprehension for multi-minute content: "TTS voices are close to rivaling human voices, yet no single voice outperforms the others across all evaluation dimensions". | Human raters, 2020-era stock TTS, not clones of the same speaker; comprehension measured in the listener, not in a model. Our O2/O3 are the machine analogue of its rating and comprehension arms. |
| 10.3389/fnbot.2020.593732 | The Human Takes It All: Humanlike Synthesized Voices Are Perceived as Less Eerie and More Likable | 2020 | 95 adults rated synthesized (IBM Watson), humanoid-robot (Sophia) and human voices; human-likeness of synthesized voices predicts lower eeriness and higher likability; explores which paralinguistic features listeners use to tell humans from artificial agents. | Human listeners, unmatched speakers; no same-speaker clone condition; nothing on downstream treatment by a machine listener. |
| 10.3389/fpsyg.2022.787499 | Robot Voices in Daily Life: Vocal Human-Likeness and Application Context as Determinants of User Acceptance | 2022 | 165 participants, five female-sounding voices at graded human realism; anthropomorphism, pleasantness, eeriness and acceptance vary with realism and with application domain (an uncanny-valley-of-voice test). | Same limits: human judges, no clone-vs-real pair, no model behaviour. Supplies the "context-dependent trust" framing for our ASSIST outcome. |
| 10.1145/3405755.3406120 | Persuasive Synthetic Speech: Voice Perception and User Behaviour (CUI 2020) | 2020 | Two-stage study (listening test, lab task with a flight-booking conversational agent): a synthetic voice built from debating-style speech was rated "significantly more truthful and more involved" than one built from audiobook speech, but recommendation-following did not differ. | Compares two synthetic voices, not synthetic vs real; behavioural outcome (compliance) is in the human, not the model. Establishes that perceived truthfulness of a synthetic voice is manipulable by voice source, a warning for our STOCK arm. |

## H6. Accessibility and voice preservation (who speaks to agents through a clone)

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 10.1250/ast.33.1 | Speech synthesis technologies for individuals with vocal disabilities: Voice banking and reconstruction | 2012 | Invited overview of clinical speech synthesis and the Edinburgh "Voice Banking and reconstruction" project for MND/ALS and Parkinson's: personalised synthetic voices for AAC devices built from a patient's recordings before speech is lost. | Pre-neural (HMM) era; no study of how third parties or machines respond to a banked voice. Establishes the population for whom a cloned voice IS the user's voice. |
| 10.1111/1460-6984.12588 | Voice banking for people living with motor neurone disease: Views and expectations | 2020 | >80% of people with MND develop speech difficulties and most eventually use AAC; generic synthesized voices are "often viewed as impersonal and a factor in AAC acceptance"; voice banking is argued to preserve identity; qualitative study of what plwMND consider when deciding to bank. | Human/clinical perspective; nothing on whether voice-agent systems treat a banked voice differently, which is precisely the harm our study would quantify. |
| 2606.21343 | An Evaluation Framework for Text-to-Speech Voice Reconstruction | 2026 | 17 zero-shot TTS systems, 193 speakers with speech disorders: MOS has "limited sensitivity and reliability"; proposes Best-Worst Scaling with situational framing and a dual-reference distributional measure of the intelligibility/identity trade-off; standard measures fail for highly unintelligible speakers. | Evaluates reconstruction quality for people, not machine treatment of reconstructed voices. Confirms zero-shot cloning is the current voice-preservation route and that identity retention is the design goal. |

## H7. Agent-to-agent voice: synthetic callers are already the norm in evaluation and deployment

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 2605.13841 | EVA-Bench: A New End-to-end Framework for Evaluating Voice Agents | 2026 | Orchestrates "dynamic bot-to-bot audio conversations" with a simulated (TTS-voiced) user; 213 enterprise scenarios, accent and noise perturbation suite, 12 systems across cascaded / speech-to-speech / hybrid architectures; accent and noise perturbations expose robustness gaps (mean delta up to 0.314). | Every caller the agents hear is synthetic, and the benchmark never asks whether that matters; provenance is not a perturbation axis. Direct evidence that agent-to-agent synthetic-voice calls are the evaluation standard. |
| 2607.27453 | VAmoS Bench: Voice Agent Simulation Bench | 2026 | End-to-end containment measurement for a credit-card support agent; 100 scenarios, a simulated caller reaches the agent "over audio", roughly one-third adversarial, graded on binary assertions over the trace including SQL tool calls. | Same silent assumption: the simulated caller's voice is synthetic and treated as inert. No real-vs-synthetic comparison. |

## H8. Source corpus

| id | title | year | what it established | what it doesn't cover |
|---|---|---|---|---|
| 10.1109/ICASSP.2015.7178964 | Librispeech: An ASR corpus based on public domain audio books | 2015 | ~1000 h of 16 kHz read English from LibriVox public-domain audiobooks, segmented and aligned; test-clean is the low-WER, speaker-disjoint evaluation split. Licence confirmed live at openslr.org/12: CC BY 4.0 (test-clean.tar.gz, 346 MB). | Built for ASR; speakers are volunteer readers who released recordings to the public domain, so cloning them for matched stimuli is within the licence (our SAFETY FRAMING). Test-clean is also the standard zero-shot TTS evaluation set (Seed-TTS, F5-TTS), so our stimuli sit exactly where the cloning literature reports its numbers. |
| 1904.02882 | LibriTTS: A Corpus Derived from LibriSpeech for Text-to-Speech | 2019 | 585 h at 24 kHz from 2,456 LibriSpeech speakers, re-cut for TTS; neural TTS trained on it reaches >4.0 naturalness MOS on five of six evaluation speakers. | Documents that LibriSpeech speakers are a common TTS TRAINING resource: any open cloning model trained on LibriTTS or LibriLight may have seen our speakers, which would make CLONE partly a "seen speaker" condition. Chatterbox's training data is undisclosed; state this as a limitation and, if budget allows, add a held-out non-LibriVox speaker check. |

## Notes

- **Instrument validity.** Seed-TTS, CosyVoice 2 and F5-TTS all report speaker-similarity
  and naturalness at or near human parity on LibriSpeech test-clean with the same
  reference-prompt / target-utterance protocol we use. That is the point: if clones are
  perceptually at parity for humans (Mai 2023: 73% detection; Müller 2021: humans no better
  than detectors) yet an audio LLM still treats them differently, the delta is informative.
  Report WavLM-SV SIM, UTMOS and DNSMOS per arm as the stimulus-validity table.
- **Three confounds to name in the paper.** (1) PerTh watermark on every Chatterbox output
  (CLONE and STOCK share it, REAL and RESYNTH do not); (2) possible training-set overlap
  between Chatterbox and LibriSpeech/LibriTTS speakers (undisclosed); (3) codec artefacts
  (CodecFake shows resynthesis alone is a detectable artefact class), which is what the
  RESYNTH arm is for.
- **Human-perception literature is all unmatched.** Every HCI study above compares
  different voices (stock TTS vs different human narrators, or two synthetic voices). None
  holds speaker and words fixed. Our design is, to the best of this search, the first
  matched real-vs-clone comparison on ANY listener, human or machine; a small human
  listening arm on the same pairs would be a cheap addition.
- **Stakes chain.** Yamagishi 2012 and Cave & Bloch 2020 give the population whose own
  voice is a clone; EVA-Bench and VAmoS show that voice agents are already evaluated
  against synthetic callers; 2609.11137 (already in hand) shows >=27% of robocalls are
  synthetic; 2605.28064 (already in hand) covers human trust in synthetic speech. None of
  these asks whether the agent on the other end behaves differently.
- **Not included after checking.** MLAAD 2401.09512 (detector training set, 205 TTS
  models, no new claim beyond ASVspoof 5 for us); Voice Cloning survey 2505.00579
  (terminology only); One Voice Fits All? 10.1145/3359325 (voice-design framework, no
  human-vs-synthetic data); telesales agent cloning 2509.04871 (deployment anecdote);
  SoundStream 2107.03312 (verified; EnCodec and DAC cover the codec control).
