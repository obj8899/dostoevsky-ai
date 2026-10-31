# PHASE 7B, BATCH 1 IMPLEMENTATION REPORT
## Core Reliability Fixes (7B.1 + 7B.2 + 7B.3)

**Project:** Dostoevsky AI  
**Design System:** The Underground Study  
**Execution Date:** 2026-10-30 18:02:23 UTC  
**Governing Document:** Phase 7A Frontend & Integration Audit  
**Status:** COMPLETE & VERIFIED — READY FOR DECISION

---

## 1. EXECUTIVE SUMMARY

Phase 7B Batch 1 addressed three high-priority reliability vulnerabilities identified during the Phase 7A Integration Audit:

1. **Task 7B.1 (FINDING-7A-01, P1):** Corrected frontend health-state reporting. The frontend previously misreported `status: "degraded"` (e.g., Ollama disconnected or model unavailable) as fully connected because the backend HTTP status was 200. The frontend now strictly evaluates backend and Ollama connectivity, cleanly distinguishing between `connected`, `degraded`, `unavailable`, and `malformed` states.
2. **Task 7B.2 (FINDING-7A-02, P1):** Corrected local development CORS origins in `backend/src/dostoevsky_ai/config.py`. The backend now explicitly authorizes both `http://localhost:5173` and `http://127.0.0.1:5173` without requiring environment variable overrides.
3. **Task 7B.3 (FINDING-7A-04, P2):** Corrected Word Cabinet empty-response handling in `frontend/src/api/client.ts`. The schema validator previously required `words.length > 0`, causing valid empty vocabulary returns (`words: []`) to throw an `ApiError`. It now accepts empty lists, allowing `WordCabinet.tsx`'s built-in graceful empty-state fallback to render.

### Implementation Scope & Boundaries
- **Strictly Limited:** All edits were restricted to the 7 files required for Tasks 7B.1, 7B.2, and 7B.3.
- **Batch 2 Deferred:** Tasks 7B.4 (draft preservation), 7B.5 (testing library expansion), and 7B.6 (URL hash routing) were NOT implemented.
- **Phase 7C Preserved:** Zero live model inference requests were sent to Ollama during this checkpoint.
- **Verification Summary:**
  - Frontend Vitest Unit Tests: **17 passed, 0 failed** (100% passing).
  - Backend Pytest Unit Tests: **78 passed, 0 failed** (100% passing).
  - TypeScript Compiler Check (`tsc --noEmit`): **0 errors**.

---

## 2. REPOSITORY STATE VERIFICATION

- **Current Git Branch:** `main`
- **Git Head Status:** Branch is up to date with `origin/main`.
- **Preserved Existing Modifications:**
  - `.gitignore` (preserved unchanged)
  - `README.md` (preserved unchanged)
- **Git Working Tree:** No staging or commits were executed. All changes remain in the local working tree.
- **Untracked Experiment Artifacts:** Preserved all historical evaluation logs, worksheets, and model files intact.

---

## 3. TASK 7B.1 DETAILED REPORT: HEALTH-STATE REPORTING

### Problem Statement (FINDING-7A-01)
When the FastAPI backend is running but Ollama is offline or the target model is unpulled, the `/api/health` endpoint returns HTTP 200 with JSON payload indicating degraded state: `{"status": "degraded", "ollama": {"status": "unavailable", ...}}`. In the original frontend implementation, `App.tsx` and `client.ts` checked only whether `fetchHealth()` resolved without throwing. Consequently, the UI topbar displayed an ink-green dot labeled `"Ollama connected"`, misleading users into believing the system was ready for inference when any feature request would immediately fail with a 503 error.

### Files Modified & Changes Made
1. `frontend/src/api/client.ts`:
   - Defined and exported `ConnectionState`: `"checking" | "connected" | "degraded" | "unavailable" | "malformed"`.
   - Exported pure evaluation function `evaluateHealthStatus(health: HealthResponse): "connected" | "degraded"`. It asserts that both `health.status === "ok"` AND `health.ollama.status === "connected"` AND `health.ollama.model_available === true`. Any deviation evaluates strictly to `"degraded"`.
2. `frontend/src/App.tsx`:
   - Updated `checkBackend` callback to use `evaluateHealthStatus(health)`.
   - Structured error handling to distinguish between malformed response schema (`setConnection("malformed")`) and network/transport failures (`setConnection("unavailable")`).
3. `frontend/src/components/AppShell.tsx`:
   - Updated `connectionCopy` mapping to define human-readable descriptions for all connection states:
     - `connected`: `"Ollama connected"`
     - `degraded`: `"Ollama unavailable"`
     - `unavailable`: `"Backend offline"`
     - `malformed`: `"Health check failed"`
     - `checking`: `"Checking connection…"`
   - Updated the topbar retry button visibility condition from `connection === "unavailable"` to `connection !== "connected" && connection !== "checking"`. This ensures users can retry the connection when in degraded or malformed states.
4. `frontend/src/styles/global.css`:
   - Added amber dot styling for `.connection-status--degraded::before` (`background: var(--warning)` / `#c98a2c`).
   - Added crimson dot styling for `.connection-status--malformed::before` (`background: var(--error)` / `#9e2a2b`).
5. `frontend/src/api/client.test.ts`:
   - Added 5 comprehensive test cases covering healthy states, degraded states, non-200 HTTP responses, schema parsing rejections, and combinations of degraded subfields.

### Frontend Behavior Comparison
| State / Scenario | Before Fix | After Fix |
|---|---|---|
| Backend running, Ollama running, model ready | Green dot, `"Ollama connected"` | Green dot, `"Ollama connected"` |
| Backend running, Ollama disconnected | **Green dot, `"Ollama connected"` (False Positive)** | **Amber dot, `"Ollama unavailable"`, Retry button displayed** |
| Backend running, model unpulled | **Green dot, `"Ollama connected"` (False Positive)** | **Amber dot, `"Ollama unavailable"`, Retry button displayed** |
| Backend returns malformed JSON / non-schema | Crimson dot, `"Backend offline"` | **Crimson dot, `"Health check failed"`, Retry button displayed** |
| Backend process completely offline | Crimson dot, `"Backend offline"` | Crimson dot, `"Backend offline"`, Retry button displayed |

---

## 4. TASK 7B.2 DETAILED REPORT: LOCAL DEVELOPMENT CORS ORIGINS

### Problem Statement (FINDING-7A-02)
Vite dev server binds by default to both `localhost` and `127.0.0.1`. Developers navigating to `http://127.0.0.1:5173` had all feature and health requests blocked by Starlette's `CORSMiddleware` because `Settings.cors_origins` defaulted strictly to `"http://localhost:5173"`.

### Configuration Changes Made
- Modified `backend/src/dostoevsky_ai/config.py`:
  - Updated default value of `cors_origins`:
    - Before: `cors_origins: str = "http://localhost:5173"`
    - After: `cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"`
  - `Settings.allowed_origins` dynamically parses `self.cors_origins.split(",")`, cleanly providing `["http://localhost:5173", "http://127.0.0.1:5173"]` to FastAPI's `CORSMiddleware`.

### Test Results
Added 4 comprehensive CORS unit tests to `backend/tests/test_health.py`:
1. `test_cors_allows_localhost_origin`: Verifies `Origin: http://localhost:5173` returns `access-control-allow-origin: http://localhost:5173`.
2. `test_cors_allows_127_0_0_1_origin`: Verifies `Origin: http://127.0.0.1:5173` returns `access-control-allow-origin: http://127.0.0.1:5173`.
3. `test_cors_rejects_unapproved_origin`: Verifies `Origin: http://malicious-site.com` does NOT receive allow-origin headers.
4. `test_cors_preflight_options_for_features`: Verifies preflight HTTP `OPTIONS` requests against `/api/features/word-cabinet` return 200 with appropriate CORS headers.

---

## 5. TASK 7B.3 DETAILED REPORT: WORD CABINET EMPTY-RESPONSE HANDLING

### Problem Statement (FINDING-7A-04)
The backend Pydantic schema for Word Cabinet (`WordCabinetResponse`) specifies `words: list[WordCabinetEntry] = Field(default_factory=list)`. An empty vocabulary list `[]` is a valid, allowable contract response (e.g. if the context yielded no suitable vocabulary or all suggestions failed validation). However, `isWordCabinetResponse` in `frontend/src/api/client.ts` contained an overly aggressive check: `value.words.length > 0 &&`. This caused any empty response to fail schema validation and throw an `ApiError("invalid response schema")`. `WordCabinet.tsx` already had an intentional empty-state UI (`"No usable vocabulary entries were returned. Try refining the context and request again."`), but this UI was unreachable because the client rejected the payload before the component could render it.

### Validation Logic Changes
- In `frontend/src/api/client.ts`:
  - Removed `value.words.length > 0 &&` from `isWordCabinetResponse`.
  - Allowed empty words array while preserving `Array.isArray(value.words) && value.words.every(isWordCabinetEntry)`.
- All other validations remain strictly intact:
  - `context` must be a non-empty string.
  - `model` must be a non-empty string.
  - `validation_warnings` must be an array of strings.
  - Every entry present in `words` must satisfy `isWordCabinetEntry` (word, part of speech enum, definition, connotation, intensity 1-5 integer, distinction, example).

### Test Results
Added 5 focused unit tests in `frontend/src/api/client.test.ts`:
- `accepts a valid empty Word Cabinet response (words: [])` — PASSED.
- `rejects a Word Cabinet response when words property is missing` — PASSED.
- `rejects a Word Cabinet response when words property is not an array` — PASSED.
- `rejects a Word Cabinet response when an entry has intensity out of range` — PASSED.
- `rejects a Word Cabinet response when an entry has an invalid part of speech` — PASSED.

---

## 6. COMBINED VERIFICATION RESULTS

| Test Suite / Tool | Command Executed | Tests Passed | Tests Failed | Total Duration | Status |
|---|---|:---:|:---:|:---:|:---:|
| Frontend Unit Tests (Vitest) | `npm test --prefix frontend` | 17 | 0 | 560 ms | **PASS** |
| TypeScript Compiler Check | `node frontend/node_modules/typescript/bin/tsc --noEmit -p frontend/tsconfig.app.json` | N/A | 0 errors | 2.1 s | **PASS** |
| Backend Health & CORS Tests | `pytest backend/tests/test_health.py` | 6 | 0 | 18.94 s | **PASS** |
| Full Backend Test Suite | `pytest backend/tests` | 78 | 0 | 38.19 s | **PASS** |

**Regression Summary:** Zero regressions across all 78 backend tests and all 17 frontend tests.

---

## 7. MODIFIED FILES MANIFEST

| File Path | Purpose of Modification | Lines Before | Lines After | Line Diff | Raw SHA-256 | Normalized LF SHA-256 |
|---|---|:---:|:---:|:---:|---|---|
| `backend/src/dostoevsky_ai/config.py` | Allow both localhost and 127.0.0.1 origins for Vite dev server | 36 | 36 | 0 net (modified 1 line) | `99d1494165dc16ba5753763f78facb3f7d9e21e763b40b4751d60d714ddefaca` | `aa1b0812f0102aed8d5447ce9c3f0d51ee57cf0085fef8ced86c2b56134f99bf` |
| `backend/tests/test_health.py` | Add CORS origin and preflight verification tests | 46 | 119 | +73 lines | `ad7c76c09831fff8f246d0b3760adfc0f2ed57f1a95f1633db8820b0aa68c694` | `1417ce49d13334b77244d19beb6065405e95f626a68fae342e2131e5442803f3` |
| `frontend/src/api/client.ts` | Add ConnectionState, evaluateHealthStatus(), and allow empty words array | 372 | 426 | +54 lines | `3dbb7a01a6acd8dc8ea460ef5db08abb330adbc50feb245c99553eb6f84deb50` | `220f9b561474466fe137aa33356b486c17346c1ec7cdff7bdc838aec5141eae6` |
| `frontend/src/api/client.test.ts` | Unit tests for health status evaluation and Word Cabinet response validation | 169 | 339 | +170 lines | `0bb042f6cd9c8085d19d4d5883dd4814d78245c9e3deae1caae4ea15724db3d8` | `266e79cb8acc7c0b9c977f5cdc6b27d2e8982c3ce7d53e0ad6446144af67b04f` |
| `frontend/src/App.tsx` | Integrate evaluateHealthStatus and distinct connection states | 62 | 72 | +10 lines | `fa15394ecb9986cc6829064158a161c06d6be3b9dfcaad02913b5dc46cd25720` | `eea50fc73b294b51c030e2916a5cdaa02de26c47e092bc47ce3333c0d3899eff` |
| `frontend/src/components/AppShell.tsx` | ConnectionState status copy and retry display on non-connected states | 109 | 118 | +9 lines | `f32f36fe01d12d87bd07697987a2c9dbcff9d63f9c0203e7a2dfff5281d7a6f7` | `25b2f2652a54bb5f1f2b25ada093bc04efffee2cd2a98e10e71416acf0142cc6` |
| `frontend/src/styles/global.css` | Visual dot indicators for degraded (warning) and malformed (error) states | 1526 | 1538 | +12 lines | `794289705a107bcf485a2277ed5dff47e32653206f50ec98cdeb1851452916c0` | `42ce370a2dd43ac73611806d98546c27844991532362a2b5101a4d8ca855fc41` |

---

## 8. RISK ASSESSMENT

| Modification | Regressions Risk | Justification & Edge Cases Addressed | Rollback Procedure |
|---|:---:|---|---|
| **7B.1 Health Reporting** | **Low** | Purely additive. Preserves `HealthResponse` shape. Adds fallback to `"degraded"` if Ollama is unreachable. Handled edge cases: `model_available: null`, `model_available: false`, non-200 HTTP codes, malformed JSON. | Revert `client.ts`, `App.tsx`, `AppShell.tsx`, and `global.css` changes via Git. |
| **7B.2 CORS Origins** | **Low** | Strict superset of existing permissions. Permits `127.0.0.1:5173` alongside `localhost:5173`. Disallowed origins remain rejected. | Revert `backend/src/dostoevsky_ai/config.py` default string to `"http://localhost:5173"`. |
| **7B.3 Empty Words** | **Low** | Relaxes frontend array-length constraint to match backend contract. Preserves rigorous per-entry validation for any non-empty entries. Allows component to render its designed fallback. | Re-insert `value.words.length > 0 &&` in `client.ts`. |

---

## 9. DEFERRED FINDINGS STATUS

The following findings and tasks were intentionally deferred to Batch 2 or Phase 7C per the authorized batch protocol:

| Finding ID | Task ID | Description | Severity | Status | Next Milestone |
|---|---|---|:---:|:---:|:---:|
| FINDING-7A-03 | 7B.4 | Draft preservation on tab navigation | P2 | Deferred | Phase 7B, Batch 2 |
| FINDING-7A-05 | 7B.6 | URL hash routing for tab navigation | P3 | Deferred | Phase 7B, Batch 2 |
| FINDING-7A-06 | 7B.5 | Component testing library setup (@testing-library/react) | P3 | Deferred | Phase 7B, Batch 2 |
| Phase 7C Live | Phase 7C | Live model inference & edge-case testing against local Ollama | N/A | Preserved | Phase 7C |

**Confirmation:** No code modifications, dependencies, or routing configurations associated with Batch 2 tasks were introduced. No live model inference calls were dispatched.

---

## 10. PHASE 7C READINESS ASSESSMENT

With the completion and verification of Batch 1, the core reliability prerequisites for live model testing are fully satisfied:
1. **Accurate Health Visibility:** Developers and raters can now see immediately whether Ollama and the target model (`dostoevsky-baseline:latest`) are online before triggering requests.
2. **Flexible Local Connectivity:** Local development and testing are unblocked whether accessing the app via `localhost` or `127.0.0.1`.
3. **Robust Vocabulary Response Parsing:** Word Cabinet will no longer crash into an unhandled API error if an inference run yields zero vocabulary suggestions.

### Recommended Next Steps
- If UI state retention (draft preservation across tabs) is desired before running live tests, proceed to **Phase 7B, Batch 2**.
- If immediate verification of live inference with the corrected reliability fixes is preferred, proceed directly to **Phase 7C**.
