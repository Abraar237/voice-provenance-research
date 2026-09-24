# Literature Review — The Synthetic-Voice Penalty
## Do audio LLMs treat a cloned voice differently from the same person's real voice?

Date: 2026-09-24. Method: a pre-emption sweep (`candidate_provenance_preemption.md`, 15 papers,
full-text reads of the three closest) followed by three search angles (F what audio LLMs know
about synthetic speech, G the TTS-stimulus bias-audit and audio-judge literature, H cloning,
codecs, human perception and deployment stakes). 96 unique verified ids (`lit_review.csv`);
every abstract fetched live from arxiv.org/abs or the publisher (the arXiv API and Semantic
Scholar rate-limited this host all day). Angle files: `angle_F_allm_awareness.md`,
`angle_G_tts_audits.md`, `angle_H_cloning_stakes.md`.

---

## Verdict: ALIVE

No paper holds speaker AND words fixed across a real recording and a synthetic rendering of
the same speaker, measures a behavioural outcome (grade, comprehension, assistant reply) on
both, separates provenance from re-encoding with a resynthesis control, and compares the
implicit behavioural delta with the model's explicit "real or synthetic?" report. The
question is being answered by accident as side-ablations inside other papers, and those
side-results disagree in sign, which is the reason to measure it properly.

---

## Novelty delineation (what is known vs what is ours)

We want to be clear about what is already known. That audio LLMs cannot reliably tell
synthetic speech from real when asked is not ours: ALLM4ADD (2505.11079) finds zero-shot
detection near or below chance, TriDF (2512.10652) finds Gemini 2.5 Pro "nearly at chance",
AudioTrust (2505.16211) finds GPT-4o refuses the question, and every detector that works is
fine-tuned. That models can encode an acoustic cue in their hidden states and act on it
without reporting it is not ours either: Senses Wide Shut (2605.13737) and Heard but Not
Heeded (2609.00727) show it for other cues. That synthetic subsets score differently from
real ones is known and contradictory: Gemini scores higher on TTS re-renders (Audio
MultiChallenge 2512.14865, MedMosaic 2605.00969, VoiceBench 2410.17196 Table 4), while
Qwen-omni, Gemma-3n, Audio-Flamingo-3 and GAMA drop more than 12 points (MedMosaic). What is
new here is the matched design that turns those unmatched, different-speaker comparisons into
a per-item causal contrast, the resynthesis control that separates provenance from
artifacts, and the implicit-versus-explicit comparison on the same pairs.

| Closest neighbour (full-text read) | What it established | What it does NOT cover (ours) |
|---|---|---|
| Audio MultiChallenge (2512.14865, Scale AI) | Human-recorded user turns re-rendered with gpt-4o-mini-tts: text-output configs +7.5% on TTS, audio-output configs −2.5% | Stock TTS voice, not the same speaker; transcript route strips disfluencies; accuracy only; no probe, no codec control, no bias framing |
| Counterfactual Audits (2608.06718) | Judge diagnostic profiles on synthesised vs original CAVA audio agree at ρ > 0.9 across 11 judges | Rank-order stability, no per-item delta, no refusal or detection outcome |
| MedMosaic (2605.00969), App. A.8 | Real clinical audio vs ElevenLabs subsets: Gemini +1.4 to +3.3, open-weight models −12 or worse | Unmatched subsets (different content and speakers); no control; a side-table |
| VoiceBench (2410.17196), Table 4 | "All models achieve better performance on synthetic data" | Different items and speakers per arm |
| BiasInEar (2602.01030) | Chatterbox clones of 3 real speakers used to validate stock-TTS bias patterns | Real recordings never evaluated; clones as a check, not a treatment |
| ALLM4ADD (2505.11079), TriDF (2512.10652), AudioTrust (2505.16211) | Zero-shot explicit detection near chance; GPT-4o refuses | Detection only; no behavioural outcome on the same clips |
| Senses Wide Shut (2605.13737), Heard but Not Heeded (2609.00727) | Hidden states encode acoustic cues the output never reports | Other cues (mismatch, style); no provenance axis |
| PhonemeDF (2603.15037) | Parallel real/synthetic LibriSpeech stimuli | Outcome is detector accuracy only |

**Ours alone:**
1. Matched speaker-and-content provenance treatment (REAL vs zero-shot CLONE of the same
   utterance) with per-item paired statistics across 40 speakers.
2. A neural-codec RESYNTH control and a STOCK-voice arm that split "synthetic provenance"
   from "re-encoding artifacts" and "cloned identity" from "synthetic in general".
3. Behavioural outcomes (grade, comprehension, assistant reply behaviour) plus transcription
   as the intelligibility covariate, on every clip.
4. The implicit-vs-explicit comparison: the model's own grade as a discriminator of
   provenance against its stated REAL/SYNTHETIC answer on the same pairs.
5. Reconciling the published sign conflict with one design and several families.

---

## Significance

**Who is affected.** Every deployed voice agent hears synthetic callers: AAC and
accessibility users who speak through TTS, voice-banking users (MND/ALS), agent-to-agent
voice calls, and robocalls (at least 27% synthetic in a 2026 honeypot, 2609.11137). And the
audit literature itself: **16 of 21 audio-LLM bias and fairness audits use synthetic-only
stimuli** (angle G), three name the TTS assumption as an untested limitation, and none runs
the originals against clones of the same speakers.

**What changes.** If a model grades or serves a cloned voice differently from the same
person's real voice, (1) accessibility users are receiving a measurably different service,
which product teams can now test with this design; (2) every TTS-stimulus bias number carries
an unmodelled provenance offset whose sign depends on the family; and (3) if the effect
survives the resynthesis control while explicit detection stays at chance, models are
discriminating on a property they cannot report, which is the case that needs monitoring
rather than prompting. If instead the effect is absent or fully explained by re-encoding,
the TTS-as-instrument methodology the field relies on is validated, and that is also worth
publishing.

---

## Confounds this review surfaced (to be stated in the paper)
- Chatterbox normally embeds the PerTh watermark; in this study the watermarker was
  disabled at generation, so CLONE and STOCK clips carry no watermark (angle H).
- Chatterbox's training data is undisclosed and LibriSpeech speakers are standard TTS
  training material (LibriTTS), so seen-speaker contamination cannot be excluded.
- Judges are robust to additive noise (AudioJudge 2507.12705: 85–93% of verdicts stable at
  1 dB SNR), so a large RESYNTH effect would be surprising; a small one is the expected
  baseline against which the CLONE effect is read.

## Angle summaries

| Angle | Verified | Closest | Verdict |
|---|---|---|---|
| P pre-emption sweep | 15 | Audio MultiChallenge, MedMosaic, Counterfactual Audits | Alive; matched design unclaimed |
| F what ALLMs know about synthetic speech | 21 | TriDF, ALLM4ADD, Senses Wide Shut | Explicit detection near chance; implicit-vs-explicit template exists, never for provenance |
| G TTS-stimulus bias audits and audio judges | 33 | MedVoiceBias, The Voice Behind the Words, VoiceBench | 16/21 audits synthetic-only; none matched |
| H cloning, codecs, perception, stakes | 28 | PhonemeDF, Chatterbox-Flash, Cambre CHI 2020 | No matched real-vs-clone effect on any listener |
