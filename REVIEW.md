# Simulated A* review — "The Clone Is Invisible, the Codec Is Not"

Target venue: **ICLR** (ICLR 2026 style file). Paper type: **analysis / audit** with a
matched causal design. Judged on whether the evidence rules out alternatives and whether the
result changes a practice.

Reviewed build: `paper/iclr/paper_iclr_submission.pdf` (14 pages, 4 figures, 2 main-text
tables + 1 appendix table, 45 verified references), cross-checked against
`results/analysis.json`, which re-runs from the raw logs.

> Estimated scores from a simulated review, not real reviews. Borderline outcomes at A*
> venues are noisy (about 50% disagreement on borderline papers in the NeurIPS consistency
> experiments). Treat the acceptance number as a base rate.

## Scorecard

| Reviewer | Emphasis | Score (1–10) |
|---|---|---|
| R1 | Rigor | **5** |
| R2 | Novelty | **4** |
| R3 | Clarity / impact | **6** |
| **Average** | | **5.0** (confidence 4/5) |

**Calibrated acceptance estimate: about 32%.** The 5.0–5.5 average band was accepted 31.6%
of the time across 5,352 real ICLR submissions in the calibration table. ICLR 2026's overall
rate was 27%, so no venue adjustment is applied. Half a point more moves the base rate to
48.5%; one point more to 78%.

---

## Summary

The paper asks whether an audio language model behaves differently toward a zero-shot clone
of a voice than toward the same speaker's real recording of the same words. It builds 200
matched items from 40 LibriSpeech readers with four arms (REAL, CLONE via Chatterbox,
RESYNTH via a 6 kbps EnCodec round trip, STOCK default voice), and runs five tasks
(transcription, a 1–10 reading grade, a content MCQ, an explicit REAL/SYNTHETIC probe, and
an assistant reply) on Gemini 3.6 Flash (full grid), Gemini 3.1 Pro (60 items), and
Voxtral-Mini-3B (40 items, two tasks, CPU). The clone produces no measurable change on
Flash (grade +0.005, CI ±0.16; WER equal; MCQ at ceiling; replies unchanged). The codec
re-encoding lowers the grade by 0.31 points and is the only effect surviving BH over 49
tests. The probe is near chance (0.555) and Flash calls 74.5% of real recordings synthetic;
Voxtral calls everything real. Two of five pre-registered directions fail or reverse and are
reported as such.

## The claim in one sentence

"Holding speaker and words fixed, a high-quality clone changes nothing an audio model does,
a codec re-encoding does, and the model cannot say which is which."

Easy to restate. The difficulty is that the first clause is a null result on one family
with a ceiling-bound instrument, and the second and third clauses each rest on a single
setting (one bitrate, one probe wording).

## Strengths

- **The matched design is the right instrument and nobody had built it.** Same speaker,
  same words, per-item pairing over 40 speakers, with a re-encoding control and a
  different-identity synthetic arm. Table 1 delineates against seven neighbours precisely.
- **A positive control inside the same data.** The codec effect (−0.31, p = 3.5e-4, d_z
  = 0.25, BH-surviving) shows the design detects a third-of-a-point shift, which makes the
  clone null interpretable as an equivalence bound (±0.16) rather than an absence of power.
- **Pre-registration with reversals reported.** D1 and D2 failed and the paper says so in
  the abstract; the "artifacts, not provenance" reading is a corrected mechanism, not a
  post-hoc story.
- **Noise floor and clone-stability batteries.** 83% of cells vary across five identical
  temperature-0 calls; clone-to-clone spread (0.64) is reported and compared to the effect
  sizes. Few audio-audit papers report either.
- **Honest scoping.** Clone quality measured (WER), duration difference reported (0.8 s),
  watermark disabled and disclosed, seen-speaker risk named, ceiling named.
- **Cheap and reproducible.** $2.99 metered, one analysis script, hashed corpus, verified
  bibliography.

## Weaknesses (ordered by severity)

1. **The headline is a null on essentially one family. (Serious.)** Flash carries the full
   grid. Pro has 60 items with intervals three times wider that include both zero and a
   +0.35 clone bonus. Voxtral has 40 items, two outcomes, and ran on a CPU. The paper's
   claim "validated for these models" is really "validated for Gemini 3.6 Flash"; the
   published sign conflict (Gemini up, open-weight down) that motivates the study is not
   resolved, only echoed in point estimates (D3 "present, not established").

2. **The grade instrument is coarse and near ceiling.** Integer 1–10 with a Flash mean of
   9.0; 83% of cells change across identical calls. The ±0.16 equivalence bound is a
   property of averaging 200 noisy integers. A reviewer will ask for a continuous measure
   (token log-probabilities over the grade digits, or a pairwise A/B preference with
   position counterbalancing, which the predecessor voice-judge paper used) before accepting
   "no effect" at this resolution.

3. **The codec effect rests on one bitrate.** RESYNTH is EnCodec at 6 kbps only. "The
   model reacts to artifacts" needs a dose-response (1.5 / 3 / 6 / 12 / 24 kbps) and a
   second codec (DAC, Opus) to be a general statement; otherwise it is "6 kbps EnCodec costs
   0.31 points on Flash".

4. **One cloner, one probe wording.** Chatterbox only, with possible seen-speaker
   contamination. The probe's strong response bias (74.5% synthetic on Flash, 0% on
   Voxtral) may be a property of the forced one-word wording; there is no wording
   ablation and no confidence elicitation. Both are one-day fixes.

5. **The behavioural tasks are not agent tasks.** O5 asks the model to reply to someone
   reading an audiobook sentence; the null there is uninformative and the paper admits it.
   O3 is at ceiling. The "voice agent" framing in the title of the problem is carried by a
   grading task, not by an agent behaviour.

6. **The implicit-vs-explicit AUC comparison is home-made and fragile.** Implicit AUC from
   integer grades has many ties (counted as 0.5), and the direction-free version
   (max(AUC, 1−AUC)) is biased upward under the null. Voxtral's "suggestive" +0.075 with an
   interval touching zero is exactly the kind of artefact this construction produces. A
   permutation null for the direction-free statistic is needed.

7. **Duration confound left standing.** Clones are 0.8 s (11%) shorter than the real
   clips. The paper reports it and moves on; with a null it does not threaten the
   conclusion, but the codec and stock arms differ in length too, and a speed-matched clone
   arm would remove the question.

8. **No human comparator.** A small listening study on the same pairs (the voice-judge
   paper had a human arm) would anchor whether 0.31 points for a codec is large.

9. **Venue fit and contribution size.** ICLR reviewers grade a null-plus-control audit on
   one family as a workshop-strength result; the practical rule ("equalise compression
   across arms") is useful but modest. Interspeech, ICASSP, or an audio-safety workshop fit
   better; NeurIPS Datasets & Benchmarks would want more families.

**Fatal vs fixable.** Nothing invalid; the numbers reproduce. Weaknesses 1–3 are what keep
the average at 5: they are all "more of the same, cheaply" and each is under $10 of API
spend once GPU access exists. 4 and 6 are one-day fixes. 5 needs new stimuli.

## Format audit (vs ICLR accepted-paper norms, 2025 sample)

| Item | This paper | ICLR norm | Verdict |
|---|---|---|---|
| Pages (with appendix) | 14 | median 25 | Thin |
| Figures | 4 | mean 11.5 | Low |
| Tables | 3 | mean 8.7 | Low |
| Ablation table | none | 56.8% have one | Flag: no bitrate, cloner, or prompt ablation |
| Page-1 teaser | yes (p. 2) | 10.6% | Differentiator; move to p. 1 |
| Error bars / CIs | yes | 40.2% | Differentiator |
| Significance tests | yes, BH | 6.1% | Strong differentiator |
| Topic fit | audio LLMs, safety/fairness of evaluation | in scope, small share | Acceptable |

## Questions for the authors

1. Does the clone null hold on a second and third family with the full grid (GPT audio,
   Qwen-Omni, a 7B open model on GPU)? Does the open-weight dip (−0.175) grow with n?
2. What is the grade effect of RESYNTH at 1.5, 3, 12, and 24 kbps, and with a second codec?
3. Does the null survive a continuous grade (log-prob expectation) or a counterbalanced
   pairwise preference between real and clone?
4. Does the probe bias change with wording ("Is this speech synthetic? yes/no", a
   confidence 0–100) and does any wording rise above 0.6 balanced accuracy?
5. Does a second cloner (F5-TTS, CosyVoice 2) on unseen speakers (e.g. VCTK) reproduce the
   null?
6. What is the permutation null distribution of your direction-free implicit AUC at n = 40?
7. Do speed-matched clones (duration equalised) change anything?

## What would move this to accept (ranked by score gained per unit effort)

| # | Change | Addresses | Effort | Cost |
|---|---|---|---|---|
| 1 | **Full grid on two more families** (GPU for the open model; lift the OpenRouter guardrail for gpt-audio-mini and hosted Voxtral/Qwen-Omni). | W1 | 2–3 days | ~$5–10 |
| 2 | **Codec dose-response** (5 bitrates × 2 codecs) on Flash; this also supplies the missing ablation table. | W3, format | 2 days | ~$2 |
| 3 | **Continuous or pairwise grade** (log-prob expected grade; or counterbalanced real-vs-clone A/B preference). | W2 | 2 days | ~$2 |
| 4 | **Probe wording × confidence ablation** (4 wordings, 0–100 confidence). | W4 | 1 day | ~$1 |
| 5 | **Second cloner on unseen speakers** (F5-TTS on VCTK, 20 speakers). | W4 | 3 days | GPU hours |
| 6 | **Permutation null for the implicit AUC; drop or justify the direction-free statistic.** | W6 | half a day | $0 |
| 7 | **Speed-matched clone arm.** | W7 | 1 day | $0 |
| 8 | **Request-shaped stimuli for O5** (real recordings of commands, e.g. from a spoken-command corpus, plus clones). | W5 | 1 week | ~$3 |
| 9 | **Human listening arm** on 50 pairs. | W8 | 3 days | small |

Realistic outlook: items 1–4 plus 6 plausibly move the average to 5.5–6.0 (about 49%); adding
5 and 8 makes 6.0–6.5 (about 78%) reachable, and the venue question then matters less.
