# DOSTOEVSKY AI — CHECKPOINT 6D: HUMAN EVALUATION HANDOFF REPORT
**Study:** `EXP-WC-02-DISTINCTION-STRUCTURE`  
**Scope:** 20-Item Contemporaneous Double-Blind Human Evaluation (10 Baseline + 10 Experimental Outputs)  
**Date:** 2026-10-30  
**Status:** **HANDOFF PACKAGE PREPARED & AUDITED (Awaiting Independent Human Ratings)**  

---

## 1. VERIFICATION OF EXISTING BLINDED EVALUATION PACKAGE

In accordance with Requirement 1, the three primary blinded package files generated in Checkpoint 6C were inspected and their SHA-256 digests verified:

| File Name | Location | SHA-256 Hash | Status |
| :--- | :--- | :--- | :--- |
| `blinded_evaluation_worksheet_20_items.json` | `evaluation/experiments/exp_wc_02_distinction_structure/` | `d0af25b9139a7452ed815382c040fd00491d99a9ab784e63ab82265cbde6f6a4` | Verified |
| `blinded_evaluation_worksheet_20_items.md` | `evaluation/experiments/exp_wc_02_distinction_structure/` | `05dd0890a845205875b16d06819eb6dcb59183f7835cec5911dc7bd86fef2d9a` | Verified |
| `blinded_evaluation_key_20_items.json` | `evaluation/experiments/exp_wc_02_distinction_structure/` | `57c39532d41eedbc7e607948298a3a0dd13992ce526dadeb940ba8a7775b5827` | Verified |

---

## 2. RUBRIC ALIGNMENT & STRUCTURAL AUDIT

All 20 items (`WC_EVAL_01` through `WC_EVAL_20`) were audited against the canonical Word Cabinet rubrics defined in `evaluation/endpoint_test_cases.json`:

1. **Item Completeness:** All 20 items present the exact context prompt, requested count, and all model-generated output fields (`word`, `part_of_speech`, `definition`, `connotation`, `intensity`, `distinction`, `example`).
2. **Criteria Evaluated:** Every item requires scores and evidence notes across the three canonical Word Cabinet criteria:
   - **`WC_CRIT_1` (Vocabulary Relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
   - **`WC_CRIT_2` (Definition & Connotation Quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
   - **`WC_CRIT_3` (Distinction Usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
3. **Scoring Scale:** Integer scale 1–5 (1 = Serious failure, 2 = Weak performance, 3 = Acceptable with noticeable issues, 4 = Strong with minor issues, 5 = Excellent performance). No half-points or decimal scores permitted.
4. **Mandatory Notes:** Each item includes dedicated fields for:
   - `evidence_notes`: Mandatory concrete textual citations and quotations from the output.
   - `boundary_notes`: Mandatory explanations whenever a judgment sits on the edge between two score points (e.g., 2 vs. 3).

---

## 3. INFORMATION-LEAKAGE AUDIT (BLINDING VERIFICATION)

An automated string and token scan was executed across both rater-facing worksheet files (`.json` and `.md`) to detect potential leakage of experimental metadata.

- **Condition Names:** `baseline`, `experimental`, `exp_wc_01`, `exp_wc_02` $\rightarrow$ **0 occurrences found (Clean)**.
- **Model Identifiers & Digests:** `qwen`, `dostoevsky-baseline`, `c6fb3dc8d97a` $\rightarrow$ **0 occurrences found (Clean)**.
- **Run Identifiers & Timestamps:** `7e82bfc0665e`, `63cb94586e9f`, `20261025`, `20261029`, `20261030` $\rightarrow$ **0 occurrences found (Clean)**.
- **Historical / Preliminary Scores:** `Score 1`, `Score 2`, `Score 3`, `Score 4`, `Score 5` $\rightarrow$ **0 occurrences found (Clean)**.

**Blinding Confirmation:** Evaluators have no observable indicators allowing them to determine whether an item originates from the baseline run or the experimental run.

---

## 4. KEY ISOLATION & DECOUPLING

- The mapping key (`blinded_evaluation_key_20_items.json`) maps each blinded ID (`WC_EVAL_01`–`WC_EVAL_20`) to its underlying condition (`baseline` vs. `experimental_exp_wc_02`) and canonical test case ID (`WC01`–`WC10`).
- **Isolation:** The mapping key is stored exclusively at the root of the experiment directory:  
  `evaluation/experiments/exp_wc_02_distinction_structure/blinded_evaluation_key_20_items.json`
- **Zero Exposure:** The key file is **strictly excluded** from the rater distribution folders (`rater_01/` and `rater_02/`).

---

## 5. RATER DISTRIBUTION PACKAGES & EXACT PATHS

Two independent, isolated distribution packages have been prepared for Rater 1 and Rater 2. Original source files remain untouched.

### Package for Rater 1:
- **Directory:** [`evaluation/experiments/exp_wc_02_distinction_structure/human_evaluation_package/rater_01/`](file:///c:/Users/nisha/OneDrive/Desktop/fyodor/evaluation/experiments/exp_wc_02_distinction_structure/human_evaluation_package/rater_01/)
- **Files Included:**
  1. `INSTRUCTIONS_FOR_INDEPENDENT_HUMAN_RATERS.md` (SHA-256: `72349a7b425cc865ebd7b67abe52624a4fefadf53396788c16c71f3ff39e7709`)
  2. `blinded_evaluation_worksheet_20_items.md` (SHA-256: `05dd0890a845205875b16d06819eb6dcb59183f7835cec5911dc7bd86fef2d9a`)
  3. `blinded_evaluation_worksheet_20_items.json` (SHA-256: `d0af25b9139a7452ed815382c040fd00491d99a9ab784e63ab82265cbde6f6a4`)
  4. `human_rater_01_submission_template.json` (SHA-256: `bcb0537d019d9d2f4360f779ba6aa525c6863aa7d134ef2c978283045bf0337c`)

### Package for Rater 2:
- **Directory:** [`evaluation/experiments/exp_wc_02_distinction_structure/human_evaluation_package/rater_02/`](file:///c:/Users/nisha/OneDrive/Desktop/fyodor/evaluation/experiments/exp_wc_02_distinction_structure/human_evaluation_package/rater_02/)
- **Files Included:**
  1. `INSTRUCTIONS_FOR_INDEPENDENT_HUMAN_RATERS.md` (SHA-256: `72349a7b425cc865ebd7b67abe52624a4fefadf53396788c16c71f3ff39e7709`)
  2. `blinded_evaluation_worksheet_20_items.md` (SHA-256: `05dd0890a845205875b16d06819eb6dcb59183f7835cec5911dc7bd86fef2d9a`)
  3. `blinded_evaluation_worksheet_20_items.json` (SHA-256: `d0af25b9139a7452ed815382c040fd00491d99a9ab784e63ab82265cbde6f6a4`)
  4. `human_rater_02_submission_template.json` (SHA-256: `16c5d41e61e677e5a02b17b09ad1734f6a96ba9d287c537bff5f71eb48ac96c3`)

---

## 6. INDEPENDENT SCORING MANDATE

The instructions explicitly instruct raters:
1. **Strict Independence:** Raters must complete all 20 items without consulting each other, comparing notes, or discussing criteria interpretations prior to official submission.
2. **Standard Scale:** All ratings must use the standard 1–5 integer rubric.
3. **Dual Submission Options:** Raters may submit either via the structured JSON response template (`human_rater_XX_submission_template.json`) or directly by filling out the markdown worksheet (`blinded_evaluation_worksheet_20_items.md`).

---

## 7. RESEARCH INTEGRITY & PRESERVATION CONFIRMATION

- **Zero Fabricated Scores:** No human ratings have been generated, imputed, or simulated. All fields in the rater submission templates are strictly initialized to `null`.
- **Preservation of Baseline Artifacts:** Historical run files (`run_20261025T180347Z...`), master scoring containers (`blinded_human_evaluation_scores_run_20261025T180347Z.json`), and test case specs remain 100% byte-for-byte identical to baseline.
- **Git State:** Clean across all tracked production code. Existing modifications to `.gitignore` and `README.md` remain strictly preserved. Zero files staged, committed, or pushed.

---

## 8. NEXT STEPS & STOP CONDITION

1. **Handoff:** Deliver `rater_01/` materials to Rater 1 and `rater_02/` materials to Rater 2.
2. **Collection:** Await independent return of both completed submission files:
   - `human_rater_01_rated.json` (or marked-up markdown).
   - `human_rater_02_completed.json` (or marked-up markdown).
3. **Execution Halted:** In accordance with the Checkpoint 6D stop condition, execution is complete and halted. No unblinding, ingestion, or score reconciliation will occur until both completed human evaluations are received and authorized by the project lead.

