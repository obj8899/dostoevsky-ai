"""
generate_blinded_worksheet.py
-----------------------------
Generates a strictly blinded human-evaluation worksheet and decoupled mapping key
for Dostoevsky AI Phase 4A evaluation results.

Preserves the exact model outputs without altering grammar, formatting, or prose.
Correctly extracts authoritative request payload fields for all three features:
  - Literary Rewrite: text
  - Word Cabinet: context, count
  - Inner Monologue: scenario, perspective, min_words, max_words
Extracts all 7 Word Cabinet schema fields: word, part_of_speech, definition, connotation, intensity, distinction, example.
Strips all model provenance, latency, HTTP status, contract status, and automated check diagnostics.
"""

import json
import hashlib
import random
from pathlib import Path
from datetime import datetime, timezone

def generate_blinded_evaluation():
    repo_root = Path(__file__).resolve().parent.parent
    run_path = repo_root / "evaluation" / "endpoint_results" / "run_20261025T180347Z_63cb94586e9f4132adf9952aae03efbb.json"
    spec_path = repo_root / "evaluation" / "endpoint_test_cases.json"
    
    assert run_path.exists(), f"Run artifact missing: {run_path}"
    assert spec_path.exists(), f"Spec missing: {spec_path}"
    
    with open(run_path, "rb") as f:
        run_data = json.load(f)
    with open(spec_path, "r", encoding="utf-8") as f:
        spec_data = json.load(f)
        
    run_id = run_data["metadata"]["run_id"]
    # Deterministic seed from run_id SHA256 hex prefix (evaluates to 1859518707)
    seed_hex = hashlib.sha256(run_id.encode("utf-8")).hexdigest()[:8]
    seed = int(seed_hex, 16)
    rng = random.Random(seed)
    
    res_by_id = {r["test_id"]: r for r in run_data["results"]}
    spec_by_id = {tc["id"]: tc for tc in spec_data["test_cases"]}
    rubric_defs = spec_data["rubric_definitions"]
    
    feature_groups = [
        ("literary_rewrite", [f"LR{i:02d}" for i in range(1, 11)], "LR_ITEM_"),
        ("word_cabinet", [f"WC{i:02d}" for i in range(1, 11)], "WC_ITEM_"),
        ("inner_monologue", [f"IM{i:02d}" for i in range(1, 11)], "IM_ITEM_"),
    ]
    
    worksheet_items = []
    key_mappings = []
    
    for feature, ids, prefix in feature_groups:
        shuffled_ids = list(ids)
        rng.shuffle(shuffled_ids)
        feat_crit_defs = rubric_defs["feature_criteria"][feature]
        
        for idx, orig_id in enumerate(shuffled_ids, 1):
            item_id = f"{prefix}{idx:02d}"
            res = res_by_id[orig_id]
            spec = spec_by_id[orig_id]
            
            # Decoupled key mapping
            key_mappings.append({
                "item_id": item_id,
                "test_id": orig_id,
                "feature": feature,
                "test_case_name": spec["name"],
                "historical_reference": spec.get("historical_reference"),
                "feature_index": idx
            })
            
            # Criteria definitions with case-specific guidance
            tc_he = spec.get("human_evaluation", {})
            cg = tc_he.get("criteria_guidance", {})
            fc = tc_he.get("failure_conditions", [])
            
            item_criteria = []
            scoring_dict = {}
            for c in feat_crit_defs:
                cid = c["criterion_id"]
                item_criteria.append({
                    "criterion_id": cid,
                    "name": c["name"],
                    "description": c["description"],
                    "guidance": cg.get(cid, "")
                })
                scoring_dict[cid] = None
            
            scoring_dict["evidence_notes"] = None
            scoring_dict["rater_id"] = None
            scoring_dict["rated_at_utc"] = None
            
            # Authoritative Request Payload & Generated Output extraction per feature
            req = res["request_payload"]
            
            if feature == "literary_rewrite":
                input_ctx = {
                    "text": req.get("text", "")
                }
                gen_out = {
                    "rewritten_text": res["response_body"].get("rewritten_text", "")
                }
            elif feature == "word_cabinet":
                input_ctx = {
                    "context": req.get("context", ""),
                    "count": req.get("count", 3)
                }
                raw_words = res["response_body"].get("words", [])
                cleaned_words = []
                for w in raw_words:
                    cleaned_words.append({
                        "word": w.get("word", ""),
                        "part_of_speech": w.get("part_of_speech", ""),
                        "definition": w.get("definition", ""),
                        "connotation": w.get("connotation", ""),
                        "intensity": w.get("intensity", ""),
                        "distinction": w.get("distinction", ""),
                        "example": w.get("example", "")
                    })
                gen_out = {
                    "words": cleaned_words
                }
            elif feature == "inner_monologue":
                input_ctx = {
                    "scenario": req.get("scenario", ""),
                    "perspective": req.get("perspective", ""),
                    "min_words": req.get("min_words", 0),
                    "max_words": req.get("max_words", 0)
                }
                gen_out = {
                    "monologue_text": res["response_body"].get("generated_text", "")
                }
            
            worksheet_items.append({
                "item_id": item_id,
                "feature": feature,
                "input_context": input_ctx,
                "generated_output": gen_out,
                "rubric": {
                    "criteria": item_criteria,
                    "failure_conditions": fc,
                    "scoring": scoring_dict
                }
            })
            
    # Build Worksheet JSON payload
    worksheet_payload = {
        "worksheet_metadata": {
            "title": "Dostoevsky AI Blinded Human Evaluation Worksheet",
            "version": "3.0.0",
            "source_run_id": run_id,
            "evaluation_suite_version": spec_data.get("suite_version", "2.1.0"),
            "total_items": len(worksheet_items),
            "scoring_scale": rubric_defs["scoring_scale"],
            "instructions": (
                "Rate each item on a 1-5 scale across its three feature criteria using the rubric definitions, "
                "case-specific guidance, and failure conditions. "
                "Provide concrete evidence notes for extreme scores (1, 2, or 5). "
                "Do not penalize word-count variance under literary criteria, as length compliance is already objectively verified."
            )
        },
        "items": worksheet_items
    }
    
    out_dir = repo_root / "evaluation" / "endpoint_results"
    worksheet_json_path = out_dir / "blinded_human_evaluation_worksheet_run_20261025T180347Z_v3.json"
    worksheet_md_path = out_dir / "blinded_human_evaluation_worksheet_run_20261025T180347Z_v3.md"
    key_json_path = out_dir / "blinded_human_evaluation_key_run_20261025T180347Z.json"
    
    # Write JSON worksheet v3 (preserves v1, v2, and key untouched)
    with open(worksheet_json_path, "w", encoding="utf-8") as f:
        json.dump(worksheet_payload, f, indent=2, ensure_ascii=False)
        
    # Write Markdown worksheet v3
    with open(worksheet_md_path, "w", encoding="utf-8") as f:
        f.write("# Dostoevsky AI — Blinded Human Evaluation Worksheet (v3)\n\n")
        f.write(f"**Source Run ID:** `{run_id}`  \n")
        f.write(f"**Suite Version:** `{spec_data.get('suite_version')}`  \n")
        f.write(f"**Total Blinded Items:** 30 (10 Literary Rewrite, 10 Word Cabinet, 10 Inner Monologue)\n\n")
        f.write("## 1. Global Scoring Scale (1–5)\n\n")
        for sc, desc in rubric_defs["scoring_scale"].items():
            f.write(f"- **{sc}:** {desc}\n")
        f.write("\n## 2. Rater Instructions\n\n")
        f.write(f"{worksheet_payload['worksheet_metadata']['instructions']}\n\n")
        f.write("---\n\n")
        
        current_feat = None
        for item in worksheet_items:
            feat = item["feature"]
            if feat != current_feat:
                current_feat = feat
                feat_title = feat.replace("_", " ").title()
                f.write(f"\n# Feature: {feat_title}\n\n")
                
            f.write(f"## Item: `{item['item_id']}`\n\n")
            
            # Input Context
            f.write("### Input Context\n\n")
            if feat == "literary_rewrite":
                f.write(f"- **Original Text to Rewrite:**\n> {item['input_context']['text']}\n\n")
            elif feat == "word_cabinet":
                f.write(f"- **Requested Vocabulary Count:** {item['input_context']['count']}\n")
                f.write(f"- **Psychological Context:**\n> {item['input_context']['context']}\n\n")
            elif feat == "inner_monologue":
                f.write(f"- **Requested Perspective:** `{item['input_context']['perspective']}`\n")
                f.write(f"- **Target Word Length Window:** {item['input_context']['min_words']}–{item['input_context']['max_words']} words\n")
                f.write(f"- **Scenario:**\n> {item['input_context']['scenario']}\n\n")
                
            # Generated Output
            f.write("### Model Generated Output\n\n")
            if feat == "literary_rewrite":
                f.write(f"> {item['generated_output']['rewritten_text']}\n\n")
            elif feat == "word_cabinet":
                f.write("| # | Word | Part of Speech | Definition | Connotation | Intensity | Distinction | Example |\n")
                f.write("| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
                for w_idx, w in enumerate(item["generated_output"]["words"], 1):
                    f.write(f"| {w_idx} | **{w['word']}** | *{w['part_of_speech']}* | {w['definition']} | {w['connotation']} | `{w['intensity']}` | {w['distinction']} | *\"{w['example']}\"* |\n")
                f.write("\n")
                for w_idx, w in enumerate(item["generated_output"]["words"], 1):
                    f.write(f"**Entry {w_idx}: {w['word']}** (*{w['part_of_speech']}*, intensity: `{w['intensity']}`)\n")
                    f.write(f"- *Definition:* {w['definition']}\n")
                    f.write(f"- *Connotation:* {w['connotation']}\n")
                    f.write(f"- *Distinction:* {w['distinction']}\n")
                    f.write(f"- *Example:* *\"{w['example']}\"*\n\n")
            elif feat == "inner_monologue":
                f.write(f"> {item['generated_output']['monologue_text']}\n\n")
                
            # Rubric & Guidance
            f.write("### Rubric & Guidance\n\n")
            for c in item["rubric"]["criteria"]:
                f.write(f"- **`{c['criterion_id']}` ({c['name']}):** {c['description']}\n")
                if c["guidance"]:
                    f.write(f"  - *Specific Guidance:* {c['guidance']}\n")
            f.write("\n")
            
            # Failure Conditions
            if item["rubric"]["failure_conditions"]:
                f.write("### Specific Failure Conditions\n\n")
                for fc in item["rubric"]["failure_conditions"]:
                    f.write(f"- ⚠️ {fc}\n")
                f.write("\n")
                
            # Scoring Form
            f.write("### Scoring & Evidence Form\n\n")
            f.write("| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |\n")
            f.write("| :--- | :--- | :---: | :--- |\n")
            for c in item["rubric"]["criteria"]:
                f.write(f"| `{c['criterion_id']}` | {c['name']} | `[ ]` | |\n")
            f.write("\n")
            f.write("**Rater ID:** `[               ]`  \n")
            f.write("**Evaluation Date (UTC):** `[               ]`\n\n")
            f.write("---\n\n")
            
    print("Files created successfully:")
    print("  Worksheet JSON v3:", worksheet_json_path)
    print("  Worksheet MD v3:  ", worksheet_md_path)
    print("  Key JSON:         ", key_json_path, "(preserved untouched)")

if __name__ == "__main__":
    generate_blinded_evaluation()
