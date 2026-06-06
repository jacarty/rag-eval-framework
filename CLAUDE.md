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

- **Language:** Python 3.13
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
│   ├── prompts/                      # Generation prompt templates (pinned)
│   ├── fca/
│   │   ├── fca_handbook.jsonl        # Scraped FCA source (pinned)
│   │   ├── sections/                 # Derived whole-section md (gitignored)
│   │   └── sections-structure/       # Derived token-capped chunks (gitignored)
│   ├── synthetic/
│   │   ├── policies/                 # Bedrock-generated source, non-deterministic (pinned)
│   │   └── policies-structure/       # Derived token-capped chunks (gitignored)
│   └── qa/                           # Ground-truth Q&A pairs (pinned)
├── docs/
│   └── adr/                          # Architecture decision records
└── results/                          # Eval output (gitignored except summaries)
```

**Data in git:** source corpora are pinned for reproducible eval results
(`fca/fca_handbook.jsonl`, `synthetic/policies/`, `qa/`, `prompts/`); everything
derived (`sections/`, `*-structure/`) is gitignored and rebuilt by the scripts.

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

- **Cohere Embed v3 has TWO hard limits at KB ingestion: 2048 *characters* AND 512 *tokens* — and the token limit is the binding one. Neither truncates; both fail the ingestion record.** Over 2048 chars → `Malformed input request: expected maxLength: 2048`. Over 512 tokens → `Invalid parameter combination` (Bedrock invokes Cohere with no truncation). The token limit is the harder constraint because token count is NOT proportional to characters: within a 2000-char budget, true Cohere token counts on the FCA corpus ranged 15–881. HTML entities are the main culprit — a single `&nbsp;` left in the scraped text inflates the token count sharply, so entity-laden annex/table sections blew past 512 tokens while staying under 2000 chars. The fix is upstream and two-part: (1) `clean_text()` in `convert_fca_to_sections.py` decodes HTML entities before chunking; (2) `src/chunking/structure.py` packs by **Cohere tokens** (cap 480, margin under 512), measured with Cohere's own tokenizer vendored at `src/chunking/cohere_tokenizer.json` (no network at runtime; `tokenizers` is a runtime dep). Files land in `*-structure` prefixes; both structure KBs share one prefix per corpus so the only variable between titan and cohere is the model. Note: ~140 chunks that *passed* were also >512 tokens — Cohere was silently truncating them (quality bug), so the token cap fixes those too. Titan's cap is ~8192 tokens / 50000 chars, so it is never the binding model.
- **Bedrock S3 metadata sidecars must be named `<full-filename>.metadata.json` (WITH the source extension) and wrapped in `{"metadataAttributes": {...}}`.** A sidecar named `<slug>.metadata.json` or containing a bare object is silently ignored — ingestion still succeeds but chunks carry no custom metadata (verify with a `retrieve` call: only `x-amz-bedrock-kb-*` keys come back). Keep custom metadata to short scalars: it is filterable by default and counts against the S3 Vectors 2048-byte filterable cap, so large lists (all of a section's `provision_ids`/`cross_references`) can breach it and fail ingestion. The eval maps ground truth via the scalar `section` key; provision IDs stay in the chunk text.
- **tiktoken is a proxy for token counting.** Titan V2 and Cohere have different tokenisers. Counts are approximate.
- **S3 Vectors `returnMetadata=True` requires both `s3vectors:QueryVectors` AND `s3vectors:GetVectors` IAM permissions.** Missing the second causes a 403 at query time.
- **Cohere embedding requires `input_type` parameter.** Use `"search_document"` at ingestion, `"search_query"` at query time.
- **Cohere on Bedrock is a Marketplace-served model — it must be enabled by a human first.** A user (not the KB service role) with AWS Marketplace permissions must call `InvokeModel` on `cohere.embed-english-v3` **once** to enable it account-wide; the KB role cannot bootstrap this itself and will 403 with "not authorized to perform AWS Marketplace actions" until it's done. The entitlement takes ~2 minutes to propagate after the first invoke ("subscription cannot be completed at this time... try again after 2 minutes" is transient, not fatal). Note: the Marketplace "Launch / Configure" product (SageMaker/CloudFormation/CLI endpoint deploy) is a *different*, hourly-billed offering — do **not** use it for the serverless on-demand model the KBs need.
- **Account pinning matters — the stack lives in member account `982099554067`, not the Org management account `449154017877`.** Marketplace subscriptions and model enablement are per-account, so enabling Cohere in the management account does nothing for the KBs. The default AWS profile resolves to the management account; `.env` pins `AWS_PROFILE=AdministratorAccess-982099554067` so the pipeline always targets the right one.
- **One ingestion job per KB at a time.** `start_ingestion_job` rejects a second data source while the first is running, so the two sources on a KB MUST be sequenced. `sync_all` now starts each job, polls `get_ingestion_job` until a terminal state (`COMPLETE`/`FAILED`/`STOPPED`), then starts the next — so a single `--sync-only` pass takes all 8 data sources (4 KBs × fca + synthetic) to completion and prints a status summary. (The old version fired both sources 2s apart and only caught the literal string `"concurrent ingestion"`, which never matched Bedrock's actual message — so the synthetic source was silently skipped on three KBs.)
- **FCA API rate limiting:** No observed limits, but add 0.5-1s delay between calls. Be polite.

---

## Updating this document

Keep this file current as the project evolves. If a pattern, constraint, or resource changes, update it here.
