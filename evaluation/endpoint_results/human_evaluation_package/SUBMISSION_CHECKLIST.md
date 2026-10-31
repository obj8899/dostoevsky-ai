# Dostoevsky AI — Human Evaluation Submission Checklist

**Document Version:** 1.0.0  
**Status:** HUMAN-PRIMARY — UNRATED  

Before submitting your evaluation package to the Coordinator, verify that all items below have been completed:

### Rater Self-Verification Checklist
- [ ] **Identification:** Rater ID (e.g. `human_rater_01`) and UTC evaluation date are recorded on the submission.
- [ ] **Coverage:** All 30 items have been evaluated (10 Literary Rewrite, 10 Word Cabinet, 10 Inner Monologue).
- [ ] **Completeness:** Exactly 90 criterion scores are assigned. No score field is left blank, null, or undecided.
- [ ] **Integer Scale:** All scores are integers between 1 and 5 (no decimals like 3.5, no letter grades).
- [ ] **Quotation Evidence:** Every single score has an accompanying evidence note containing direct quotations (`'...'`) from the generated text.
- [ ] **Extreme Score Rationale:** Every score of 1 or 2 explicitly names the fatal defect or triggered failure condition. Every score of 5 justifies why the output warrants the top endpoint over a 4.
- [ ] **Boundary Notes:** Borderline decisions (near 2/3, 3/4, or 4/5) have documented boundary notes explaining the dilemma.
- [ ] **Length Decoupling:** Word count variances were not penalized under qualitative literary criteria.
- [ ] **Independence:** All ratings were assigned independently without consulting other raters or preliminary AI scores.

### Coordinator Intake Verification Checklist
- [ ] Package received from authorized rater.
- [ ] Receipt timestamp logged in UTC.
- [ ] Cryptographic SHA-256 hash calculated and logged for the raw submission.
- [ ] Programmatic validation confirms 90 scores, 90 evidence notes with quotes, and valid integer ranges.
- [ ] Submission archived in immutable records before ingestion into `evaluations.human_primary`.
