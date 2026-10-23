

# Dostoevsky AI â€” Project Log



## 1. Project Overview



**Project:** Dostoevsky AI â€” A Literary Writing and Vocabulary Assistant



**Objective:** Build and evaluate a locally runnable literary assistant inspired by the psychological and philosophical depth of Fyodor Dostoevsky's literature.



**Approach:** Establish a prompting baseline, prepare a documented literary corpus, investigate parameter-efficient fine-tuning, and evaluate the resulting system honestly.



## 2. Three-Phase Plan



\- \[x] Phase 1: Environment setup and baseline LLM

\- \[ ] Phase 2: Literary corpus and fine-tuning

\- \[ ] Phase 3: Deployment, evaluation, and finalization



Phase 1 is in progress. The initial model and prompting experiments have been verified, but the project structure and log still need to be completed.



## 3. Environment Information



\- Operating system: Windows 11 Home Single Language

\- CPU: Intel Core i5-12450H, 8 cores, 12 logical processors

\- Installed RAM: 15.73 GB

\- Reported graphics: Intel UHD Graphics, reported adapter memory 2 GB

\- NVIDIA utility: `nvidia-smi` was not recognized

\- Free storage at initial inspection: C: 43.62 GB; D: 331.91 GB

\- Ollama version: 0.40.9



Hardware details are based on PowerShell output supplied during the project. The reported graphics memory has not been independently validated.



## 4. Verified Models



### Base Model



\- Model: `qwen2.5:3b`

\- Reported Ollama size: 1.9 GB

\- Verification: Successfully downloaded and ran a literary generation prompt.



### Configured Baseline



\- Model: `dostoevsky-baseline:latest`

\- Reported Ollama size: 1.9 GB

\- Configuration file: `Modelfile`

\- Base model: `qwen2.5:3b`

\- Context parameter: 4096

\- Temperature: 0.85

\- Top-p: 0.9

\- Repeat penalty: 1.1

\- Maximum generated tokens: 512



The configured baseline uses a system prompt and generation parameters. It has not been fine-tuned, and its neural network weights have not been retrained.



## 5. Baseline Evaluation



### Test 1 â€” Literary Rewrite



**Prompt:** Rewrite a sentence about helping a friend while secretly feeling resentment.



**Observed result:** The model produced concise prose that preserved the central contradiction.



**Limitation:** The imagery was familiar rather than particularly distinctive.



### Test 2 â€” Word Cabinet



**Prompt:** Suggest three precise words for shame about one's own good intentions, with definitions, distinctions, and examples.



**Observed result:** The model provided three words with definitions and example sentences.



**Limitation:** "Discomfort" was too broad for the requested emotional precision. Some distinctions were also oversimplified.



### Test 3 â€” Psychological Monologue



**Prompt:** Write an internal monologue about a man who tells the truth to protect his reputation and questions his honesty.



**Observed result:** The model explored reputation, self-deception, and moral uncertainty.



**Limitation:** The monologue described the man's statement as both a lie and the truth, creating an inconsistency with the premise.



### Initial Conclusion



The baseline can generate coherent literary prose, but task adherence, vocabulary precision, and narrative consistency require further evaluation.



These are qualitative observations from three manually executed tests, not a formal benchmark.



## 6. Current Progress



\- \[x] Inspect basic system hardware and storage

\- \[x] Install and verify Ollama

\- \[x] Download and run `qwen2.5:3b`

\- \[x] Create the baseline Modelfile

\- \[x] Create `dostoevsky-baseline:latest`

\- \[x] Execute three baseline evaluation prompts

\- \[ ] Create the project directories

\- \[ ] Save this project log

\- \[ ] Begin Phase 2 after confirming the Phase 1 checkpoint



## 7. Pending Work



1\. Confirm the project structure and log are saved.

2\. Learn the differences between prompting, continued pretraining, supervised fine-tuning, and retrieval-augmented generation.

3\. Select a suitable training objective.

4\. Identify a legally usable literary corpus and document its provenance.

5\. Assess whether cloud GPU training is needed.

6\. Prepare, train, deploy, and evaluate only to the extent supported by actual results.



## 8. Progress Entry Template

### 2026-10-23 â€” Phase 1 Completion

- **Action completed:** Installed and verified Ollama, downloaded Qwen2.5 3B, created the `dostoevsky-baseline` Modelfile, tested three literary tasks, created project directories, and initialized the project log.
- **Commands or configuration:** `ollama --version`, `ollama list`, `ollama create dostoevsky-baseline -f .\Modelfile`, and `ollama run dostoevsky-baseline`.
- **Learning outcome:** Established a local inference baseline and identified initial weaknesses in vocabulary precision, instruction following, and narrative consistency.
- **Files or artifacts produced:** `Modelfile`, `PROJECT_LOG.md`, `data/raw/`, `data/processed/`, `evaluation/`, and `notes/`.
- **Verification and actual outcome:** Ollama version 0.40.9 was reported; both `qwen2.5:3b` and `dostoevsky-baseline:latest` appeared in the model list. Three baseline prompts were executed. Project directory creation and Markdown heading display were verified.
- **Errors and resolutions:** Markdown escape characters in the initial log were corrected. UTF-8 heading display was subsequently verified.
- **Next pending step:** Begin Phase 2 by selecting and documenting the training objective before sourcing the literary corpus.



### \[Date] â€” \[Phase and Step]



\- **Action completed:**

\- **Commands or configuration:**

\- **Learning outcome:**

\- **Files or artifacts produced:**

\- **Verification and actual outcome:**

\- **Errors and resolutions:**

\- **Next pending step:**



Record only actions actually performed and results actually observed.



## Phase 2 â€” Corpus Cleaning and Initial Validation

Status: Cleaning script implemented; initial structural validation passed.

### Actions completed
- Extracted literary text between Project Gutenberg markers.
- Removed the contents listing from both cleaned books.
- Preserved the translator's preface in Crime and Punishment.
- Verified selected headings: Part I, Part II, Chapter I, Chapter II, and Epilogue.
- Removed publisher material after the final story in White Nights and Other Stories.
- Normalized whitespace and paragraph boundaries.
- Generated data/processed/corpus_report.json.
- Confirmed zero remaining Gutenberg markers and zero Unicode replacement characters in the checked Crime and Punishment output.
- Confirmed both processed text files are excluded from Git.

### Verification limitations
- Selected headings and ending boundaries were checked; complete chapter-by-chapter integrity has not yet been verified.
- The UTF-8 apostrophe was verified through Python decoding; the unusual terminal rendering is not evidence of file corruption.
- Raw and processed literary texts remain excluded from Git.

### Next pending step
- Review the project log and Git staging area.
- Commit and push the corpus-cleaning script and project log.
- Continue corpus integrity checks before preparing the evaluation dataset.

