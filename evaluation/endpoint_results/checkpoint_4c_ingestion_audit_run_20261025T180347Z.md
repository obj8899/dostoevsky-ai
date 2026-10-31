# Dostoevsky AI — Checkpoint 4C: Authorized Score Ingestion Audit Report

**Evaluation Phase:** Phase 4A Endpoint Human-Primary Evaluation  
**Checkpoint:** Checkpoint 4C (Authorized Score Ingestion & Consensus Recording)  
**Evaluator / Auditor Role:** AI Evaluation Engineer, Database Integrity Auditor  
**Ingestion Date (UTC):** 2026-10-29T14:52:51Z  
**Ingestion Status:** SUCCESSFUL & VALIDATED  

---

## 1. Scope of Authorization & Governance

The project lead explicitly authorized:
1. Ingestion of both original human rating sets (`human_rater_01_rated.json` and `human_rater_02_completed.json`) into `evaluations.human_primary` in `evaluation/endpoint_results/blinded_human_evaluation_scores_run_20261025T180347Z.json`.
2. Recording the three approved consensus decisions in `evaluations.adjudicated_final`:
   - `LR_ITEM_09` / `LR_CRIT_1` (*meaning_and_fact_preservation*): **2**
   - `LR_ITEM_09` / `LR_CRIT_2` (*psychological_depth*): **2**
   - `WC_ITEM_09` / `WC_CRIT_1` (*vocabulary_relevance*): **3**
3. Full preservation of all original ratings, evidence notes, boundary notes, and rater provenance without silent rounding or data loss.

---

## 2. Ingestion Execution & Content Verification

### A. `evaluations.human_primary` Tier Ingestion
- **Total Items Updated:** Exactly 30 items.
- **Rater 01 Ingested Ratings:** Exactly 90 criterion-level ratings.
- **Rater 02 Ingested Ratings:** Exactly 90 criterion-level ratings.
- **Total Human Ratings Ingested:** Exactly 180 ratings across both raters.
- **Pairing & Integrity:** Ratings paired strictly by `(item_id, criterion_id)`. All scores verified as integers between 1 and 5.
- **Rater 1 Provenance & Disclosure:**
  - `rater_id`: `claude_ai_assigned_human_rater_01_template` (preserved verbatim from submission metadata)
  - `rated_at_utc`: `2026-10-29`
  - `reported_disclosure`: *"Evaluator reports independently choosing the ratings and substantive judgments; AI was used to structure the data."* (Recorded as reported disclosure, not independently verified fact)
- **Rater 2 Provenance:**
  - `rater_id`: `human_rater_02`
  - `rated_at_utc`: `2026-10-29T13:45:00Z`
- **Notes Coverage:** 100% of evidence notes and boundary notes were transferred verbatim from source files.

### B. `evaluations.adjudicated_final` Tier Consensus Recording
Exactly three consensus decisions were recorded with full provenance and written rationales from the Checkpoint 4B review:

#### 1. `LR_ITEM_09` — `LR_CRIT_1` (`meaning_and_fact_preservation`)
- **Final Approved Score:** `2`
- **Original Rater Scores:** Rater 1 = `2`, Rater 2 = `4` (Signed Diff: `-2`)
- **Approval Status:** `APPROVED_BY_PROJECT_LEAD`
- **Approval Checkpoint:** `Checkpoint 4C`
- **Approval Timestamp (UTC):** `2026-10-29T14:52:51Z`
- **Reference Report:** `evaluation/endpoint_results/checkpoint_4b_adjudication_review_run_20261025T180347Z.md`
- **Written Rationale:** *"Adjudicated to 2 (project_lead approval, Checkpoint 4C). Fails canonical failure condition: omits direct spoken forgiveness ('I said it was fine'), replacing it with ambiguous cognitive dismissal ('dismissed the incident'), and mutates the timeline ('the following day' vs. source's 'the rest of the day'). Original ratings: Rater 1 = 2, Rater 2 = 4. Reference: checkpoint_4b_adjudication_review_run_20261025T180347Z.md."*

#### 2. `LR_ITEM_09` — `LR_CRIT_2` (`psychological_depth`)
- **Final Approved Score:** `2`
- **Original Rater Scores:** Rater 1 = `2`, Rater 2 = `4` (Signed Diff: `-2`)
- **Approval Status:** `APPROVED_BY_PROJECT_LEAD`
- **Approval Checkpoint:** `Checkpoint 4C`
- **Approval Timestamp (UTC):** `2026-10-29T14:52:51Z`
- **Reference Report:** `evaluation/endpoint_results/checkpoint_4b_adjudication_review_run_20261025T180347Z.md`
- **Written Rationale:** *"Adjudicated to 2 (project_lead approval, Checkpoint 4C). The rubric explicitly demands psychological tension conveyed 'through concrete behavioral detail rather than melodrama or abstract emotion labels'. The prose contains zero behavioral micro-details and relies entirely on abstract emotion labels ('harbored anger') and bureaucratic summary phrases ('dismissed the incident', 'withdrew from engaging'). Original ratings: Rater 1 = 2, Rater 2 = 4. Reference: checkpoint_4b_adjudication_review_run_20261025T180347Z.md."*

#### 3. `WC_ITEM_09` — `WC_CRIT_1` (`vocabulary_relevance`)
- **Final Approved Score:** `3`
- **Original Rater Scores:** Rater 1 = `2`, Rater 2 = `4` (Signed Diff: `-2`)
- **Approval Status:** `APPROVED_BY_PROJECT_LEAD`
- **Approval Checkpoint:** `Checkpoint 4C`
- **Approval Timestamp (UTC):** `2026-10-29T14:52:51Z`
- **Reference Report:** `evaluation/endpoint_results/checkpoint_4b_adjudication_review_run_20261025T180347Z.md`
- **Written Rationale:** *"Adjudicated to 3 (project_lead approval, Checkpoint 4C). Complete structural generation of 8 entries covering the core prompt elements warrants baseline Scale 3. However, literal prompt echoing (4 words taken verbatim from prompt text: 'paralysis', 'thrill', 'craving', 'anticipation') and near-synonym clustering ('anxiety', 'unease', 'foreboding') preclude Scale 4. Original ratings: Rater 1 = 2, Rater 2 = 4. Reference: checkpoint_4b_adjudication_review_run_20261025T180347Z.md."*

#### Non-Adjudicated Items Confirmation
- For all other 87 criterion pairs, `adjudicated_final.scores` remains `null`, `adjudication_rationale` remains `null`, and `adjudicator_id` remains `null`.
- No non-divergent consensus scores were fabricated, inferred, or prematurely closed.

---

## 3. Cryptographic Verification & Artifact Preservation

### A. Scoring Container Pre- and Post-Ingestion Hashes
| Container Path | Pre-Ingestion SHA-256 | Post-Ingestion SHA-256 | Pre Size | Post Size | Status |
|---|---|---|---|---|---|
| `evaluation/endpoint_results/blinded_human_evaluation_scores_run_20261025T180347Z.json` | `da0be36c4088b23229baf239a4c3b3440b61d2e9efa5827e42105585e4d0ac23` | `81e650d7a65d4f28d7190f99a7c3276aa22ae98862e8c24e18a7d6250f3fbc0b` | 65672 bytes | 161248 bytes | **INGESTED & VALIDATED** |

### B. Source Submissions & Protected Artifact Preservation
All original submissions and protected evaluation records were cryptographically re-verified post-ingestion. Zero external mutations occurred:

| Artifact Path | Expected Baseline SHA-256 | Post-Ingestion SHA-256 | Verification Status |
|---|---|---|---|
| `human_rater_01_rated.json` | `1df8c90c6a7d6aff5c603bfe4135392f9e94c3473d8b051100073d3bdca66315` | `1df8c90c6a7d6aff5c603bfe4135392f9e94c3473d8b051100073d3bdca66315` | **UNCHANGED** |
| `human_rater_02_completed.json` | `3f8fe083ca4aef842d18058d3d1722c37db7cdd8937a818b60a47b24ca6532ee` | `3f8fe083ca4aef842d18058d3d1722c37db7cdd8937a818b60a47b24ca6532ee` | **UNCHANGED** |
| `evaluation/endpoint_results/run_20261025T180347Z_63cb94586e9f4132adf9952aae03efbb.json` | `076ab4aa7e9b57acd5f964c91b6e706031d25bb6713c2aa958339603990ece51` | `076ab4aa7e9b57acd5f964c91b6e706031d25bb6713c2aa958339603990ece51` | **UNCHANGED** |
| `evaluation/endpoint_results/blinded_human_evaluation_key_run_20261025T180347Z.json` | `5051cb5fff73f87b8204a82b5d0e3d02405ae7360ee0a01451777bd6a837ff10` | `5051cb5fff73f87b8204a82b5d0e3d02405ae7360ee0a01451777bd6a837ff10` | **UNCHANGED** |
| `evaluation/endpoint_results/human_primary_agreement_report_run_20261025T180347Z.md` | `fd29d207e157fdc4f521809bff96a081d818682f45b3fd26f63a3a2760435230` | `fd29d207e157fdc4f521809bff96a081d818682f45b3fd26f63a3a2760435230` | **UNCHANGED** |
| `evaluation/endpoint_results/human_primary_disagreements_run_20261025T180347Z.csv` | `66c604af41f7dd8f2bcf6e108a42dbe2fea87e548982088ecc7cff33727f0990` | `66c604af41f7dd8f2bcf6e108a42dbe2fea87e548982088ecc7cff33727f0990` | **UNCHANGED** |
| `evaluation/endpoint_results/human_primary_agreement_metrics_run_20261025T180347Z.json` | `2620d375e5d85e2ad574274263666f37c59e30362562fec4c17505aa4cf008e6` | `2620d375e5d85e2ad574274263666f37c59e30362562fec4c17505aa4cf008e6` | **UNCHANGED** |
| `evaluation/endpoint_results/checkpoint_4b_adjudication_review_run_20261025T180347Z.md` | `2c9dfdd0462ddd87449c13ff22a907ec6d9925d68a4ad5a663bc84ed0c6f7fb2` | `2c9dfdd0462ddd87449c13ff22a907ec6d9925d68a4ad5a663bc84ed0c6f7fb2` | **UNCHANGED** |

---

## 4. Limitations & Scope Compliance

1. **Atomicity Guarantee:** The scoring container update was executed via atomic temporary-file serialization and rename (`os.replace`), eliminating risk of partial or corrupt file states.
2. **Idempotence:** Re-running the ingestion pipeline on the baseline replaces the tier arrays deterministically without duplicate entries.
3. **Git Isolation:** No git commits, tags, or pushes were performed. Working tree status remains clean of unauthorized changes.
