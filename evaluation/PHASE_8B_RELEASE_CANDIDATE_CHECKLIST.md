# PHASE 8B: RELEASE CANDIDATE PACKAGING & DEMONSTRATION CHECKLIST

**Project:** Dostoevsky AI  
**Design System:** The Underground Study  
**Release Target:** Controlled Local Release Candidate (`v0.1.0-rc1`)  
**Target Serving Model:** `dostoevsky-baseline:latest` (Base: `qwen2.5:3b`, `Q4_K_M`)  
**Auditor Roles:** Principal Software Engineer & Release Manager  
**Date:** 2026-10-31  

---

## 1. RELEASE PACKAGING OVERVIEW

This checklist governs the packaging, verification, demonstration, and distribution readiness of **Dostoevsky AI** as a local-first release candidate and AI/ML portfolio project.

> [!IMPORTANT]
> **Controlled Scope Policy:** Dostoevsky AI is strictly engineered and validated for local-first desktop single-user execution. It is **not** authorized or architected for multi-tenant public cloud deployment. No public network hosting should be attempted without authentication, rate limiting, and sandboxed inference infrastructure.

---

## 2. PRE-RELEASE REPRODUCIBILITY CHECKLIST

### 2.1 System Environment Prerequisites
- [x] **Python:** Python 3.11+ (verified on Python 3.13.5 win32).
- [x] **Node.js:** Node.js 18+ (verified on Node.js v20+).
- [x] **npm:** npm 9+ (lockfile `frontend/package-lock.json` synchronized).
- [x] **Inference Engine:** Ollama running locally at `http://localhost:11434`.
- [x] **Base Model Weights:** `qwen2.5:3b` pulled via `ollama pull qwen2.5:3b`.
- [x] **Serving Model:** `dostoevsky-baseline:latest` built from root `Modelfile` via `ollama create dostoevsky-baseline -f ./Modelfile`.

### 2.2 Configuration & Secrets
- [x] **`.env.example`:** Verified present and documented with sensible local defaults.
- [x] **Secret Audit:** Verified zero API keys, tokens, or credentials in codebase.
- [x] **CORS Origins:** Verified backend Starlette middleware authorizes `http://localhost:5173` and `http://127.0.0.1:5173`.
- [x] **Network Binding:** Verified servers bind to `127.0.0.1` / `localhost` only.
- [x] **Data Privacy:** Verified zero logging of user input or generated text to stdout, logs, or disk.

### 2.3 Intellectual Property & Corpus Safety
- [x] **License Status:** The repository currently has no open-source `LICENSE` file. All rights reserved by project maintainers. Evaluators may clone and inspect locally for demonstration purposes only.
- [x] **Corpus Distribution Safety:** Raw and processed literary texts (Project Gutenberg downloads in `data/raw/` and `data/processed/`) are strictly excluded via `.gitignore`. No copyrighted or third-party texts are committed or packaged.
- [x] **Evaluation Integrity:** Historical evaluation artifacts in `evaluation/` remain read-only and preserved.

---

## 3. AUTOMATED VERIFICATION GATES

All verification gates must pass cleanly prior to release sign-off:

| Suite | Command | Verification Evidence | Status |
|---|---|---|:---:|
| **Backend Unit & API Tests** | `python -m pytest backend/tests` | 82 / 82 tests passing (Pytest 8.4.2) | **PASS** |
| **Frontend Unit & UI Tests** | `npm test --prefix frontend` | 55 / 55 tests passing across 6 suites (Vitest 5.0.5) | **PASS** |
| **TypeScript Typecheck** | `tsc --noEmit -p frontend/tsconfig.app.json` | 0 type errors | **PASS** |
| **Frontend Production Build**| `npm run build --prefix frontend` | 0 errors, gzip 53.5 kB JS, build time < 500ms | **PASS** |

---

## 4. FUNCTIONAL CAPABILITY MATRIX

| Feature / Studio | Expected Behavior | Release Verification |
|---|---|:---:|
| **Studio 01: Literary Rewrite** | Accepts up to 5,000 chars; returns psychologically layered prose preserving narrative core. | **VERIFIED** |
| **Studio 02: Word Cabinet** | Accepts context (up to 2,000 chars) and count (3-8); returns structured JSON vocabulary cards with intensity, distinction, and examples. | **VERIFIED** |
| **Studio 03: Inner Monologue** | Accepts situation and word range (50-500); generates conflicting interior voice; transparently warns if length shortfalls occur. | **VERIFIED** |
| **Health State Indicator** | Accurately distinguishes between Backend Offline, Model Offline, and Ready states. | **VERIFIED** |
| **Empty Result Recovery** | Gracefully handles empty or filtered vocabulary without raising 502 server errors. | **VERIFIED** |
| **Error Resilience** | Controlled HTTP 422 for input boundaries; HTTP 503 on Ollama downtime; HTTP 504 on timeout. | **VERIFIED** |
| **DOM State Retention** | Preserves drafts and generated output across studio switching with zero re-fetching. | **VERIFIED** |
| **URL Hash Routing** | Synchronizes `#rewrite`, `#word-cabinet`, `#inner-monologue` with browser history and direct linking. | **VERIFIED** |

---

## 5. FIVE-MINUTE PORTFOLIO DEMO SEQUENCE

Use this structured script for live portfolio demonstrations, technical interviews, and stakeholder walkthroughs:

### Minute 1: Introduction & Architecture Overview (60s)
1. **The Hook:** Introduce *Dostoevsky AI* as a local-first literary assistant exploring human contradiction, moral ambivalence, and psychological interiority inspired by Dostoevsky.
2. **Architecture:** Explain the local-first stack: React 18 frontend with custom "Underground Study" dark academia design system, FastAPI backend with strict Pydantic contract validation, and local Ollama running a quantized 3B LLM (`qwen2.5:3b`).
3. **Privacy:** Emphasize that all processing occurs in local RAM; zero telemetry, zero cloud API fees, and zero data leakage.

### Minute 2: Studio 01 — Literary Rewrite (60s)
1. Navigate to `#rewrite` (Literary Rewrite).
2. Input a flat emotional sentence:  
   *`"I knew I had acted rightly, yet I avoided meeting her eyes."`*
3. Click **"Rewrite"**. Note the restrained UI feedback and loading indicator.
4. Review the generated prose: highlight how the model introduced psychological hesitation and interior subtext without violating the factual core.
5. Demonstrate the one-click clipboard copy action.

### Minute 3: Studio 02 — Word Cabinet (60s)
1. Switch to `#word-cabinet` (note: Literary Rewrite draft is completely preserved in background).
2. Enter a conflicted scenario:  
   *`"I feel grateful for the opportunity, but resentful that I was overlooked until someone else declined."`*
3. Point out the subtle latency guidance: *"Fewer suggestions can reduce generation time on local hardware. Try four entries for a quicker vocabulary session."* Select 4 words.
4. Review the structured vocabulary cards: demonstrate the distinction field ("Unlike envy, it involves..."), intensity meter (1-5), and contextual example.

### Minute 4: Studio 03 — Inner Monologue & Model Realism (60s)
1. Switch to `#inner-monologue` (demonstrate cross-studio state retention).
2. Enter scenario:  
   *`"After a cruel argument, I want to apologize to my sister, but I keep remembering the things she said years ago."`*
3. Point out the word-count guidance (suggested 100–180 words for local 3B model). Set range to 100–180 words.
4. Execute generation. Show the generated interior monologue and explain the word-count validator and warning mechanism.

### Minute 5: AI/ML Engineering Rigor & Scientific Integrity (60s)
1. **The Falsification Story:** Explain that the most important engineering achievement was NOT blind prompt iteration, but the **pre-registered double-blind human evaluation** (EXP-WC-02).
2. **Methodology:** Describe how 20 blinded items were evaluated across 2 independent human raters using a frozen rubric and Cohen's kappa.
3. **Honest Falsification:** When human scoring disproved the hypothesis (delta -0.20 on distinction usefulness), the team resisted confirmation bias, adhered to pre-registered rules, rejected the change, and restored the cryptographically verified baseline prompt (`be472f536fbb27ed...`).
4. **Conclusion:** Conclude on why empirical rigor matters more in production AI than unverified marketing claims.

---

## 6. BACKUP OFFLINE DEMONSTRATION PLAN

If Ollama is slow, offline, or experiencing hardware constraints during a live presentation:

1. **Phase 7C Artifact Showcase:** Open `evaluation/phase_7c_live_e2e/` and review real captured JSON payloads:
   - `02_lr_live_01_result.json`: Live 42-word rewrite in 18.66s.
   - `03_wc_live_01_result.json`: Live 6-entry structured vocabulary generation in 76.22s.
   - `04_im_live_01_result.json`: Live 147-word inner monologue in 24.96s with transparent warning metadata.
2. **Double-Blind Evaluation Worksheet:** Open `evaluation/experiments/exp_wc_02_distinction_structure/blinded_evaluation_worksheet_20_items.md` to demonstrate the rater blinding procedure and rubric structure.
3. **Automated Test Execution:** Run `npm test --prefix frontend` (55 tests in ~11s) and `pytest backend/tests` (82 tests in ~13s) to demonstrate full-stack test suite reliability live.

---

## 7. RELEASE TAG PREPARATION CHECKLIST

> [!CAUTION]
> **MAINTAINER ACTION ONLY:** Do not execute Git commits, pushes, or tag creation automatically. This checklist is for the project lead to execute when authorizing the release candidate.

### Pre-Tag Verifications
- [ ] Confirm working directory is clean (`git status --short` shows no unintended modifications).
- [ ] Confirm `.gitignore` preserves local environments (`.venv`, `node_modules`, `data/`).
- [ ] Confirm all 82 backend tests and 55 frontend tests pass.
- [ ] Confirm TypeScript compilation passes with zero errors.
- [ ] Confirm production frontend build succeeds.
- [ ] Confirm `evaluation/PHASE_8B_FINAL_IMPLEMENTATION_REPORT.md` is present and verified.

### Suggested Release Tag Command (For Project Lead)
```powershell
# Review final status
git status

# Create annotated release candidate tag
git tag -a v0.1.0-rc1 -m "Release Candidate 1: Dostoevsky AI Local-First Assistant"
```
