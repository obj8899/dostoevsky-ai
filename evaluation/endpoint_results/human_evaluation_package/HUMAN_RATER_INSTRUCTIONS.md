# Dostoevsky AI — Blinded Human Rater Instructions

**Document Version:** 1.0.0  
**Status:** HUMAN-PRIMARY — UNRATED  
**Evaluation Scope:** 30 Blinded Output Cases (90 Criterion Ratings)  
**Evaluator Role:** Independent Human Evaluator  

---

## 1. Introduction & Evaluation Purpose

Welcome to the human evaluation of Dostoevsky AI. In this study, you will evaluate 30 model-generated outputs spanning three literary features:
1. **Literary Rewrite** (10 items: `LR_ITEM_01` to `LR_ITEM_10`)
2. **Word Cabinet** (10 items: `WC_ITEM_01` to `WC_ITEM_10`)
3. **Inner Monologue** (10 items: `IM_ITEM_01` to `IM_ITEM_10`)

For each item, you will assign integer scores from **1 to 5** across exactly three applicable criteria, accompanied by concise observable evidence notes and boundary explanations.

---

## 2. Global Scoring Scale (1–5)

You must use the following standard 5-point scale across all features. Do not use half-points or decimal scores.

* **1 — Serious failure:** Violates fundamental constraints, major factual hallucinations, or unreadable prose.
* **2 — Weak performance:** Noticeable drift, shallow psychological depth, or frequent stylistic flaws.
* **3 — Acceptable with noticeable issues:** Preserves core task but contains minor drift, cliché, or slight repetition.
* **4 — Strong with minor issues:** High fidelity, believable psychology, disciplined prose with trivial flaws.
* **5 — Excellent performance:** Exceptional nuance, perfect fidelity, compelling literary restraint.

---

## 3. Mandatory Evidence & Note Requirements

### A. Concrete Textual Quotations Required
Every criterion score requires an evidence note. **You must quote specific words, phrases, or observable textual features from the output.**
* *Acceptable Note:* `Score 4. Captures the physical hesitation and quiet moral restraint well through 'intending to retrieve... yet I refrained'.`
* *Unacceptable Note:* `Score 4. The writing felt very restrained and realistic.` (Fails because it cites no text).

### B. Mandatory Justification for Extreme Scores (1, 2, and 5)
* **For Scores of 1 or 2:** You must explicitly identify which serious flaw, factual contradiction, or case-specific failure condition was triggered, explaining why a score of 3 was disqualified.
* **For Scores of 5:** You must explain why the output achieves exceptional restraint, perfect fidelity, or outstanding nuance warranting an endpoint score rather than a 4.

### C. Boundary Notes for Borderline Decisions
Where an output sits on the boundary between two adjacent ratings (e.g. between 2 and 3, or between 4 and 5):
1. Assign the primary integer score that best captures the dominant quality.
2. In the **Boundary Notes** field, explicitly explain the tension (e.g. `"Boundary note: 3 vs 2; semantic slip touches Scale 2 drift, but core action sequence preserved."`).

---

## 4. Critical Protocol Rules

### Rule 1: Decoupling Length Compliance from Literary Quality
* In features like Inner Monologue, outputs may vary in length from requested word ranges.
* **Do not penalize qualitative literary criteria (fidelity, perspective, progression) solely because an output is shorter or longer than requested.** Length metrics are checked separately by automated systems. Evaluate the literary prose on its merits.

### Rule 2: Handling Incomplete vs. Malformed Outputs
* **Malformed or Truncated Output:** If an output cuts off abruptly mid-sentence, contains broken syntax, or unclosed markup:
  - Do not reconstruct or guess the missing text.
  - Assign a score of **1** to affected criteria, citing structural failure.
* **Valid Partial Output with Warning:** If the model returns fewer entries than requested (e.g. 5 words instead of 6) but each returned entry is complete, grammatically valid, and well-formed:
  - Do not automatically assign 1 to all criteria.
  - Evaluate the quality of the returned entries on their literary merits, and note the missing count in boundary notes if relevant.

### Rule 3: Strict Blinding & Independence
* Do not look at external model benchmarks, preliminary scores, or other raters' evaluations.
* Rate items in sequential order within feature blocks to maintain consistent cognitive calibration.
