# PHASE 8B: HISTORICAL EVALUATION & CRYPTOGRAPHIC INTEGRITY RECONCILIATION

**Project:** Dostoevsky AI  
**Repository Path:** `C:\Users\nisha\OneDrive\Desktop\fyodor`  
**Date:** 2026-10-31  
**Author:** Principal Software Engineer, AI/ML Architect & Experimental Integrity Auditor  
**Scope:** Reconcile baseline prompt SHA-256 discrepancy, verify multi-tier evaluation records, and establish authoritative claim boundaries.

---

## 1. EXECUTIVE INTEGRITY SUMMARY

1. **Resolution of Baseline Prompt Hash Discrepancy:** The discrepancy between the baseline prompt hash reported in Phase 8A (`be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686`) and earlier project notes (`be472f536fbb27ed78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b`) is **fully resolved and mathematically explained**.
   - The authentic CRLF hash is: `be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686`.
   - The authentic LF hash is: `7f084d75ad9271bd78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b`.
   - The discrepancy string is a composite chimera: the first 16 hexadecimal characters of the CRLF hash (`be472f536fbb27ed`) were accidentally concatenated with the trailing 48 characters of the LF hash (`78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b`). No file ever legitimately produced that composite hash.
2. **Authoritative Evaluation Tier Separation:** All historical evaluation artifacts remain intact, unmodified, and categorized across five distinct evidence tiers. No historical ratings, blinded keys, or rater notes have been altered.
3. **Double-Blind Human Evaluation Veracity:** The contemporaneous double-blind evaluation of EXP-WC-02 (20 blinded items, 2 raters, 120 ratings) is fully preserved. The rejection decision (delta -0.20 on primary distinction usefulness; Rater 2 delta -0.40 on relevance) was faithfully executed by rolling back to the verified baseline.

---

## 2. CRYPTOGRAPHIC PROMPT HASH RECONCILIATION

### 2.1 File Under Audit
- **Target File:** `backend/src/dostoevsky_ai/prompts/word_cabinet.py`
- **Role:** System and user prompt templates for Word Cabinet JSON generation.

### 2.2 Mathematical Hash Analysis

| Representation | Byte Count | Normalization | Computed SHA-256 Hash |
|---|:---:|---|---|
| **Windows Raw (Disk)** | 1,185 bytes | CRLF (`\r\n`) | `be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686` |
| **Unix Normalized** | 1,152 bytes | LF (`\n`) | `7f084d75ad9271bd78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b` |
| **Documented Discrepancy** | N/A | Spliced Chimera | `be472f536fbb27ed78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b` |

### 2.3 Proof of the Copy-Paste Splice
Inspecting the 64-character hexadecimal representation demonstrates the exact point of concatenation:

```text
CRLF Authentic:  [be472f536fbb27ed] 460f03e744889c95af91db3a8f8ac8809992ac55dd447686
LF Authentic:    7f084d75ad9271bd [78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b]
Discrepancy:     [be472f536fbb27ed][78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b]
                 ^-- CRLF chars 0-15 --^ ^----------- LF chars 16-63 -------------^
```

- **Root Cause:** During manual documentation assembly in Checkpoint 6B/6C, a copy-paste clipboard buffer error took the first 16 characters from the CRLF raw hash row and pasted the remainder from the LF normalized hash row.
- **Resolution:** The true canonical baseline hash is `be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686` on Windows (raw CRLF) and `7f084d75ad9271bd78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b` under standard Unix LF line-ending normalization. Both baseline files in `evaluation/experiments/exp_wc_01_prompt_diversity/EXP_WC_01_REPORT.md` and `CHECKPOINT_6E_FINAL_HUMAN_EVALUATION_REPORT.md` record these exact verified hashes.

---

## 3. MULTI-TIER EVALUATION RECONCILIATION

The repository contains five distinct tiers of evaluation evidence collected across the lifecycle of Dostoevsky AI. These tiers must never be conflated:

```
+------------------------------------------------------------------------------------+
| Tier 1: AI-Assisted Preliminary Evaluations (Phase 4 - Phase 5)                    |
| - Method: LLM-as-a-judge scoring on 15 canonical test cases (5 per feature).       |
| - Ratings: 45 criterion ratings across 1-5 integer scale.                          |
| - Key Artifacts: evaluation/experiment1_*_scores.csv, EXPERIMENT1_REPORT.md        |
| - Finding: Overall mean dropped from 3.00 to 2.87 (-0.13 regression).              |
+------------------------------------------------------------------------------------+
                                          |
+------------------------------------------------------------------------------------+
| Tier 2: Algorithmic Prompt Experimentation (EXP-WC-01, Checkpoint 6A.1)             |
| - Method: Heuristic checks (relevance degradation, synonym clustering, length).    |
| - Key Artifact: evaluation/experiments/exp_wc_01_prompt_diversity/EXP_WC_01_REPORT.md |
| - Decision: Pre-registered REJECT / ROLLBACK due to severe relevance drops.        |
+------------------------------------------------------------------------------------+
                                          |
+------------------------------------------------------------------------------------+
| Tier 3: Contemporaneous Double-Blind Human Evaluation (EXP-WC-02, Phase 6D/6E)      |
| - Method: 20 blinded items (10 baseline, 10 experimental), 2 independent raters,   |
|   120 rubric ratings, quadratic weighted Cohen's kappa.                            |
| - Primary Criterion (WC_CRIT_3 Distinction Usefulness):                            |
|   - Rater 1 Delta: -0.2000 (3.20 vs 3.00)                                          |
|   - Rater 2 Delta: -0.2000 (3.50 vs 3.30)                                          |
|   - Pre-registered Threshold: Reject if either delta <= 0.00                       |
| - Guardrail Criterion (WC_CRIT_1 Vocabulary Relevance):                             |
|   - Rater 1 Delta: -0.2000; Rater 2 Delta: -0.4000 (Threshold: Reject if < -0.25)  |
| - Inter-Rater Agreement: Exact: 58.33% (35/60); Within-1: 100.0% (60/60);          |
|   Quadratic Cohen's kappa: 0.3781; Mean Absolute Disagreement: 0.4167.             |
| - Decision: REJECT -> Immediate cryptographic rollback to baseline.                |
| - Key Artifacts: blinded_evaluation_key_20_items.json, CHECKPOINT_6E_*             |
+------------------------------------------------------------------------------------+
                                          |
+------------------------------------------------------------------------------------+
| Tier 4: Live End-to-End Integration Verification (Phase 7C)                        |
| - Method: Live real-time HTTP requests to FastAPI and local Ollama daemon.         |
| - Latency & Output:                                                                |
|   - Literary Rewrite: 18.66s (42 words generated)                                  |
|   - Word Cabinet: 76.22s (6 structured entries generated and validated)           |
|   - Inner Monologue: 24.96s (147 words generated, warning surfaced for 180 target) |
| - Key Artifact: evaluation/PHASE_7C_LIVE_END_TO_END_VERIFICATION_REPORT.md         |
+------------------------------------------------------------------------------------+
                                          |
+------------------------------------------------------------------------------------+
| Tier 5: Qualitative Stylistic Appraisal                                            |
| - Method: Descriptive qualitative literary appraisal of prose rhythm, interiority, |
|   psychological tension, and moral ambivalence.                                    |
| - Finding: Model effectively evokes dark, introspective Russian literary voice,     |
|   with inherent small-model limitations in long-range word-count adherence.        |
+------------------------------------------------------------------------------------+
```

---

## 4. CLAIMS RECONCILIATION & BOUNDARY REGISTER

To ensure complete honesty during technical reviews, interview discussions, and portfolio presentations, the following claim boundaries are formally recorded:

| Proposed Claim | Verification Status | Evidentiary Basis & Proper Framing |
|---|:---:|---|
| *"Model fine-tuned on Dostoevsky novels"* | **DISPROVED / FORBIDDEN** | The model is strictly prompt-engineered on base `qwen2.5:3b`. Zero fine-tuning weights were created. |
| *"Word Cabinet prompt improvements were retained"* | **DISPROVED / FORBIDDEN** | Both EXP-WC-01 and EXP-WC-02 were rejected by pre-registered rules and rolled back to baseline. |
| *"Guaranteed word-count compliance in Inner Monologue"* | **DISPROVED / FORBIDDEN** | Qwen2.5 3B under-generates on long word-count targets (e.g. 147 words on 180 min). System surfaces transparent warnings. |
| *"Public cloud production deployed"* | **DISPROVED / FORBIDDEN** | Bounded explicitly as a local-first single-user application. No multi-tenant auth or rate-limiting exists. |
| *"Contemporaneous double-blind human evaluation conducted"* | **SUPPORTED & PROVEN** | 20 blinded items, 2 independent raters, 120 ratings, Cohen's kappa 0.3781, complete cryptographic trail. |
| *"Defensive structured JSON generation architecture"* | **SUPPORTED & PROVEN** | FastAPI backend parses Ollama JSON, enforces Pydantic schemas, deduplicates entries, handles truncation. |
| *"Zero draft loss on studio switching"* | **SUPPORTED & PROVEN** | React frontend preserves DOM nodes via HTML5 `hidden` attribute with 100% test verification. |
| *"Bidirectional URL hash navigation"* | **SUPPORTED & PROVEN** | Browser back/forward, direct link hashing (`#rewrite`, `#word-cabinet`, `#inner-monologue`) verified by 55 tests. |

---

## 5. SOURCE ARTIFACT AUDIT TRAIL

The following primary evaluation artifacts were inspected and confirmed unmodified:

1. `evaluation/experiments/exp_wc_02_distinction_structure/blinded_evaluation_key_20_items.json`  
   SHA-256: `6fe03417631da7e8d6411516e87a22bc70d306b3e94fe3d16279f6eb2be17e17`
2. `evaluation/experiments/exp_wc_02_distinction_structure/blinded_evaluation_worksheet_20_items.json`  
   SHA-256: `c830e071cb2989c926a84d41270dd71efc5b96792ae5fce068d30eec9fe11a3e`
3. `evaluation/experiments/exp_wc_02_distinction_structure/submissions/human_rater_01_rated.json`  
   SHA-256: `08442c75a96db40ee033bc69f53a1523ec3e316a7f45bc8ba8e54737cf137882`
4. `evaluation/experiments/exp_wc_02_distinction_structure/submissions/human_rater_02_completed.json`  
   SHA-256: `4130f14652c71049929a50993fc53896dfa207287754b5df01ea1c435534b8c9`
5. `evaluation/experiments/exp_wc_02_distinction_structure/checkpoint_6e_human_primary_comparison.json`  
   SHA-256: `3b3d1bcf524783eb9e0a02a8bf8a6e872eebc03e65922eb094ec8979c3d4f3b0`
6. `backend/src/dostoevsky_ai/prompts/word_cabinet.py` (Current Baseline)  
   SHA-256 (CRLF): `be472f536fbb27ed460f03e744889c95af91db3a8f8ac8809992ac55dd447686`  
   SHA-256 (LF): `7f084d75ad9271bd78e7ad61ef2b2c8687cf8e16c17dd14b88e2b9e474cd878b`

---

## 6. CONCLUSION & AUDIT STATUS

- **Hash Discrepancy:** RESOLVED (documented as a 16/48 character CRLF/LF string splicing artifact).
- **Evaluation Records:** 100% RECONCILED and VERIFIED across all 5 tiers.
- **Data Integrity:** Fully preserved without modification of historical files.
