# Dostoevsky AI — Baseline Evaluation Report

## 1. Overview

- Model: `dostoevsky-baseline:latest`
- Base model: Qwen2.5 3B
- Evaluation suite version: 1.0.0
- Test cases: 15 (5 per feature)
- Criterion-level scores: 45
- Scoring scale: 1–5
- Overall mean criterion score: 3.00/5
- Baseline result: Evaluation completed; quality is mixed and improvement is needed.

The overall mean is a descriptive summary of this fixed test suite. It is not a statistical estimate of general model performance.

## 2. Results by Feature

| Feature | Mean score | Strongest case | Weakest case |
|---|---:|---|---|
| Literary Rewrite | 2.93/5 | LR02: 4.00/5 | LR01: 1.67/5 |
| Word Cabinet | 2.53/5 | WC05: 3.67/5 | WC01 and WC04: 1.33/5 |
| Inner Monologue | 3.53/5 | IM01: 4.33/5 | IM04: 2.67/5 |

Inner Monologue received the highest average score. Word Cabinet received the lowest.

## 3. Key Findings

### Literary Rewrite

- LR01 showed major semantic drift: the output introduced an unsupported explanation and omitted important events from the original.
- LR02 was comparatively restrained and preserved the main meaning.
- LR03 introduced an unsupported psychological explanation.
- LR04 relied on decorative imagery and abstract phrasing.
- LR05 failed its exact two-sentence requirement despite remaining below the requested word limit.

Priority: preserve source meaning and validate explicit structural constraints.

### Word Cabinet

- WC01 selected words that did not precisely express pleasure at another person's failure mixed with shame.
- WC02 explained the four emotions reasonably well but contained imprecise distinctions and a weak example for remorse.
- WC03 supplied relevant expressions but treated intensity as a simpler progression than the meanings justified.
- WC04 repeated a term and failed to provide three precise alternatives for fear of indebtedness.
- WC05 offered useful distinctions, but its output ended mid-thought with `done_reason=length`.

Priority: improve contextual word selection, semantic distinctions, and completion checks.

### Inner Monologue

- IM01 credibly presented the desire to confess alongside fear of reputational loss, and left the conflict unresolved.
- IM02 presented mixed emotions but added broad background claims that were not well grounded.
- IM03 connected remembered grievances to hesitation over apologizing.
- IM04 explored possible reasons for distress but relied on generic philosophical reflections.
- IM05 included a concrete setting and opposing thoughts, but repeated phrasing and a contradictory ending weakened coherence.

### Word-count compliance

The required range for each Inner Monologue test was 180–250 words.

| Test | Word count | Result |
|---|---:|---|
| IM01 | 327 | Fail |
| IM02 | 407 | Fail |
| IM03 | 271 | Fail |
| IM04 | 292 | Fail |
| IM05 | 233 | Pass |

Length compliance was 1/5 (20%). All five generations ended with `done_reason=stop`, so the four overlength responses were not reported as generation-limit interruptions.

## 4. Prioritized Improvement Plan

1. Improve instruction following for word counts, sentence counts, and requested output structure.
2. Preserve facts and intended meaning during literary rewrites.
3. Improve contextual vocabulary selection and distinguish related emotional terms accurately.
4. Detect incomplete outputs and prevent contradictory conclusions.
5. Reduce generic metaphors, repetitive phrasing, and unsupported psychological explanations.

## 5. Method and Limitations

- The evaluation used 15 fixed test cases, five per feature.
- Each case was assessed against three criteria scored from 1 to 5.
- The results comprise 45 criterion-level scores, not 45 independent test cases.
- Findings describe this model configuration and this test suite only.
- Scores are rubric-based judgments and may contain evaluator subjectivity.
- Inner Monologue scores should be reviewed and confirmed by the project owner because they were initially drafted with assistant support.
- The baseline outputs should remain unchanged so later evaluations can be compared fairly.
- No claim of fine-tuning or model improvement is made by this report.

## 6. Baseline Status

Baseline generation and scoring are complete. The next phase should address the highest-impact failure patterns and use the same fixed evaluation suite to measure whether changes improve performance.
