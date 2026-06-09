# RAG Evaluation Framework

A configurable framework for quantifying how chunking strategies, embedding models, and retrieval methods affect RAG quality. Built on AWS Bedrock Knowledge Bases with dual LLM-as-judge evaluation.

## Results

78 ground-truth Q&A pairs evaluated across 4 pipeline configurations. Each answer scored by two independent judges (Claude Haiku 4.5 and GPT-oss-120b) for claim-level faithfulness.

| Config | Precision@k | Recall@k | % Grounded | % Ungrounded | Citation Acc | Latency (p50) | Cost/Query | Judge Agreement |
|--------|-------------|----------|------------|--------------|--------------|---------------|------------|-----------------|
| **structure-titan** | **38.2%** | 97.4% | 90.2% | 2.0% | 99.2% | 12,760ms | $0.097 | 77.9% |
| **structure-cohere** | **33.1%** | 96.2% | 90.4% | 1.8% | 99.9% | 13,327ms | $0.097 | 75.5% |
| fixed-titan | 13.5% | 98.7% | 89.1% | 1.7% | 100.0% | 12,548ms | $0.098 | 76.8% |
| fixed-cohere | 12.1% | 96.2% | 91.8% | 1.3% | 100.0% | 12,566ms | $0.095 | 76.8% |

## Key Findings

**Structure-aware chunking delivers 3× better retrieval precision.** Aligning chunk boundaries to the FCA Handbook's module/chapter/section/provision hierarchy (38.2% precision) dramatically outperforms fixed-size splitting (13.5%). The retrieval system returns far less noise when chunks correspond to complete regulatory provisions rather than arbitrary 512-token windows.

**Embedding model choice is secondary.** Titan slightly outperforms Cohere within each chunking strategy (38.2% vs 33.1% for structure-aware, 13.5% vs 12.1% for fixed), but the gap is small compared to the chunking effect.

**Faithfulness is strong across all configurations.** ~90% of claims are fully grounded in retrieved context, with <2% hallucination regardless of pipeline config. Claude Sonnet 4.6 with structured outputs stays well-grounded even with lower-precision retrieval.

**Recall is uniformly high.** All four configurations find the relevant sections 96-99% of the time. The difference is how much irrelevant material comes along for the ride.

**Hybrid search is unavailable on S3 Vectors.** The planned 8-configuration matrix (2 chunking × 2 embedding × 2 retrieval) reduced to 4 because S3 Vectors does not support hybrid (dense + BM25) search. This is a platform constraint, not a design choice.

## What This Is

A framework for running controlled experiments on RAG pipelines. Given a document corpus, it:

1. Chunks documents using configurable strategies
2. Embeds and indexes chunks in Bedrock Knowledge Bases
3. Retrieves against a ground-truth Q&A set
4. Generates answers with Claude using structured outputs
5. Scores each answer with dual LLM judges (claim-level faithfulness)
6. Computes retrieval precision/recall, citation accuracy, cost, and latency
7. Outputs comparison tables across configurations

The reference implementation uses UK Financial Conduct Authority (FCA) Handbook text as the corpus. Regulatory data is a good stress test for RAG: explicit document hierarchy, dense cross-references between sections, and precise terminology where a wrong word changes the legal meaning.

## Architecture

```
FCA Handbook API ──→ scrape_fca.py ──→ fca_handbook.jsonl (28MB, 1246 sections)
                                            │
                    ┌───────────────────────┤
                    ▼                       ▼
         convert_fca_to_sections.py    generate_policies.py
         (whole-section markdown)      (20 synthetic bank policies)
                    │                       │
        ┌───────────┤                       │
        ▼           ▼                       ▼
   Fixed-size    Structure-aware      Policy markdown
   (Bedrock)     (provision-level)    + metadata sidecars
        │           │                       │
        ▼           ▼                       ▼
   ┌─────────────────────────────────────────────┐
   │  4 Bedrock Knowledge Bases (S3 Vectors)     │
   │  fixed-titan  │  fixed-cohere               │
   │  structure-titan  │  structure-cohere        │
   └─────────────────────────────────────────────┘
                        │
                        ▼ Retrieve API (SEMANTIC)
                        │
   ┌─────────────────────────────────────────────┐
   │  Pipeline (src/pipeline.py)                 │
   │  retrieve chunks → Claude Sonnet 4.6       │
   │  structured outputs → PipelineResult        │
   └─────────────────────────────────────────────┘
                        │
                        ▼
   ┌─────────────────────────────────────────────┐
   │  Eval Harness (scripts/run_eval.py)         │
   │  78 Q&A pairs × 4 configs                  │
   │  Dual judges: Haiku 4.5 + gpt-oss-120b     │
   │  Metrics: precision, recall, faithfulness,  │
   │           citations, latency, cost          │
   └─────────────────────────────────────────────┘
                        │
                        ▼
               Comparison tables
```

## Repository Structure

```
rag-eval-framework/
├── src/
│   ├── pipeline.py           # Retrieval + generation pipeline (Pydantic-typed)
│   ├── judge.py              # Dual LLM-as-judge (claim-level faithfulness)
│   ├── metrics.py            # Precision, recall, faithfulness, cost metrics
│   ├── scraper/              # FCA Handbook API client
│   └── chunking/             # Structure-aware chunker + Cohere tokenizer
├── scripts/
│   ├── scrape_fca.py         # Scrape FCA Handbook to JSONL
│   ├── convert_fca_to_sections.py  # Split JSONL → section markdown files
│   ├── generate_policies.py  # Generate synthetic bank policies via Bedrock
│   ├── generate_qa.py        # Generate ground-truth Q&A pairs (Claude Opus + GPT critic)
│   ├── patch_difficulty.py   # Recover difficulty-only critic failures
│   ├── setup_knowledge_bases.py  # Create and sync 4 Bedrock KBs
│   ├── query.py              # CLI for manual pipeline testing
│   └── run_eval.py           # Full evaluation runner with checkpointing
├── config/
│   └── knowledge_bases.json  # KB IDs and configuration
├── data/
│   ├── fca/                  # FCA source data (fca_handbook.jsonl pinned)
│   ├── synthetic/policies/   # 20 synthetic bank policies with metadata sidecars
│   ├── qa/                   # 78 ground-truth Q&A pairs
│   ├── prompts/              # Generation and evaluation prompts
│   └── eval/                 # Evaluation results and checkpoints
├── docs/
│   ├── adr/                  # Architecture decision records
│   └── section_chunk_mapping.md  # How Q&A source refs map to KB chunks
├── pyproject.toml            # Dependencies (uv/hatch)
└── .env.example              # Required AWS configuration
```

## Eval Methodology

### Ground-Truth Q&A Pairs

78 curated pairs generated by Claude Opus 4.6, validated by GPT-oss-120b as an independent critic. Three types:

| Type | Count | Description |
|------|-------|-------------|
| Single-module | 24 | Answerable from one FCA section |
| Cross-module | 32 | Requires 2-3 FCA sections |
| Policy-regulation | 22 | Spans synthetic policies and referenced FCA provisions |

Each pair includes `source_sections` — the ground-truth sections that should be retrieved.

### Metrics

**Retrieval Precision@k** — What fraction of retrieved chunks come from ground-truth source sections? Higher means less noise in the context window.

**Retrieval Recall@k** — What fraction of ground-truth source sections appear in the retrieved chunks? Higher means fewer missed relevant sections.

**% Grounded** — What fraction of claims in the generated answer are directly supported by a retrieved chunk? Assessed per-claim by the LLM judge.

**% Ungrounded** — What fraction of claims have no supporting evidence in any retrieved chunk? This is the hallucination rate.

**Citation Accuracy** — Do the model's self-reported citations point to chunks that were actually retrieved?

**Inter-Judge Agreement** — Claim-level agreement between primary (Claude Haiku 4.5) and secondary (GPT-oss-120b) judges. ~77% agreement indicates reasonable calibration.

### Judge Design

Each judge decomposes the answer into individual factual claims, then classifies each as GROUNDED, PARTIALLY_GROUNDED, or UNGROUNDED against the retrieved chunks. This avoids the score-clustering problem of holistic 1-5 ratings — "87% of claims grounded" is more actionable than "3.8/5".

Two judges from different model families (Anthropic + OpenAI) provide a cross-provider consistency check. The inter-judge agreement metric flags where the judges disagree, which typically occurs at the GROUNDED/PARTIALLY_GROUNDED boundary.

## How to Run

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- AWS account with Bedrock model access enabled for: Claude Sonnet 4.6, Claude Haiku 4.5, Claude Opus 4.6, Cohere Embed English v3, Amazon Titan Embeddings v2, GPT-oss-120b
- AWS CLI configured with a named profile

### Setup

```bash
git clone https://github.com/jacarty/rag-eval-framework.git
cd rag-eval-framework
cp .env.example .env   # edit with your AWS config
uv sync
```

### Run the Pipeline

```bash
# Single query (default: structure-titan config)
uv run python scripts/query.py "What are the FCA Principles for Business?"

# Compare all 4 configs on one question
uv run python scripts/query.py "What are the FCA Principles for Business?" --all

# Retrieve only (no generation cost)
uv run python scripts/query.py "SYSC 10.1 conflicts of interest" --retrieve-only
```

### Run the Evaluation

```bash
# Quick test — 5 questions, skip judges (~$1)
uv run python scripts/run_eval.py --all --limit 5 --skip-judges

# Full run with Haiku judge (~$12, ~3 hours)
uv run python scripts/run_eval.py --all --primary-judge haiku

# Full run with dual judges (~$12, ~3 hours)
uv run python scripts/run_eval.py --all --primary-judge haiku

# Resume after interruption (per-question checkpointing)
uv run python scripts/run_eval.py --all --primary-judge haiku --resume

# Use Opus as judge (higher quality, ~$65)
uv run python scripts/run_eval.py --all --primary-judge opus
```

Results are saved to `data/eval/` as timestamped JSON detail, aggregate JSON, and Markdown comparison tables.

## Lessons Learned

**S3 Vectors is the right managed vector store for Bedrock KBs, but hybrid search is off the table.** The fully managed ingestion pipeline avoids manual embedding calls and BM25 index maintenance. The trade-off: no hybrid search support, reducing the config matrix from 8 to 4.

**Cohere's 512-token embedding limit is the binding constraint on chunk size.** The 2,048-character input limit maps to roughly 480 Cohere tokens. Structure-aware chunks need both character and token caps, enforced with a vendored Cohere tokenizer.

**Bedrock structured outputs work well for enforcing response schemas.** Passing a Pydantic-derived JSON schema via `outputConfig.textFormat` constrains Claude's output at the grammar level. First call compiles the schema (~30s), then it's cached for 24 hours.

**Different generators from different providers as judges prevents self-enhancement bias.** Using Claude to judge Claude's own output risks inflated scores. The dual-judge design (Anthropic + OpenAI) with inter-judge agreement metrics makes this transparent.

**Per-question checkpointing is essential for long eval runs.** A 312-query eval run takes ~3 hours. Without checkpointing, a crash at question 290 loses everything. The checkpoint file saves after every question and supports resume.

## Future Work

- **Hybrid search** — migrate to OpenSearch Serverless to unlock hybrid (dense + BM25) retrieval and complete the 8-configuration matrix
- **Model comparison** — the pipeline already accepts configurable generation models; evaluating Haiku vs Sonnet vs Opus as the answer generator would quantify the quality/cost trade-off
- **Agentic retrieval** — replace single-shot retrieval with iterative tool-use retrieval where the model decides when to search again
- **Larger corpus** — extend beyond FCA to test domain-transfer properties of each configuration

## Licence

MIT
