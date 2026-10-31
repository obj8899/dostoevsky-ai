# EXPERIMENT REPORT — EXP-WC-01-PROMPT-DIVERSITY
**Dostoevsky AI — Checkpoint 6A.1: Controlled Word Cabinet Improvement Experiment**

- **Experiment ID:** `EXP-WC-01-PROMPT-DIVERSITY`
- **Target Feature:** Word Cabinet (`/api/features/word-cabinet`)
- **Evaluation Date:** 2026-10-29
- **Status:** Completed — Pre-registered Decision: **REJECT / ROLLBACK**

---

## 1. EXPERIMENTAL HYPOTHESIS & PROMPT DIFF

### Hypothesis
Adding explicit anti-echo and multi-faceted emotional representation guidance to the Word Cabinet system prompt will reduce prompt-word regurgitation and synonym clustering, thereby improving primary quality metrics (`WC_CRIT_1` vocabulary relevance and `WC_CRIT_3` distinction usefulness) across canonical evaluation test cases without causing structural regressions or vocabulary obscurity.

### Exact Prompt Diff

**File:** `backend/src/dostoevsky_ai/prompts/word_cabinet.py`  
- **Baseline SHA-256:** `be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686`
- **Experimental SHA-256:** `0c49326daeb0717231906516aa280068e7f7e3b868120f861cc95b57171fb6c0`

```diff
--- a/backend/src/dostoevsky_ai/prompts/word_cabinet.py
+++ b/backend/src/dostoevsky_ai/prompts/word_cabinet.py
@@ -8,6 +8,11 @@ WORD_CABINET_SYSTEM_PROMPT = """\
 distinctions over near-identical synonyms, and include a balanced range of intensity and
 nuance when appropriate.
 
+Prefer vocabulary that adds expressive value beyond simply repeating the user's wording.
+Avoid selecting an input word or a near-equivalent merely because it appears in the context;
+reuse a concept when it is genuinely necessary and the selected word adds a meaningful
+distinction. Across the set, represent different psychological facets or tensions rather
+than producing several interchangeable variants of one emotion.
+
 Explain connotations as possible associations, not universal facts. Give plain-language
 definitions, distinguish each entry from a nearby synonym, and write an original natural
```

---

## 2. BASELINE & EXPERIMENTAL CONFIGURATION

All parameters other than the isolated system prompt text were strictly held constant.

| Parameter | Baseline Condition | Experimental Condition |
| :--- | :--- | :--- |
| **Serving Model Name** | `dostoevsky-baseline:latest` | `dostoevsky-baseline:latest` |
| **Base LLM Architecture** | Qwen2.5 3B (`Q4_K_M`) | Qwen2.5 3B (`Q4_K_M`) |
| **Model Digest** | `c6fb3dc8d97a4e8cab26b0ea088705887efce3f582a01bfb9049f5ef8e1033c9` | `c6fb3dc8d97a4e8cab26b0ea088705887efce3f582a01bfb9049f5ef8e1033c9` |
| **Decoding Options** | `temperature: 0.85`, `top_p: 0.9`, `repeat_penalty: 1.1`, `num_ctx: 4096` | `temperature: 0.85`, `top_p: 0.9`, `repeat_penalty: 1.1`, `num_ctx: 4096` |
| **Token Budget (`num_predict`)** | 1400 | 1400 |
| **Schema Validation** | `WordCabinetGeneration` Pydantic JSON Schema | `WordCabinetGeneration` Pydantic JSON Schema |
| **Evaluation Specification** | `evaluation/endpoint_test_cases.json` (SHA-256: `3aca24e8...`) | `evaluation/endpoint_test_cases.json` (SHA-256: `3aca24e8...`) |
| **Evaluated Cases** | `WC01` through `WC10` (10 canonical items) | `WC01` through `WC10` (10 canonical items) |

---

## 3. PRE-INFERENCE REGRESSION & UNIT TESTS

Before executing model inference, the unit and regression test suite was executed in the project virtual environment (`backend/.venv`):
- **Focused Word Cabinet Tests (`backend/tests/test_word_cabinet.py`):** **16 passed / 16 total** (100% pass rate in 0.89s).
- **Full Backend Regression Suite (`backend/tests/`):** **74 passed / 74 total** (100% pass rate in 5.80s across evaluator, health, inner monologue, literary rewrite, and word cabinet).

---

## 4. METRICS & METHODOLOGY

### Primary Human-Quality Rubric (1–5 scale)
- **`WC_CRIT_1` (Vocabulary Relevance):** Measures whether selected terms precisely articulate the subtle psychological dilemma/tension of the context.
- **`WC_CRIT_3` (Distinction Usefulness):** Measures whether distinctions meaningfully and accurately separate each entry from a nearby synonym rather than relying on self-referential or trivial statements.

### Secondary Diagnostics & Echo-Rate Methodology
- **Echo-Rate Definition:** An entry is flagged as a *verbatim input-word echo* if the suggested word/phrase directly matches any non-stopword token (length $\ge 4$) in the prompt context or shares its immediate lemma/stem root (e.g., `paralysis` $\rightarrow$ `paralyzing dread`, `thrill` $\rightarrow$ `thrilling horror`, `craving` $\rightarrow$ `urgency craving`, `bitterness` $\rightarrow$ `resentment` / `bitter`).
- **Echo Rate Formula:** $\text{Echo Rate} = \frac{\text{Number of Echoed Entries}}{\text{Total Usable Entries Returned}} \times 100\%$.
- **Completion Rate:** $\frac{\text{Usable Entries Returned}}{\text{Requested Entries}} \times 100\%$.

---

## 5. COMPARATIVE RESULTS ACROSS ALL 10 CASES

### Summary Quantitative Metrics

| Metric | Baseline | Experimental | Delta | Decision Threshold | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mean `WC_CRIT_1` (Prelim AI)** | **2.800** | **2.300** | **-0.500** | $\ge +0.25$ | **FAILED (Regressed)** |
| **Mean `WC_CRIT_1` (Combined Human)** | **2.700** | **2.300** | **-0.400** | $\ge +0.25$ | **FAILED (Regressed)** |
| **Mean `WC_CRIT_3` (Prelim AI)** | **3.000** | **2.200** | **-0.800** | $\ge +0.25$ | **FAILED (Regressed)** |
| **Mean `WC_CRIT_3` (Combined Human)** | **2.450** | **2.200** | **-0.250** | $\ge +0.25$ | **FAILED (Regressed)** |
| **Verbatim Echo Rate** | **11.1%** (5/45) | **20.5%** (9/44) | **+84.7% rel** | $\le -50\%$ relative | **FAILED (Increased)** |
| **Completion Rate** | **97.8%** (45/46) | **95.7%** (44/46) | -2.1% | $\ge 90.0\%$ | **PASSED** |
| **Contract / Schema Violations** | 0 / 10 | 0 / 10 | 0 | 0 allowed | **PASSED** |
| **Mean Latency per Case** | 66.26s | 60.82s | -5.44s (-8.2%) | Neutral | Diagnostic only |

---

### Per-Case Itemized Comparison

| Case ID | Blinded Item | Prompt Context Theme | Base Words | Exp Words | Base Scores (C1/C3) | Exp Scores (C1/C3) | Key Observations & Failure Modes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WC01** | `WC_ITEM_10` | Schadenfreude with shame (req 3) | `Titillation`, `Schadenfreude`, `Vindictive Joy` | `gratified`, `contemptuous` | 4 / 4 (P)<br>3.5 / 2.5 (H) | **2 / 1** | **Count shortfall (2/3 returned).** Distinctions collapsed to single isolated words (`resented`, `proud`) with zero explanatory text. |
| **WC02** | `WC_ITEM_07` | Moral violation vs social dread (req 4) | `tormented`, `betrayed`, `guilt-ridden`, `dismayed` | `compunction`, `paralysis`, `agonizing`, `contemplative` | 2 / 3 (P)<br>2.5 / 2.0 (H) | **3 / 3** | `compunction` is strong; `contemplative` and `paralysis` slightly dilute the acute moral panic. Modest improvement over baseline generic descriptors. |
| **WC03** | `WC_ITEM_04` | Outward submission, inward resentment (req 4) | `sullen`, `stoic`, `contemptuous`, `malignant` | `tolerance`, `ingratitude`, `apathy`, `resentment` | 4 / 4 (P)<br>3.0 / 3.0 (H) | **2 / 2** | **Severe semantic contradiction:** `ingratitude` contradicts the prompt (victim of insult, not ungrateful recipient); `apathy` contradicts burning resentment. |
| **WC04** | `WC_ITEM_06` | Prideful refusal of vital aid (req 3) | `intransigent`, `paralyzing dread`, `honor-bound` | `diligently`, `frugally`, `mistrustingly` | 4 / 4 (P)<br>3.0 / 3.0 (H) | **1 / 2** | **Severe category error:** Generated adverbs of ordinary work ethic and budgeting (`diligently`, `frugally`) that completely miss the acute terror of dependency and prideful martyrdom. |
| **WC05** | `WC_ITEM_01` | Moral grievance vs general bitterness (req 3) | `resentment`, `misanthropy`, `bitterness` | `retributive indignation`, `resentment`, `enmity` | 4 / 4 (P)<br>2.5 / 2.0 (H) | **4 / 3** | Good recovery of `retributive indignation`; `resentment` retained. Differentiates personal vs abstract indignation well. |
| **WC06** | `WC_ITEM_05` | Intellectual imposture & pedantic defense (req 5) | `insidious`, `vexatious`, `feigning`, `dogmatism`, `condescension` | `tinge`, `veil`, `vein`, `cloak` | 3 / 2 (P)<br>3.0 / 3.0 (H) | **1 / 2** | **Count shortfall (4/5 returned).** Total semantic collapse: Replaced intellectual defense and pedantic disdain with 4 physical fabric/covering metaphors (`tinge`, `veil`, `vein`, `cloak`). |
| **WC07** | `WC_ITEM_02` | Hollow triumph & post-success disgust (req 6) | `paralyzing`, `acerbic`, `morbidly fascinated`, `sour grapes`, `morose`, `vexed` | `disgust`, `insatiable`, `pangs`, `desolate`, `frustration`, `acerbic` | 1 / 2 (P)<br>2.0 / 2.0 (H) | **3 / 3** | Avoided baseline catastrophe of "sour grapes" (defeat-oriented terms), but `frustration` is too weak and `insatiable` is prospective rather than retrospective. |
| **WC08** | `WC_ITEM_03` | Ostentatious martyrdom & moral vanity (req 6) | `haughty`, `hypocritical`, `morbid`, `misanthropic`, `privileged` | `morbiditself`, `hypocriticalpride`, `self-flagellation`, `morallyhypocriticalpitying`, `sufferingpride`, `self-imposedtribunal` | 2 / 2 (P)<br>2.0 / 2.5 (H) | **1 / 1** | **Catastrophic pseudo-token agglutination:** To evade the anti-echo prohibition while satisfying the schema, the model concatenated prompt words without spaces into 5 non-existent compound tokens. |
| **WC09** | `WC_ITEM_08` | Unwanted compassion for enemy (req 4) | `vicarious empathy`, `condescending pity`, `morbid curiosity`, `misanthropic affection` | `contagious pity`, `empathetic wretch`, `vicarious loathing`, `empathetic collapse` | 2 / 2 (P)<br>2.5 / 2.0 (H) | **3 / 3** | `empathetic collapse` captures the involuntary surge well; `empathetic wretch` labels the person rather than the emotional state. |
| **WC10** | `WC_ITEM_09` | Catastrophe craving & dark thrill (req 8) | `foreboding`, `anxiety`, `paralysis`, `thrill`, `craving`, `anticipation`, `unease`, `desperation` | `dreaded anticipation`, `paralyzing dread`, `thrilling horror`, `dark curiosity`, `urgency craving`, `ominous calm`, `sudden descent`, `nightmarish certainty` | 2 / 3 (P)<br>3.0 / 2.5 (H) | **3 / 3** | Shifted to 2-word phrases. Rather than avoiding echoes, it prepended adjectives to prompt words (`paralyzing dread`, `thrilling horror`, `urgency craving`), resulting in 4 verbatim echoes. |

*(Note: Baseline scores include Prelim AI [P] and Combined Human [H] average across Rater 1 & 2).*

---

## 6. PRE-REGISTERED DECISION RULE EVALUATION

| Criterion | Pre-Registered Rule | Experimental Result | Status |
| :--- | :--- | :--- | :--- |
| **1. Relevance Improvement** | Mean `WC_CRIT_1` improves by $\ge +0.25$ points | Regressed by **-0.500** (prelim) / **-0.400** (human) | **FAILED** |
| **2. Distinction Improvement** | Mean `WC_CRIT_3` improves by $\ge +0.25$ points | Regressed by **-0.800** (prelim) / **-0.250** (human) | **FAILED** |
| **3. Echo Rate Reduction** | Verbatim echo rate decreases by $\ge 50\%$ relative | Echo rate **increased by +84.7% relative** (11.1% $\rightarrow$ 20.5%) | **FAILED** |
| **4. Schema Integrity** | Zero schema violations or unhandled 500 errors | 0 schema violations, 0 HTTP errors (10/10 contract pass) | **PASSED** |
| **5. Completion Rate** | Completion rate does not fall below 90% | 95.7% completion (44/46 entries returned) | **PASSED** |
| **6. No Material Regressions** | No regression toward obscure or irrelevant vocabulary | **Severe regressions:** Agglutinated tokens (`morbiditself`), work-ethic adverbs (`diligently`), and metaphoric drift (`cloak`) | **FAILED** |

---

## 7. ROOT CAUSE ANALYSIS & LIMITATIONS

The experiment demonstrates a classic small-model prompt-steering failure mode in 3B parameter quantized models (`qwen2.5:3b`):
1. **Agglutination Evasion (Token-Smashing):** When negative lexical constraints ("Avoid selecting an input word or a near-equivalent merely because it appears in the context...") are paired with strict JSON schema and semantic guidance, the small model circumvents the constraint by concatenating input tokens without spaces (e.g. `hypocriticalpride`, `morallyhypocriticalpitying`, `self-imposedtribunal` in `WC08`).
2. **Context Escapism / Irrelevant Drift:** Faced with pressure not to use words from the context, the model drifted into adjacent, irrelevant semantic domains—generating everyday work ethic adverbs (`diligently`, `frugally` in `WC04`) or literal physical garments (`tinge`, `veil`, `vein`, `cloak` in `WC06`).
3. **Prefix Padding:** Rather than discovering novel, distinct vocabulary for blended emotions (such as *fatalism*, *schadenfreude*, *aporia*), the model simply attached generic modifiers to the prompt words (`dreaded anticipation`, `thrilling horror`, `urgency craving` in `WC10`), paradoxically increasing the echo rate.
4. **Structural Degradation:** In `WC01`, the extra prompt complexity caused the model to return fewer entries (2 instead of 3) and truncate the `distinction` field into isolated single words (`resented`, `proud`) rather than full comparative sentences.

---

## 8. ARTIFACT PROVENANCE & INTEGRITY AUDIT

### New Artifacts Generated

1. **Experimental Run Container:**
   - **Path:** `evaluation/experiments/exp_wc_01_prompt_diversity/run_20261029T180820Z_c36faad3656341f7a2b7903b8495ea53.json`
   - **SHA-256:** `2d90124ebdb5bc55aea84b3a94fcca13979d4ac8b33dd20d8f26c85567f34bea`
2. **Experiment Report:**
   - **Path:** `evaluation/experiments/exp_wc_01_prompt_diversity/EXP_WC_01_REPORT.md`

### Historical Artifact Integrity Confirmation

All historical artifacts from Checkpoints 1 through 5.1 were preserved byte-for-byte without any alteration or overwriting:
- `evaluation/endpoint_results/blinded_human_evaluation_scores_run_20261025T180347Z.json`  
  **SHA-256:** `81e650d7a65d4f28d7190f99a7c3276aa22ae98862e8c24e18a7d6250f3fbc0b` *(Verified 100% identical)*
- `evaluation/endpoint_results/run_20261025T180347Z_63cb94586e9f4132adf9952aae03efbb.json`  
  **SHA-256:** `076ab4aa7e9b57acd5f964c91b6e706031d25bb6713c2aa958339603990ece51` *(Verified 100% identical)*
- `evaluation/endpoint_test_cases.json`  
  **SHA-256:** `3aca24e846f8c4ad0a5ed867f95d2bd307001059b439a13d49be964d9d642516` *(Verified 100% identical)*

### Git State
- **Branch:** `main`
- **Working Tree:** No files staged, committed, or pushed to remote.

---

## 9. CONCLUSION & RECOMMENDATION

The experimental prompt in `EXP-WC-01-PROMPT-DIVERSITY` failed 4 out of the 6 pre-registered decision criteria. While it improved cases like `WC02` and `WC07`, it introduced severe anomalies including pseudo-token agglutination, distinction field truncation, and irrelevant semantic drift.

**Recommendation:**
In accordance with the pre-registered protocol, **do not merge or retain the experimental prompt**. The Word Cabinet system prompt should be reverted to its clean baseline version (`be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686`).

