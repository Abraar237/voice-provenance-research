# Reference verification (2026-09-24)

Every arXiv id was fetched live from https://arxiv.org/abs/<id> (HTTP 200); titles and full author lists were read from the page's citation_* metadata and the Comments field was used to decide venue. Non-arXiv entries were resolved via doi.org (content-negotiated BibTeX) or the live GitHub repository. Lit-review titles (angle_F/G/H, candidate_provenance_preemption) were compared where present.

| key | verdict | title on abs/DOI page | lit-review title (if any) |
|---|---|---|---|
| a2512_14865 | OK | Audio MultiChallenge: A Multi-Turn Evaluation of Spoken Dialogue Systems on Natural Human Interaction | Audio MultiChallenge |
| a2608_06718 | OK (lit-review label 'Do ALMs use paralinguistic evidence? Counterfactual audits' is a nickname; abs title differs in wording only) | Do Audio Language Models Use Paralinguistic Evidence? Counterfactual Audits for Response Evaluation | Do ALMs use paralinguistic evidence? Counterfactual audits |
| a2605_00969 | OK | MedMosaic: A Challenging Large Scale Benchmark of Diverse Medical Audio | MedMosaic |
| a2410_17196 | OK | VoiceBench: Benchmarking LLM-Based Voice Assistants | VoiceBench: Benchmarking LLM-Based Voice Assistants |
| a2602_01030 | OK (lit-review label 'BiasInEar' is a nickname; abs title differs in wording only) | Bias in the Ear of the Listener: Assessing Sensitivity in Audio Language Models Across Linguistic, Demographic, and Positional Variations | BiasInEar |
| a2505_11079 | OK | ALLM4ADD: Unlocking the Capabilities of Audio Large Language Models for Audio Deepfake Detection | ALLM4ADD |
| a2505_16211 | OK | AudioTrust: Benchmarking the Multifaceted Trustworthiness of Audio Large Language Models | AudioTrust |
| a2512_10652 | OK | TriDF: Evaluating Perception, Detection, and Hallucination for Interpretable DeepFake Detection | TriDF: Evaluating Perception, Detection, and Hallucination for Interpretable DeepFake Detection |
| a2605_13737 | OK | Senses Wide Shut: A Representation-Action Gap in Omnimodal LLMs | Senses Wide Shut: A Representation-Action Gap in Omnimodal LLMs |
| a2609_00727 | OK | Heard but Not Heeded: Paralinguistic Information Encoding and Loss in Audio-Language Models | Heard but Not Heeded: Paralinguistic Information Encoding and Loss in Audio-Language Models |
| a2603_15037 | OK | PhonemeDF: A Synthetic Speech Dataset for Audio Deepfake Detection and Naturalness Evaluation | PhonemeDF: A Synthetic Speech Dataset for Audio Deepfake Detection and Naturalness Evaluation |
| a2609_11137 | OK | The Machines Are Calling: Measuring Automated and Synthetic Voices in Unwanted Inbound Calls | The Machines Are Calling |
| a2510_02352 | OK | Evaluating Bias in Spoken Dialogue LLMs for Real-World Decisions and Recommendations | Evaluating Bias in Spoken Dialogue LLMs for Real-World Decisions and Recommendations |
| a2604_17248 | OK | VIBE: Voice-Induced open-ended Bias Evaluation for Large Audio-Language Models via Real-World Speech | VIBE |
| a2603_16941 | OK | The Voice Behind the Words: Quantifying Intersectional Bias in SpeechLLMs | The Voice Behind the Words: Quantifying Intersectional Bias in SpeechLLMs |
| a2507_12705 | OK | AudioJudge: Understanding What Works in Large Audio Model Based Speech Evaluation | AudioJudge: Understanding What Works in Large Audio Model Based Speech Evaluation |
| a2607_13477 | OK | Auditing Protocol-Level Shortcuts in Large Audio Language Model Judges for Speech Evaluation | Auditing Protocol-Level Shortcuts in Large Audio Language Model Judges for Speech Evaluation |
| a2604_11594 | OK | HumDial-EIBench: A Human-Recorded Multi-Turn Emotional Intelligence Benchmark for Audio Language Models | HumDial-EIBench: A Human-Recorded Multi-Turn Emotional Intelligence Benchmark for Audio Language Models |
| a2606_26968 | OK | RedVox: Safety and Fairness Gaps in Speech Models Across Languages | RedVox: Safety and Fairness Gaps in Speech Models Across Languages |
| a2604_21276 | OK | Do LLM Decoders Listen Fairly? Benchmarking How Language Model Priors Shape Bias in Speech Recognition | Do LLM Decoders Listen Fairly? Benchmarking How Language Model Priors Shape Bias in Speech Recognition |
| a2601_10384 | OK | RSA-Bench: Benchmarking Audio Large Models in Real-World Acoustic Scenarios | RSA-Bench: Benchmarking Audio Large Models in Real-World Acoustic Scenarios |
| a2511_06592 | OK | MedVoiceBias: A Controlled Study of Audio LLM Behavior in Clinical Decision-Making | MedVoiceBias: A Controlled Study of Audio LLM Behavior in Clinical Decision-Making |
| a2605_30748 | OK | Chatterbox-Flash: Prior-Calibrated Block Diffusion for Streaming Zero-Shot TTS | Chatterbox-Flash: Prior-Calibrated Block Diffusion for Streaming Zero-Shot TTS |
| a2501_08238 | OK | CodecFake+: Codec-Based Resynthesized Data as a Proxy for Detecting CodecFake Speech | CodecFake+: Codec-Based Resynthesized Data as a Proxy for Detecting CodecFake Speech |
| a2605_28064 | OK | I Hear, Therefore I Trust: A Socio-Technical Investigation of Humans as Synthetic Speech Detectors | I Hear, Therefore I Trust |
| a2605_26136 | OK | Eroding Trust in Real Speech: A Large-Scale Study of Human Audio Deepfake Perception | Eroding Trust in Real Speech: A Large-Scale Study of Human Audio Deepfake Perception |
| a2604_25591 | OK | Walking Through Uncertainty: An Empirical Study of Uncertainty Estimation for Audio-Aware Large Language Models | Walking Through Uncertainty: An Empirical Study of Uncertainty Estimation for Audio-Aware Large Language Models |
| a2604_19300 | OK | HalluAudio: A Comprehensive Benchmark for Hallucination Detection in Large Audio-Language Models | HalluAudio: A Comprehensive Benchmark for Hallucination Detection in Large Audio-Language Models |
| a2606_24648 | OK | ParaPairAudioBench: Paralinguistic Pairwise Audio Benchmark for LALM-as-a-Judge | ParaPairAudioBench: Paralinguistic Pairwise Audio Benchmark for LALM-as-a-Judge |
| a2601_00777 | OK | Investigating the Viability of Employing Multi-modal Large Language Models in the Context of Audio Deepfake Detection | Investigating the Viability of Employing Multi-modal Large Language Models in the Context of Audio Deepfake Detection |
| a2601_23066 | OK | Towards Explicit Acoustic Evidence Perception in Audio LLMs for Speech Deepfake Detection | Towards Explicit Acoustic Evidence Perception in Audio LLMs for Speech Deepfake Detection |
| a2210_13438 | OK | High Fidelity Neural Audio Compression | High Fidelity Neural Audio Compression |
| a2410_06885 | OK | F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching | F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching |
| a2412_10117 | OK | CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models | CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models |
| a2507_13264 | OK | Voxtral | - |
| a2608_30348 | OK | Perceptually Better, Semantically Worse: Measuring Speech Enhancement Impact on LLM-Based Voice Systems | Perceptually Better, Semantically Worse: Measuring Speech Enhancement Impact on LLM-Based Voice Systems |
| a2603_10725 | OK (lit-review label 'HIR-SDD' is a nickname; abs title differs in wording only) | Towards Robust Speech Deepfake Detection via Human-Inspired Reasoning | HIR-SDD |
| a2509_22061 | OK | Speak Your Mind: The Speech Continuation Task as a Probe of Voice-Based Model Bias | Speak Your Mind: The Speech Continuation Task as a Probe of Voice-Based Model Bias |
| a2604_14548 | OK | VoxSafeBench: Not Just What Is Said, but Who, How, and Where | VoxSafeBench: Not Just What Is Said, but Who, How, and Where |
| a2602_04796 | OK | LALM-as-a-Judge: Benchmarking Large Audio-Language Models for Safety Evaluation in Multi-Turn Spoken Dialogues | LALM-as-a-Judge: Benchmarking Large Audio-Language Models for Safety Evaluation in Multi-Turn Spoken Dialogues |
| librispeech | OK | Librispeech: An ASR corpus based on public domain audio books (ICASSP 2015, pp. 5206-5210, DOI 10.1109/ICASSP.2015.7178964 resolves) | - |
| cambre2020 | OK | Choice of Voices: A Large-Scale Evaluation of Text-to-Speech Voice Quality for Long-Form Content (CHI 2020, DOI 10.1145/3313831.3376789 resolves; authors Cambre, Colnago, Maddock, Tsai, Kaye) | - |
| bh1995 | OK | Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing (J. R. Statist. Soc. B 57(1):289-300, DOI 10.1111/j.2517-6161.1995.tb02031.x resolves) | - |
| chatterbox | OK | github.com/resemble-ai/chatterbox returns 200; GitHub API: 'SoTA open-source TTS', MIT, created 2025-04-23 | - |
| mueller2021 | OK | Human Perception of Audio Deepfakes (arXiv 2107.09667; Mueller, Pizzi, Williams; published at ACM MM 2022 DDAM workshop, DOI 10.1145/3552466.3556531) | - |

OK: 45  PROBLEM: 0

Notes:
- 2603.10725 is labelled 'HIR-SDD' in the lit review; the abs title is 'Towards Robust Speech Deepfake Detection via Human-Inspired Reasoning' (same paper, nickname expands to it).
- 2507.13264 (Voxtral) is not in the lit-review tables but resolves; 106 authors, truncated to 8 + 'and others'.
- Venue entries (@inproceedings / journal) were used only where the abs Comments field states acceptance: ICML 2026 (2605.00969, 2602.04796), EACL 2026 Findings (2602.01030), ACM MM 2025 (2505.11079), ICLR 2026 (2505.16211), CVPR 2026 (2512.10652), LREC 2026 (2603.15037), Interspeech 2026 (2603.16941, 2606.24648), TASLP 2026 (2501.08238), Odyssey 2026 (2605.28064), ACL 2026 (2604.19300), IJCB 2025 (2601.00777), EMNLP 2026 (2608.30348), Identity-Aware AI Workshop at LREC 2026 (2509.22061). 2604.17248 says only 'Submitted to SLT 2026' so it stays an arXiv preprint.
- Author lists with more than 8 names are truncated to 8 + 'and others' (2512.14865, 2505.11079, 2505.16211, 2512.10652, 2609.11137, 2601.10384, 2501.08238, 2606.24648, 2412.10117, 2507.13264, 2604.14548).
- Accented author names are LaTeX-escaped so the file compiles under pdflatex without inputenc.
