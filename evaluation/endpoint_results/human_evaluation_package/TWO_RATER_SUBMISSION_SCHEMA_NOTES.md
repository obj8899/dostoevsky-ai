# Dostoevsky AI — Two-Rater JSON Submission Schema Notes

**Document Version:** 1.0.0  
**Status:** WORKFLOW SPECIFICATION — PREPARATION ONLY  
**Applicable Container:** `evaluation/endpoint_results/human_evaluation_package/HUMAN_PRIMARY_UNRATED_RESPONSE_TEMPLATE.json`  

---

## 1. Schema Overview & Structural Hierarchy

The submission template is structured to capture independent human ratings across all 30 evaluation cases with full criterion granularity, concrete textual evidence, and boundary explanations:

```
{
  "metadata": {
    "title": string,
    "version": string,
    "status": string,
    "source_run_id": string,
    "total_items": 30,
    "total_ratings": 90,
    "rater_id": string | null,          <-- Populated upon receipt (e.g. "human_rater_01")
    "submitted_at_utc": string | null,  <-- Populated upon receipt (ISO 8601 UTC timestamp)
    "instructions": string
  },
  "items": [
    {
      "item_id": string,                <-- "LR_ITEM_01".."LR_ITEM_10", "WC_ITEM_01".."WC_ITEM_10", "IM_ITEM_01".."IM_ITEM_10"
      "feature": string,                <-- "literary_rewrite", "word_cabinet", "inner_monologue"
      "scores": {
        "<CRIT_1>": integer (1-5),      <-- Exactly 3 criterion IDs matching the feature
        "<CRIT_2>": integer (1-5),
        "<CRIT_3>": integer (1-5)
      },
      "evidence_notes": {
        "<CRIT_1>": string,             <-- Non-empty string containing text quotation ('...')
        "<CRIT_2>": string,
        "<CRIT_3>": string
      },
      "boundary_notes": {
        "<CRIT_1>": string | null,      <-- Documented dilemma if score is borderline (e.g. 2/3 or 4/5)
        "<CRIT_2>": string | null,
        "<CRIT_3>": string | null
      }
    },
    ... (exactly 30 items)
  ]
}
```

---

## 2. The 14 Mandatory Validation Rules for Human Submissions

Before any submission is accepted into the primary evaluation record, the Coordinator must verify all 14 programmatic and methodological rules:

1. **Clean JSON Syntax:** The file must parse without syntax errors using standard RFC 8259 JSON parsers.
2. **Item Count & Uniqueness:** Exactly `30` items must be present, matching the canonical anonymized item IDs (`LR_ITEM_01`–`10`, `WC_ITEM_01`–`10`, `IM_ITEM_01`–`10`) with zero duplicate or missing entries.
3. **Feature-Criterion Matching:** Each item must contain exactly the three criterion IDs specified for its feature:
   - Literary Rewrite: `LR_CRIT_1`, `LR_CRIT_2`, `LR_CRIT_3`
   - Word Cabinet: `WC_CRIT_1`, `WC_CRIT_2`, `WC_CRIT_3`
   - Inner Monologue: `IM_CRIT_1`, `IM_CRIT_2`, `IM_CRIT_3`
4. **Integer Score Range:** Every criterion score must be an integer between 1 and 5 ($1 \le 	ext{score} \le 5$). Nulls, boolean values (`True`/`False`), floats (`3.5`), letter grades, and strings are strictly rejected.
5. **Direct Quotation in Evidence Notes:** Every evidence note must be non-empty and contain direct quotations (enclosed in single quotes `'...'`) or specific syntactic citations referencing the model generated output.
6. **Boundary Notes Compliance:** Borderline or ambiguous scores (particularly near 2/3, 3/4, or 4/5) must document an explicit boundary note explaining why the selected rating was favored over the adjacent score.
7. **Score 1 and 2 Justification:** Scores of 1 or 2 must explicitly name the serious flaw, factual contradiction, or triggered failure condition that disqualified the prose from Scale 3.
8. **Score 5 Endpoint Justification:** Scores of 5 must explicitly explain why the output achieves exceptional restraint, perfect fidelity, or outstanding nuance warranting an endpoint score rather than a 4.
9. **Provenance & Identifiers:** `metadata.rater_id` must be populated with the designated workflow identifier (`human_rater_01` or `human_rater_02`), and `metadata.submitted_at_utc` must contain an authentic ISO 8601 UTC timestamp.
10. **Zero Tier Leakage:** The submission must not contain AI-assisted preliminary scores, preliminary rationales, mapping keys, or adjudicated final scores.
11. **Output Parity:** The submission structure and item IDs must correspond 1-to-1 with the blinded worksheet without altering item order or definitions.
12. **Length Diagnostic Decoupling:** Raters must evaluate scenario fidelity, perspective, and progression on qualitative literary merit. Diagnostic word-count warnings recorded by automated tests must not be used to dock qualitative points.
13. **Incomplete vs. Partial Output Rule:**
    - Malformed or truncated outputs (e.g. broken sentences, unclosed syntax) receive Score 1 for structural failure without guessing.
    - Valid partial responses with honest diagnostic warnings (e.g. 5 of 6 entries returned) are evaluated on their literary merits without automatic structural failure.
14. **No Content Reconstruction:** Raters must never reconstruct, guess, or invent missing or truncated text.

---

## 3. Direct Mapping to the Primary Container Tier

The submission schema is designed for seamless, lossless ingestion into `blinded_human_evaluation_scores_run_20261025T180347Z.json`.

For each item, the validated submission record:
```json
{
  "item_id": "LR_ITEM_01",
  "scores": { "LR_CRIT_1": 4, "LR_CRIT_2": 3, "LR_CRIT_3": 4 },
  "evidence_notes": { "LR_CRIT_1": "...", "LR_CRIT_2": "...", "LR_CRIT_3": "..." },
  "boundary_notes": { "LR_CRIT_1": null, "LR_CRIT_2": "...", "LR_CRIT_3": null }
}
```
maps directly to an entry appended to `evaluations.human_primary`:
```json
{
  "rater_id": "human_rater_01",
  "scores": { "LR_CRIT_1": 4, "LR_CRIT_2": 3, "LR_CRIT_3": 4 },
  "evidence_notes": { "LR_CRIT_1": "...", "LR_CRIT_2": "...", "LR_CRIT_3": "..." },
  "boundary_notes": { "LR_CRIT_1": null, "LR_CRIT_2": "...", "LR_CRIT_3": null },
  "rated_at_utc": "2026-10-29T14:00:00Z"
}
```
This architecture preserves complete rater independence, zero tier collision, and 100% auditability.
