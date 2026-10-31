# Instructions for Independent Human Raters
**Evaluation Study:** Dostoevsky AI Word Cabinet Evaluation (`EXP-WC-02`)  
**Scope:** 20 Blinded Output Cases (`WC_EVAL_01` through `WC_EVAL_20`)  
**Criteria per Case:** 3 criteria (60 ratings total per rater)  
**Standard Scale:** Integer scale 1–5  

---

## 1. Core Guidelines for Scientific Integrity

1. **Strictly Independent Scoring:** You must perform your evaluation completely independently. **Do not consult, discuss, or share ratings with the other rater** before all submissions are officially submitted.
2. **Double-Blind Integrity:** You have been provided with 20 blinded cases in randomized order. All condition labels, timestamps, and model identifiers have been removed. Rate each case purely on its observable merits against the context prompt.
3. **Evidence Requirement:** For every criterion score, you must provide an `evidence_note` citing specific textual observations or quotations from the output.
4. **Boundary Notes:** Whenever a score sits on the boundary between two adjacent ratings (e.g. 2 vs 3, or 3 vs 4), provide a concise `boundary_note` explaining what specific factor tipped the judgment.

---

## 2. Standard 1–5 Scoring Scale

* **1 — Serious failure:** Violates fundamental constraints, completely misses the psychological dilemma, or produces incoherent / unreadable entries.
* **2 — Weak performance:** Noticeable drift, shallow psychological depth, trivial or circular distinctions, or generic emotion descriptors.
* **3 — Acceptable with noticeable issues:** Preserves the core emotional dilemma but contains minor drift, cliché, slight repetition, or pedestrian distinctions.
* **4 — Strong with minor issues:** High fidelity to the context, believable and nuanced psychology, disciplined distinctions with only trivial flaws.
* **5 — Excellent performance:** Exceptional nuance, perfect fidelity to the psychological tension, compelling and sharp distinctions.

---

## 3. Rubric Definitions (Word Cabinet)

### `WC_CRIT_1`: Vocabulary Relevance
* **Definition:** Selected terms precisely address the specific emotional or psychological nuance described in the context.
* **Key Considerations:** Do the terms articulate the genuine psychological tension of the prompt, or are they generic emotion words? Do they cover both poles of a conflicting dilemma?

### `WC_CRIT_2`: Definition and Connotation Quality
* **Definition:** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
* **Key Considerations:** Are definitions accurate and free from circularity? Are connotations plausible psychological associations rather than dogmatic claims?

### `WC_CRIT_3`: Distinction Usefulness
* **Definition:** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
* **Key Considerations:** Does the distinction establish an authentic psychological boundary with a plausible nearby neighbor? Does it avoid comparing a word with itself or with other words in the same list? Is the distinction concise, natural, and helpful?

---

## 4. How to Submit

You may complete your ratings either by:
1. Filling in the structured JSON submission template (`human_rater_XX_submission_template.json`), OR
2. Recording your scores directly into the Markdown worksheet under each item's `Ratings:` section.

Ensure all 20 items have integer scores [1-5] for `WC_CRIT_1`, `WC_CRIT_2`, and `WC_CRIT_3`.
