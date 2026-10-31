# Dostoevsky AI — Checkpoint 5.1: Preliminary Metric Reconciliation Audit Report

**Evaluation Phase:** Phase 4A Endpoint Human Evaluation  
**Checkpoint:** Checkpoint 5.1 (Preliminary Metric Reconciliation Audit)  
**Audit Type:** Strictly Read-Only Investigation & Arithmetic Reconciliation  
**Target Scoring Container:** `evaluation/endpoint_results/blinded_human_evaluation_scores_run_20261025T180347Z.json`  
**Run ID:** `run_20261025T180347Z_63cb94586e9f4132adf9952aae03efbb`  
**Date of Reconciliation:** 2026-10-29  

---

## Executive Finding & Root Cause Conclusion

> [!IMPORTANT]
> **ROOT CAUSE CONCLUSION: TRANSCRIPTION / PROSE REPORTING ERROR IN CHAT RESPONSE**  
> 1. **The Authoritative Preliminary Metrics are 3.4333 (Overall), 3.5667 (LR), 3.0333 (WC), and 3.7000 (IM).** These numbers match the exact arithmetic sum and mean of all 90 scores in `evaluations.ai_assisted_preliminary` in the official scoring container, established in Checkpoint 3B, audited in Checkpoint 3B audit, and recorded in the persisted report file `evaluation/endpoint_results/checkpoint_5_final_evaluation_audit.md` (lines 98–99).  
> 2. **The Discrepant Figures (3.3111, 3.1000, 3.3667, 3.4667) were a Chat Response Typo.** They appeared solely in the narrative text of the conversational assistant response at Step 477. They do NOT exist in the persisted on-disk report `checkpoint_5_final_evaluation_audit.md`, nor do they correspond to any dataset, scoring tier, inclusion rule, or mathematical calculation in the repository.

---

## 1. Authoritative Preliminary Scoring Records Audit

### A. Target Record & Identification
- **Container Path:** `evaluation/endpoint_results/blinded_human_evaluation_scores_run_20261025T180347Z.json`
- **Evaluated Tier:** `evaluations.ai_assisted_preliminary`
- **Source Run ID:** `run_20261025T180347Z_63cb94586e9f4132adf9952aae03efbb`
- **Total Items:** Exactly 30 canonical items (`LR_ITEM_01`–`10`, `WC_ITEM_01`–`10`, `IM_ITEM_01`–`10`)
- **Total Criterion Scores:** Exactly 90 integer scores in $[1, 5]$ (3 criteria per item)

### B. Direct Arithmetic Recalculation from Underlying Scores

| Feature | Criteria Analyzed | Score Count ($N$) | Score Sum ($\sum S$) | Exact Mean | Rounded (4 Dec) | Median | Status |
|---|---|---|---|---|---|---|---|
| **Literary Rewrite** | `LR_CRIT_1..3` | 30 | 107 | 107 / 30 | **3.5667** | 4.0 | **AUTHORITATIVE** |
| **Word Cabinet** | `WC_CRIT_1..3` | 30 | 91 | 91 / 30 | **3.0333** | 3.0 | **AUTHORITATIVE** |
| **Inner Monologue** | `IM_CRIT_1..3` | 30 | 111 | 111 / 30 | **3.7000** | 4.0 | **AUTHORITATIVE** |
| **Overall Preliminary** | All 9 Criteria | 90 | 309 | 309 / 90 | **3.4333** | 4.0 | **AUTHORITATIVE** |

---

## 2. Forensic Discrepancy Investigation

### A. Comparison Between Artifacts

| Metric Dimension | Actual Scoring Container (`ai_assisted_preliminary`) | Persisted On-Disk File (`checkpoint_5_final_evaluation_audit.md` §3.1) | Conversational Chat Response (Step 477 §3) | Discrepancy Analysis |
|---|---|---|---|---|
| **Overall Mean** | **3.4333** (309/90) | **3.4333** | 3.3111 | Chat response hallucination; on-disk file is correct |
| **Literary Rewrite** | **3.5667** (107/30) | **3.5667** | 3.1000 | Chat response hallucination; on-disk file is correct |
| **Word Cabinet** | **3.0333** (91/30) | **3.0333** | 3.3667 | Chat response hallucination; on-disk file is correct |
| **Inner Monologue** | **3.7000** (111/30) | **3.7** | 3.4667 | Chat response hallucination; on-disk file is correct |

### B. Detailed Verification of the On-Disk Checkpoint 5 Report
Inspection of `evaluation/endpoint_results/checkpoint_5_final_evaluation_audit.md` confirmed lines 96–100 state verbatim:
```markdown
### 1. `ai_assisted_preliminary` Tier (Reference Baseline)
- **Scope:** All 90 criterion ratings populated during Checkpoint 3B.
- **Overall Mean Score:** **3.4333** (Median: **4.0**)
- **Feature Means:** Literary Rewrite: **3.5667** | Word Cabinet: **3.0333** | Inner Monologue: **3.7**
```
This proves that the script that generated the report on disk computed and recorded the mathematically correct numbers. The erroneous numbers (3.3111, 3.1000, 3.3667, 3.4667) were introduced solely in the manual narrative summary written in the chat response window.

### C. Mathematical Properties of the Discrepant Numbers
Analysis of the numbers `3.1000`, `3.3667`, `3.4667`, and `3.3111` revealed:
- $3.1000 \times 30 = 93$
- $3.3667 \times 30 = 101.001 \approx 101$
- $3.4667 \times 30 = 104.001 \approx 104$
- Total sum: $93 + 101 + 104 = 298$
- Mean: $298 / 90 = 3.311111... \approx 3.3111$
A full scan across all repository files, git commit histories, and baseline runs confirmed that no dataset or criterion grouping yields sums of 93, 101, 104, or 298. These figures represent an ungrounded hallucination in the chat assistant's text generation.

---

## 3. Independent Audit of Human-Primary Descriptive Statistics

All descriptive statistics for the `human_primary` tier were independently recalculated directly from the underlying integer scores:

### A. Rater 1 Underlying Metrics ($N = 90$ Ratings)
- **Literary Rewrite (30 ratings):** Sum = 97 | Mean = **3.2333** | Median = 3.0
- **Word Cabinet (30 ratings):** Sum = 73 | Mean = **2.4333** | Median = 2.0
- **Inner Monologue (30 ratings):** Sum = 94 | Mean = **3.1333** | Median = 3.0
- **Overall Rater 1 (90 ratings):** Sum = 264 | Mean = **2.9333** | Median = 3.0

### B. Rater 2 Underlying Metrics ($N = 90$ Ratings)
- **Literary Rewrite (30 ratings):** Sum = 117 | Mean = **3.9000** | Median = 4.0
- **Word Cabinet (30 ratings):** Sum = 81 | Mean = **2.7000** | Median = 3.0
- **Inner Monologue (30 ratings):** Sum = 97 | Mean = **3.2333** | Median = 3.0
- **Overall Rater 2 (90 ratings):** Sum = 295 | Mean = **3.2778** | Median = 3.0

### C. Combined Human Descriptive Averages ($N = 180$ Ratings)
- **Overall Human Mean:** $\frac{264 + 295}{180} = \frac{559}{180} = \mathbf{3.1056}$ (Median: **3.0**)
- **Mean Signed Difference ($R1 - R2$):** $2.9333 - 3.2778 = \mathbf{-0.3444}$ points

### D. Audit of Narrative Section 4 in `checkpoint_5_final_evaluation_audit.md`
An additional minor discrepancy was identified in the narrative subsection headings of Section 4 in `checkpoint_5_final_evaluation_audit.md`:
- Section 4.A heading states: `(Mean Score: R1 2.67 / R2 3.33)` instead of `(R1 3.23 / R2 3.90)`
- Section 4.B heading states: `(Mean Score: R1 2.90 / R2 3.17)` instead of `(R1 2.43 / R2 2.70)`
- Section 4.C heading states: `(Mean Score: R1 3.23 / R2 3.33)` instead of `(R1 3.13 / R2 3.23)`
These heading strings were draft illustrative annotations that were not wired dynamically to the statistical engine. The authoritative feature-level means for Rater 1 and Rater 2 are those correctly tabulated in Section 2.B and in `checkpoint_5_descriptive_summaries.csv`.

---

## 4. Preservation & Cryptographic Hash Audit

All source files and evaluation records were verified cryptographically before and after reconciliation. Zero byte mutations occurred:

| Artifact Path | File Size | SHA-256 Hash | Verification Status |
|---|---|---|---|
| `evaluation/endpoint_results/blinded_human_evaluation_scores_run_20261025T180347Z.json` | 161,248 B | `81e650d7a65d4f28d7190f99a7c3276aa22ae98862e8c24e18a7d6250f3fbc0b` | **UNCHANGED** |
| `human_rater_01_rated.json` | 49,682 B | `1df8c90c6a7d6aff5c603bfe4135392f9e94c3473d8b051100073d3bdca66315` | **UNCHANGED** |
| `human_rater_02_completed.json` | 27,598 B | `3f8fe083ca4aef842d18058d3d1722c37db7cdd8937a818b60a47b24ca6532ee` | **UNCHANGED** |
| `evaluation/endpoint_results/checkpoint_5_final_evaluation_audit.md` | 17,298 B | `c25bfd2161d8740156c39791210a93c138161bc1a9abc20b19d6e21d46fb8f30` | **UNCHANGED** |
| `evaluation/endpoint_results/checkpoint_5_descriptive_summaries.csv` | 1,603 B | `7d293b302fc14177e15ea096dc22d6a96560399e393b112e0f5ff6762157e579` | **UNCHANGED** |
| `evaluation/endpoint_results/checkpoint_5_1_preliminary_metric_reconciliation.md` | [Generated] | [New Report] | **NEW RECONCILIATION REPORT** |
