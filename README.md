# Dostoevsky AI

**A literary writing and vocabulary assistant inspired by Fyodor Dostoevsky's psychological and philosophical themes.**

Dostoevsky AI is an experimental local language-model project focused on psychologically nuanced writing, precise vocabulary, and introspective character monologues.

## Core Features

- **Literary Rewrite:** Transform ordinary writing into introspective, psychologically complex prose.
- **Word Cabinet:** Explore precise words for nuanced emotional states, including definitions, connotations, and usage examples.
- **Inner Monologue:** Generate original monologues involving conflicting motives, moral tension, and self-questioning.

## Current Status

**Phase 1 — Baseline established**

- Configured a local Qwen2.5 3B model using Ollama.
- Created the `dostoevsky-baseline` model with a custom system prompt.
- Established initial qualitative baseline tests.
- Identified initial weaknesses in vocabulary precision and consistency.
- Downloaded two Project Gutenberg texts for planned corpus preparation.

The model is currently **prompt-configured, not fine-tuned**. Fine-tuning and systematic evaluation are planned next.

## Technology

- Python
- Ollama
- Qwen2.5 3B
- Git and GitHub

Additional training and evaluation tools will be documented as the project develops.

## Project Structure

```text
fyodor/
├── Modelfile
├── PROJECT_LOG.md
├── README.md
├── .gitignore
├── data/
│   ├── raw/          # Local source texts; excluded from Git
│   └── processed/    # Prepared corpus; excluded from Git
├── scripts/
│   └── inspect_corpus.py
├── evaluation/
└── notes/
```

## Development Roadmap

1. Establish and evaluate a prompt-configured baseline.
2. Inspect, clean, and prepare the literary corpus.
3. Develop a training dataset and investigate parameter-efficient fine-tuning.
4. Compare the adapted model with the baseline.
5. Document results, limitations, and reproducible setup instructions.

## Reproducibility

The project is developed and tested on Windows with Ollama. Commands, configuration, evaluation results, and major decisions will be documented as development progresses.

The downloaded literary texts are kept locally and are not included in this repository by default. Consult each source's licensing and distribution terms before redistributing source texts or derived materials.

## Disclaimer

This is an experimental literary assistant, not an official representation of Fyodor Dostoevsky or a claim that a language model can reproduce his writing exactly.
