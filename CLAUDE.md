# rag-eval-framework — Claude Code Context

## Project Overview

A configurable RAG evaluation framework that quantifies how different chunking strategies, embedding models, and retrieval methods affect answer quality, faithfulness, and cost. The reference corpus is UK FCA regulatory text; the eval harness is domain-agnostic.

**Issue Tracking:** Linear — project "AI and Machine Learning", team "James", parent issue JAM-237

---

## Rules

These are non-negotiable. They apply to every session regardless of scope.

- **Never commit directly to main.** Always create a feature or fix branch and open a PR.
- **Before pushing, verify only intended files are staged.** Run `git status` and `git diff --cached --name-only` before every commit.
- **Run lint + tests locally before opening a PR.**
- **No secrets in code.** AWS credentials, API keys, and bucket names come from environment variables or `.env`. Never hardcode them.
- **No manual steps.** Everything is scripted — scraping, uploading, ingestion, eval runs. If it can't be reproduced by running a command, it's not done.
- **This is a public repo.** No references to personal job applications, hiring targets, or company-specific objectives in any committed content (code, docs, comments, commit messages).
- **Coach, don't generate.** James writes all code. Claude explains, guides, and reviews. Do not generate implementation code unprompted — discuss the approach first, then guide James through writing it.

---

## Architecture

```
FCA Handbook REST API (api-handbook.fca.org.uk)
  → scripts/scrape_fca.py → data/fca/ (JSONL)
  → S3 upload

Synthetic policy documents (Claude-generated)
  → scripts/generate_policies.py → data/synthetic/ (markdown + metadata)
  → S3 upload

Ingestion pipeline (scripts/ingest.py)
  → src/chunking/ (fixed-size | structure-aware)
  → src/embeddings/ (Titan V2 | Cohere Embed v3 via Bedrock)
  → src/vectorstore/ (S3 Vectors — 4 indexes)
  → BM25 pickle indexes → S3

Ground-truth Q&A (scripts/generate_qa.py)
  → data/qa/qa_pairs.json

Retrieval + generation (src/retrieval/ + src/generation/)
  → query_pipeline() — config-driven, any combination

Evaluation (src/eval/)
  → run_eval.py — 8 configs, dual LLM judges
  → results/ (per-question JSON, aggregate CSV, comparison table markdown)
```

## Key Technology Choices

- **Language:** Python 3.12
- **Package manager:** uv
- **Cloud:** AWS (eu-west-1)
- **Vector store:** S3 Vectors (serverless)
- **Embedding models:** Amazon Titan Text Embeddings V2, Cohere Embed English v3 (both via Bedrock)
- **Generation model:** Claude Sonnet 4.6 via Bedrock
- **Judge models:** Claude Opus via Bedrock (primary), GPT-4o (secondary, for inter-judge agreement)
- **BM25:** rank_bm25 library, pickled to S3
- **Hybrid retrieval:** Reciprocal Rank Fusion (k=60)

## AWS Resources

- **Region:** eu-west-1
- **S3 bucket:** TBD (will be set in .env)
- **S3 Vectors bucket:** TBD (will be set in .env)
- **Bedrock models:** amazon.titan-embed-text-v2:0, cohere.embed-english-v3, Claude Sonnet 4.6, Claude Opus

---

## Repository Structure

```
rag-eval-framework/
├── CLAUDE.md                         # This file
├── README.md                         # Public-facing, results-led
├── pyproject.toml                    # Project config + dependencies (uv)
├── .env.example                      # Required environment variables
├── scripts/
│   ├── scrape_fca.py                 # FCA Handbook API scraper
│   ├── generate_policies.py          # Synthetic bank policy generator
│   ├── generate_qa.py                # Ground-truth Q&A pair generator
│   └── ingest.py                     # Chunking + embedding + S3 Vectors
├── src/
│   ├── __init__.py
│   ├── scraper/                      # FCA API client, JSONL writer
│   │   └── __init__.py
│   ├── chunking/                     # Fixed-size + structure-aware
│   │   └── __init__.py
│   ├── embeddings/                   # Titan + Cohere Bedrock clients
│   │   └── __init__.py
│   ├── vectorstore/                  # S3 Vectors read/write
│   │   └── __init__.py
│   ├── retrieval/                    # Dense + hybrid (RRF)
│   │   └── __init__.py
│   ├── generation/                   # Claude generation with citations
│   │   └── __init__.py
│   └── eval/                         # Judge prompts, metrics, runner
│       └── __init__.py
├── data/
│   ├── prompts/                      # Generation prompt templates
│   ├── fca/                          # Scraped FCA JSONL (gitignored)
│   ├── synthetic/                    # Generated policy docs (gitignored)
│   └── qa/                           # Ground-truth Q&A pairs
├── docs/
│   └── adr/                          # Architecture decision records
└── results/                          # Eval output (gitignored except summaries)
```

---

## Key Patterns

### FCA Handbook API

Two public REST endpoints, no authentication required:

- **Table of contents:** `GET https://api-handbook.fca.org.uk/Handbook/GetAllHandbook`
  Returns complete handbook hierarchy: blocks → sourcebooks → chapters → sections. Each node has an `entityId`.

- **Section content:** `GET https://api-handbook.fca.org.uk/Handbook/GetAllHandBookProvisionsSortedOrderByChapter/{chapterId}?sectionId={sectionId}&IsDeleted=false`
  Returns provisions with `provisionName` (rule ID), `provisionType` (Rules/Guidance/Evidential), `contentText` (plain text), `contentType` (HTML with cross-references).

### Config-driven pipeline

All pipeline components accept configuration parameters so any combination can be run:

```python
result = query_pipeline(
    question="...",
    retrieval_method="hybrid",      # dense | hybrid
    chunking_strategy="structure",  # fixed | structure
    embedding_model="titan",        # titan | cohere
    top_k=10
)
```

### Eval scoring

Claim-level grounding (not holistic 1-5 scale):
- Each answer is decomposed into individual claims
- Each claim classified: grounded / partially grounded / ungrounded
- Aggregated to percentages for the results table

### Ground-truth design

Q&A pairs use section-level references (e.g. "SYSC 10.1.3R"), not chunk IDs. The eval harness maps sections to chunk IDs per strategy, keeping ground truth strategy-agnostic.

---

## Testing

| Level | Tool | Scope |
|-------|------|-------|
| Unit | pytest | Chunkers, metrics, cross-reference parser |
| Integration | pytest | End-to-end pipeline with small test corpus |

```bash
uv run pytest
```

---

## Git Workflow

**Branch strategy:** Feature branches → PR → merge to main.

```
main                         ← protected
└── feature/jam-238-scraper  ← feature work, named by Linear issue
└── fix/<slug>               ← bug fixes
```

---

## Common Pitfalls & Constraints

- **Cohere Embed v3 has a 512-token input limit.** Structure-aware chunks exceeding this are silently truncated. Log warnings; document as a finding, not a bug.
- **tiktoken is a proxy for token counting.** Titan V2 and Cohere have different tokenisers. Counts are approximate.
- **S3 Vectors `returnMetadata=True` requires both `s3vectors:QueryVectors` AND `s3vectors:GetVectors` IAM permissions.** Missing the second causes a 403 at query time.
- **Cohere embedding requires `input_type` parameter.** Use `"search_document"` at ingestion, `"search_query"` at query time.
- **FCA API rate limiting:** No observed limits, but add 0.5-1s delay between calls. Be polite.

---

## Updating this document

Keep this file current as the project evolves. If a pattern, constraint, or resource changes, update it here.
