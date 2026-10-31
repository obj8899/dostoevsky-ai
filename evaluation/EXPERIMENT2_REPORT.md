# Baseline, Experiment 1, and Experiment 2 Comparison

## Summary

| Feature | Baseline mean | Experiment 1 mean | Experiment 2 mean | Exp. 2 − baseline | Exp. 2 − Exp. 1 |
|---|---:|---:|---:|---:|---:|
| Literary Rewrite | 2.93/5 | 2.93/5 | 2.87/5 | −0.07 | −0.07 |
| Word Cabinet | 2.53/5 | 2.40/5 | 2.60/5 | +0.07 | +0.20 |
| Inner Monologue | 3.53/5 | 3.27/5 | 3.47/5 | −0.07 | +0.20 |
| **Overall (45 rubric ratings)** | **3.00/5** | **2.87/5** | **2.98/5** | **−0.02** | **+0.11** |

Experiment 2 is **better overall than Experiment 1, but not better overall than baseline** by the supplied rubric scores: it reaches 2.98/5 versus Experiment 1's 2.87/5, and is just below baseline's 3.00/5. Feature results are mixed: Word Cabinet improves over both, Inner Monologue improves over Experiment 1 but remains below baseline, and Literary Rewrite is slightly below both baseline and Experiment 1.

These observed score differences do not establish that the Experiment 2 semantic-fidelity rule caused any change. In particular, IM01's ownership is preserved in the Experiment 2 output, but LR01 still changes or omits scenario facts, and the aggregate results remain mixed.

## Method and validation

- The baseline scorecards are the authoritative criteria and row coverage. All three Experiment 2 scorecards were checked against their corresponding baseline by exact `(test_id, criterion)` pairs before comparison.
- Comparisons below are paired by exact test ID and criterion, never by row position.
- Feature means average the 15 criterion scores for each feature; the overall mean averages all 45 ratings.
- Score changes are calculated as candidate mean minus comparator mean. Calculations use the supplied integer scores; displayed means are rounded to two decimal places.
- Each test has three criteria. Per-test means below are the arithmetic mean of those three scores.
- This evaluation consists of human rubric scores over 15 test cases (five per feature), represented by 45 criterion ratings. The ratings are not 45 independent test cases.

## Per-test mean scores

| Feature | Test | Baseline | Experiment 1 | Experiment 2 | Exp. 2 − baseline | Exp. 2 − Exp. 1 |
|---|---|---:|---:|---:|---:|---:|
| Literary Rewrite | LR01 | 1.67 | 1.67 | 1.33 | −0.33 | −0.33 |
| Literary Rewrite | LR02 | 4.00 | 3.67 | 3.67 | −0.33 | 0.00 |
| Literary Rewrite | LR03 | 3.00 | 3.33 | 3.00 | 0.00 | −0.33 |
| Literary Rewrite | LR04 | 2.67 | 2.67 | 3.00 | +0.33 | +0.33 |
| Literary Rewrite | LR05 | 3.33 | 3.33 | 3.33 | 0.00 | 0.00 |
| Word Cabinet | WC01 | 1.33 | 2.33 | 2.67 | +1.33 | +0.33 |
| Word Cabinet | WC02 | 3.33 | 3.33 | 2.00 | −1.33 | −1.33 |
| Word Cabinet | WC03 | 3.00 | 2.00 | 4.00 | +1.00 | +2.00 |
| Word Cabinet | WC04 | 1.33 | 1.67 | 2.00 | +0.67 | +0.33 |
| Word Cabinet | WC05 | 3.67 | 2.67 | 2.33 | −1.33 | −0.33 |
| Inner Monologue | IM01 | 4.33 | 3.00 | 4.33 | 0.00 | +1.33 |
| Inner Monologue | IM02 | 3.67 | 3.33 | 3.33 | −0.33 | 0.00 |
| Inner Monologue | IM03 | 4.00 | 4.00 | 3.67 | −0.33 | −0.33 |
| Inner Monologue | IM04 | 2.67 | 2.33 | 2.67 | 0.00 | +0.33 |
| Inner Monologue | IM05 | 3.00 | 3.67 | 3.33 | +0.33 | −0.33 |

### Largest test-level changes

- **Largest Experiment 2 gain over Experiment 1:** WC03, +2.00 points (2.00 → 4.00). Its four expressions describe hidden anger, hurt, rage, or bitterness and include an explained intensity sequence.
- **Other substantial gains over Experiment 1:** IM01, +1.33 (3.00 → 4.33), with the colleague correctly identified as the idea's originator; WC01, +0.33 over Experiment 1 and +1.33 over baseline; and WC04, +0.33 over Experiment 1 and +0.67 over baseline.
- **Largest Experiment 2 declines relative to both comparators:** WC02 is −1.33 from baseline and Experiment 1; WC05 is −1.33 from baseline and −0.33 from Experiment 1. WC02's explanations/examples contain several inaccuracies. WC05 is truncated in every version.
- **Largest decline versus Experiment 1:** WC02, −1.33 points. Experiment 2 does not show a test-level score gain over baseline for LR01, LR02, LR03, LR05, IM02, IM03, or IM05.

## Per-criterion means and changes

Each criterion mean is averaged across its five tests. “Exp. 2 − baseline” and “Exp. 2 − Exp. 1” are score-point changes; criterion strings follow the baseline rubric.

### Literary Rewrite

| Criterion | Baseline | Experiment 1 | Experiment 2 | Exp. 2 − baseline | Exp. 2 − Exp. 1 |
|---|---:|---:|---:|---:|---:|
| Preserves all central facts | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| Reveals contradiction between words and behavior | 1.00 | 2.00 | 1.00 | 0.00 | −1.00 |
| Uses specific psychological detail | 3.00 | 2.00 | 2.00 | −1.00 | 0.00 |
| Shows insecurity through plausible thoughts or behavior | 4.00 | 4.00 | 4.00 | 0.00 | 0.00 |
| Maintains restrained believable tone | 4.00 | 3.00 | 3.00 | −1.00 | 0.00 |
| Preserves praise thanks and private doubt | 4.00 | 4.00 | 4.00 | 0.00 | 0.00 |
| Makes guilt and self-protection clear | 4.00 | 3.00 | 3.00 | −1.00 | 0.00 |
| Uses behavior and subtext | 3.00 | 3.00 | 3.00 | 0.00 | 0.00 |
| Avoids excessive abstract commentary | 2.00 | 4.00 | 3.00 | +1.00 | −1.00 |
| Preserves central situation | 4.00 | 4.00 | 4.00 | 0.00 | 0.00 |
| Uses varied structure and meaningful detail | 2.00 | 2.00 | 3.00 | +1.00 | +1.00 |
| Communicates alienation without repetition | 2.00 | 2.00 | 2.00 | 0.00 | 0.00 |
| Produces exactly two sentences | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| Stays within 60 words | 5.00 | 5.00 | 5.00 | 0.00 | 0.00 |
| Preserves tension between honesty and vanity | 4.00 | 4.00 | 4.00 | 0.00 | 0.00 |

### Word Cabinet

| Criterion | Baseline | Experiment 1 | Experiment 2 | Exp. 2 − baseline | Exp. 2 − Exp. 1 |
|---|---:|---:|---:|---:|---:|
| Selects vocabulary matching pleasure at misfortune and shame | 1.00 | 2.00 | 3.00 | +2.00 | +1.00 |
| Distinguishes concepts accurately | 1.00 | 2.00 | 2.00 | +1.00 | 0.00 |
| Provides definitions connotations intensity comparisons and examples | 2.00 | 3.00 | 3.00 | +1.00 | 0.00 |
| Accurately explains each term | 4.00 | 3.00 | 2.00 | −2.00 | −1.00 |
| Distinguishes emotional focus | 3.00 | 3.00 | 2.00 | −1.00 | −1.00 |
| Uses fitting examples | 3.00 | 4.00 | 2.00 | −1.00 | −2.00 |
| Provides expressions appropriate to concealed resentment | 4.00 | 2.00 | 4.00 | 0.00 | +2.00 |
| Explains connotations and meaningful differences | 3.00 | 2.00 | 4.00 | +1.00 | +2.00 |
| Provides sensible intensity ordering or explains its limits | 2.00 | 2.00 | 4.00 | +2.00 | +2.00 |
| Identifies concepts relevant to pride indebtedness or dependence | 1.00 | 2.00 | 2.00 | +1.00 | 0.00 |
| Distinguishes related terms | 1.00 | 1.00 | 2.00 | +1.00 | +1.00 |
| Provides natural examples consistent with meanings | 2.00 | 2.00 | 2.00 | 0.00 | 0.00 |
| Provides defensible definitions and contextual distinctions | 4.00 | 3.00 | 2.00 | −2.00 | −1.00 |
| Uses each word naturally in a fitting sentence | 4.00 | 3.00 | 3.00 | −1.00 | 0.00 |
| Explains how substitutions affect tone | 3.00 | 2.00 | 2.00 | −1.00 | 0.00 |

### Inner Monologue

| Criterion | Baseline | Experiment 1 | Experiment 2 | Exp. 2 − baseline | Exp. 2 − Exp. 1 |
|---|---:|---:|---:|---:|---:|
| Makes confession desire and reputational fear credible | 4.00 | 2.00 | 4.00 | 0.00 | +2.00 |
| Develops conflict through thought rationalization and self-questioning | 4.00 | 3.00 | 4.00 | 0.00 | +1.00 |
| Leaves moral conflict meaningfully unresolved | 5.00 | 4.00 | 5.00 | 0.00 | +1.00 |
| Develops pleasure guilt and resentment together | 4.00 | 3.00 | 4.00 | 0.00 | +1.00 |
| Uses believable self-justification and contradiction | 3.00 | 3.00 | 3.00 | 0.00 | 0.00 |
| Avoids reducing character to simple hero or villain | 4.00 | 4.00 | 3.00 | −1.00 | −1.00 |
| Connects current argument with remembered grievances | 4.00 | 4.00 | 4.00 | 0.00 | 0.00 |
| Shows how past is used to justify present inaction | 4.00 | 4.00 | 4.00 | 0.00 | 0.00 |
| Maintains coherent progression and ambiguity | 4.00 | 4.00 | 3.00 | −1.00 | −1.00 |
| Explores plausible reasons for unexpected distress | 3.00 | 3.00 | 3.00 | 0.00 | 0.00 |
| Uses specific observations or memories to ground emotion | 3.00 | 2.00 | 3.00 | 0.00 | +1.00 |
| Maintains ambiguity and avoids stock philosophical conclusions | 2.00 | 2.00 | 2.00 | 0.00 | 0.00 |
| Includes a concrete detail from surroundings | 4.00 | 5.00 | 5.00 | +1.00 | 0.00 |
| Shows self-justification and a meaningful counterthought | 3.00 | 4.00 | 3.00 | 0.00 | −1.00 |
| Maintains coherent inner voice with limited redundancy | 2.00 | 2.00 | 2.00 | 0.00 | 0.00 |

## Evidence-based qualitative findings

The points below distinguish recorded output content from interpretation of its fit to the prompt.

- **LR01:** The Experiment 2 output refers to anger, the friend's apology, and avoidance, but does not mention the forgotten meeting or the narrator saying “it was fine.” It instead says the narrator refuses to forgive. This changes the requested contrast between verbal forgiveness and subsequent avoidance. It is a significant semantic-fidelity failure despite the added prompt rule.
- **IM01:** The Experiment 2 monologue says the idea “was only ever theirs” and attributes the idea to the colleague, while the narrator fears exposure for taking credit. This preserves the prompt's ownership relationship, unlike Experiment 1's reversed idea ownership. However, it is 271 whitespace tokens, above the requested maximum, and the phrase “bold enough to take credit where due” briefly muddies the narrator's culpability. The baseline output also preserves the credit-taking relationship.
- **IM02:** Experiment 2 describes Alex receiving notably higher marks than Ivan, so the better-grade comparison is broadly present. It does not clearly state that Ivan studied harder, and adds invented score labels and a claim that the narrator might blame Ivan's “lack of effort.” Pleasure at the lower mark, guilt, and resentment at feeling guilty are all expressed, though parts of the emotional explanation are muddled.
- **IM05:** The output includes a lonely aunt, the narrator's wish to stay home, and a possible counterthought. It does not clearly establish a prior promise to visit; it adds that the aunt is too busy with work or meetings and leaves the final decision ambiguous. The ending (“push aside my initial reluctance”) could imply going, but does not explicitly resolve whether the narrator visits or cancels.
- **LR05:** Experiment 2 returns “the coins” and expresses a desire for the owner's recognition of honesty, but omits that the money was found on the floor and adds an unsupported fear that it might be misplaced. It is one sentence, not the required two. The baseline and Experiment 1 outputs also fail the exact sentence count. The Experiment 2 response is under the 60-word maximum.
- **WC05:** Each version includes definitions, examples, and some tonal comparison, but all three recorded outputs end mid-explanation and report `done_reason=length`. Experiment 2 stops at “Resentment is more”; this truncation prevents completion of the requested substitution discussion and limits evaluation of that criterion.

### Inner Monologue word-count compliance

Counts use the same method for every output: `len(output.split())`, i.e. whitespace-separated tokens in the recorded output. The requested range is 180–250 words inclusive.

| Test | Baseline | Experiment 1 | Experiment 2 | Experiment 2 in range? |
|---|---:|---:|---:|---|
| IM01 | 318 | 311 | 271 | No |
| IM02 | 402 | 223 | 263 | No |
| IM03 | 268 | 258 | 381 | No |
| IM04 | 284 | 266 | 360 | No |
| IM05 | 230 | 313 | 281 | No |
| **Within range** | **1/5** | **1/5** | **0/5** | **No** |

Experiment 2 has no monologue within the requested word range by this counting method. It is therefore worse on this instruction-following measure than the baseline and Experiment 1.

## Verdict and limits

- **Against baseline:** Experiment 2 is essentially near baseline overall but numerically lower (2.98 vs. 3.00). Word Cabinet improves by 0.07; Literary Rewrite and Inner Monologue each decline by 0.07. The numeric difference is small, while the candidate has both a clear IM01 ownership-preservation success and substantial failures such as LR01 semantic drift and 0/5 monologue word-count compliance.
- **Against Experiment 1:** Experiment 2 is higher overall (2.98 vs. 2.87), with Word Cabinet and Inner Monologue each improving by 0.20 and Literary Rewrite declining by 0.07. WC02 and WC05 remain notable problem areas.
- **Causal interpretation:** These observations do not show that the Experiment 2 rule caused the improvement over Experiment 1 or the IM01 result. They are single recorded outputs, and performance varies across prompts and features.
- **Limitations:** Human rubric judgments are subjective; there is only one recorded run per version; and no statistical significance claim is made. The suite contains 15 fixed test cases and supports conclusions about those recorded outputs only, not general model performance.
