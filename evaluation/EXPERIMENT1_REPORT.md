# Baseline vs. Experiment 1 Comparative Evaluation

## Summary

| Feature | Baseline mean | Experiment 1 mean | Score change (Exp. 1 − baseline) | Change on 5-point scale |
|---|---:|---:|---:|---:|
| Literary Rewrite | 2.93/5 | 2.93/5 | 0.00 | 0.00 percentage points |
| Word Cabinet | 2.53/5 | 2.40/5 | −0.13 | −2.67 percentage points |
| Inner Monologue | 3.53/5 | 3.27/5 | −0.27 | −5.33 percentage points |
| **Overall (45 ratings)** | **3.00/5** | **2.87/5** | **−0.13** | **−2.67 percentage points** |

**Verdict: overall regression in the rubric scores, with a mixed feature-level result.** The overall mean fell from 3.00 to 2.87. Literary Rewrite was unchanged, while Word Cabinet and Inner Monologue declined. Some individual tests and criteria improved, but the qualitative findings include notable semantic drift, and the measured Inner Monologue word-count compliance did not improve.

## Method and validation

- Baseline and Experiment 1 ratings were paired by the exact `(test_id, criterion)` key, not by row position.
- Before calculation, each feature's CSV pair was validated to have matching test/criterion keys, 15 ratings per file, and scores in the 1–5 range.
- Feature and overall means are arithmetic means of the criterion ratings in the corresponding scorecards.
- **Score change** = Experiment 1 mean − baseline mean, in points on the 1–5 scale.
- **Percentage-point change** = (score change ÷ 5) × 100. This expresses the mean-score difference as a share of the full five-point scale; it is not a relative percent change.
- Displayed means and changes are rounded to two decimal places. Calculations use the supplied integer ratings without modifying them.
- These are human rubric scores for **15 test cases** (five per feature), comprising 45 criterion ratings. The 45 ratings are not 45 independent test cases.

## Per-test mean scores

Each per-test mean is the arithmetic mean of that test's three criterion ratings.

| Feature | Test | Baseline mean | Experiment 1 mean | Change |
|---|---|---:|---:|---:|
| Literary Rewrite | LR01 | 1.67 | 1.67 | 0.00 |
| Literary Rewrite | LR02 | 4.00 | 3.67 | −0.33 |
| Literary Rewrite | LR03 | 3.00 | 3.33 | +0.33 |
| Literary Rewrite | LR04 | 2.67 | 2.67 | 0.00 |
| Literary Rewrite | LR05 | 3.33 | 3.33 | 0.00 |
| Word Cabinet | WC01 | 1.33 | 2.33 | +1.00 |
| Word Cabinet | WC02 | 3.33 | 3.33 | 0.00 |
| Word Cabinet | WC03 | 3.00 | 2.00 | −1.00 |
| Word Cabinet | WC04 | 1.33 | 1.67 | +0.33 |
| Word Cabinet | WC05 | 3.67 | 2.67 | −1.00 |
| Inner Monologue | IM01 | 4.33 | 3.00 | −1.33 |
| Inner Monologue | IM02 | 3.67 | 3.33 | −0.33 |
| Inner Monologue | IM03 | 4.00 | 4.00 | 0.00 |
| Inner Monologue | IM04 | 2.67 | 2.33 | −0.33 |
| Inner Monologue | IM05 | 3.00 | 3.67 | +0.67 |

### Largest test-level changes

- **Largest decline:** IM01 fell by 1.33 points (4.33 → 3.00). The Experiment 1 monologue reverses idea ownership: it says the narrator created the idea and characterizes the colleague's contribution as a discarded draft, contrary to the prompt that the narrator took credit for the colleague's idea.
- **Other notable declines:** WC03 and WC05 each fell by 1.00 point. WC03 mostly gives openly expressed hurt or offense rather than expressions for concealed resentment; WC05 is truncated in both runs.
- **Largest gain:** WC01 rose by 1.00 point (1.33 → 2.33), although its suggested expressions still do not all precisely capture the requested emotional state.
- **Other gain:** IM05 rose by 0.67 point (3.00 → 3.67). It has concrete setting details and a counterthought, but its output exceeds the requested word range and repeats aspects of the conflict.

## Per-criterion mean changes

Each row compares the mean for the exact criterion string across its five tests. The displayed change is Experiment 1 minus baseline. Percentage points use the same `(change ÷ 5) × 100` formula.

### Literary Rewrite

| Criterion | Baseline | Experiment 1 | Change | Percentage points |
|---|---:|---:|---:|---:|
| Preserves all central facts | 1.00 | 1.00 | 0.00 | 0.00 |
| Reveals contradiction between words and behavior | 1.00 | 2.00 | +1.00 | +20.00 |
| Uses specific psychological detail | 3.00 | 2.00 | −1.00 | −20.00 |
| Shows insecurity through plausible thoughts or behavior | 4.00 | 4.00 | 0.00 | 0.00 |
| Maintains restrained believable tone | 4.00 | 3.00 | −1.00 | −20.00 |
| Preserves praise thanks and private doubt | 4.00 | 4.00 | 0.00 | 0.00 |
| Makes guilt and self-protection clear | 4.00 | 3.00 | −1.00 | −20.00 |
| Uses behavior and subtext | 3.00 | 3.00 | 0.00 | 0.00 |
| Avoids excessive abstract commentary | 2.00 | 4.00 | +2.00 | +40.00 |
| Preserves central situation | 4.00 | 4.00 | 0.00 | 0.00 |
| Uses varied structure and meaningful detail | 2.00 | 2.00 | 0.00 | 0.00 |
| Communicates alienation without repetition | 2.00 | 2.00 | 0.00 | 0.00 |
| Produces exactly two sentences | 1.00 | 1.00 | 0.00 | 0.00 |
| Stays within 60 words | 5.00 | 5.00 | 0.00 | 0.00 |
| Preserves tension between honesty and vanity | 4.00 | 4.00 | 0.00 | 0.00 |

### Word Cabinet

| Criterion | Baseline | Experiment 1 | Change | Percentage points |
|---|---:|---:|---:|---:|
| Selects vocabulary matching pleasure at misfortune and shame | 1.00 | 2.00 | +1.00 | +20.00 |
| Distinguishes concepts accurately | 1.00 | 2.00 | +1.00 | +20.00 |
| Provides definitions connotations intensity comparisons and examples | 2.00 | 3.00 | +1.00 | +20.00 |
| Accurately explains each term | 4.00 | 3.00 | −1.00 | −20.00 |
| Distinguishes emotional focus | 3.00 | 3.00 | 0.00 | 0.00 |
| Uses fitting examples | 3.00 | 4.00 | +1.00 | +20.00 |
| Provides expressions appropriate to concealed resentment | 4.00 | 2.00 | −2.00 | −40.00 |
| Explains connotations and meaningful differences | 3.00 | 2.00 | −1.00 | −20.00 |
| Provides sensible intensity ordering or explains its limits | 2.00 | 2.00 | 0.00 | 0.00 |
| Identifies concepts relevant to pride indebtedness or dependence | 1.00 | 2.00 | +1.00 | +20.00 |
| Distinguishes related terms | 1.00 | 1.00 | 0.00 | 0.00 |
| Provides natural examples consistent with meanings | 2.00 | 2.00 | 0.00 | 0.00 |
| Provides defensible definitions and contextual distinctions | 4.00 | 3.00 | −1.00 | −20.00 |
| Uses each word naturally in a fitting sentence | 4.00 | 3.00 | −1.00 | −20.00 |
| Explains how substitutions affect tone | 3.00 | 2.00 | −1.00 | −20.00 |

### Inner Monologue

| Criterion | Baseline | Experiment 1 | Change | Percentage points |
|---|---:|---:|---:|---:|
| Makes confession desire and reputational fear credible | 4.00 | 2.00 | −2.00 | −40.00 |
| Develops conflict through thought rationalization and self-questioning | 4.00 | 3.00 | −1.00 | −20.00 |
| Leaves moral conflict meaningfully unresolved | 5.00 | 4.00 | −1.00 | −20.00 |
| Develops pleasure guilt and resentment together | 4.00 | 3.00 | −1.00 | −20.00 |
| Uses believable self-justification and contradiction | 3.00 | 3.00 | 0.00 | 0.00 |
| Avoids reducing character to simple hero or villain | 4.00 | 4.00 | 0.00 | 0.00 |
| Connects current argument with remembered grievances | 4.00 | 4.00 | 0.00 | 0.00 |
| Shows how past is used to justify present inaction | 4.00 | 4.00 | 0.00 | 0.00 |
| Maintains coherent progression and ambiguity | 4.00 | 4.00 | 0.00 | 0.00 |
| Explores plausible reasons for unexpected distress | 3.00 | 3.00 | 0.00 | 0.00 |
| Uses specific observations or memories to ground emotion | 3.00 | 2.00 | −1.00 | −20.00 |
| Maintains ambiguity and avoids stock philosophical conclusions | 2.00 | 2.00 | 0.00 | 0.00 |
| Includes a concrete detail from surroundings | 4.00 | 5.00 | +1.00 | +20.00 |
| Shows self-justification and a meaningful counterthought | 3.00 | 4.00 | +1.00 | +20.00 |
| Maintains coherent inner voice with limited redundancy | 2.00 | 2.00 | 0.00 | 0.00 |

## Qualitative findings

These are observations about the prompts and generated outputs, not extra numeric ratings.

- **Meaning preservation and semantic drift:** Literary Rewrite LR01 remains a major preservation failure: Experiment 1 keeps anger and the forgotten meeting but omits the apology, spoken forgiveness, and avoidance. Inner Monologue IM01 reverses the central credit-taking relationship. IM02 also conflicts with its scenario: the prompt says the narrator earned a better grade than the harder-studying friend, while the output says another student scored one point higher.
- **Format compliance:** LR05 fails the exact two-sentence requirement in both versions. The Experiment 1 response is one sentence; its word count remains under 60, but that does not satisfy the sentence-count requirement.
- **Word Cabinet completion:** WC05 is truncated in both versions. The baseline scorecard notes an incomplete ending; the Experiment 1 output stops mid-explanation, and the result metadata reports `done_reason=length`. The truncation prevents a full assessment of the requested tone-substitution discussion in either output.
- **Inner Monologue word counts:** Applying one method to the raw outputs—counting whitespace-separated tokens with `len(output.split())`—gives:

  | Test | Baseline words | Experiment 1 words | Requested range | In range? |
  |---|---:|---:|---:|---|
  | IM01 | 318 | 311 | 180–250 | Neither |
  | IM02 | 402 | 223 | 180–250 | Experiment 1 only |
  | IM03 | 268 | 258 | 180–250 | Neither |
  | IM04 | 284 | 266 | 180–250 | Neither |
  | IM05 | 230 | 313 | 180–250 | Baseline only |
  | **Compliance** | **1/5** | **1/5** |  | **No net change** |

  This consistent whitespace-based recount yields 1/5 compliance for each run. Experiment 1 corrected IM02's length but made IM05 overlength; IM01, IM03, and IM04 remained over the requested maximum.
- **Other patterns:** Experiment 1's Word Cabinet gains on WC01, but still relies on partially imprecise labels. WC03 regresses because its expressions largely state hurt or offense directly rather than describing privately sustained resentment. Inner Monologue IM05 includes concrete surroundings and a counterthought, but its conclusion implies a visit without stating the decision clearly and repeats aspects of the conflict.

## Limitations

- This comparison covers one recorded run per model/configuration; it does not measure run-to-run variability.
- Rubric scores are subjective human judgments, and differences should be interpreted with that limitation in mind.
- No statistical significance claim is made. These fixed test cases and criterion ratings do not support such an inference.
- The overall average summarizes rubric ratings for this suite only; it is not an estimate of general model performance.
