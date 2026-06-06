# rag-eval-framework

A configurable RAG evaluation framework with quantified comparisons across chunking strategies, embedding models, and retrieval methods.

## What this is

This project evaluates how different RAG pipeline configurations affect retrieval quality, answer faithfulness, and cost. The framework is domain-agnostic — it takes a corpus, chunks it, embeds it, retrieves against it, and scores the results. The eval harness can be pointed at any document collection.

The reference implementation uses UK Financial Conduct Authority (FCA) regulatory text as the corpus. Regulatory data is a good stress test for RAG: it has explicit document hierarchy, dense cross-references between sections, and precise terminology where a wrong word changes the legal meaning.

## Eval dimensions

Each configuration is scored on:

| Metric | Method |
|--------|--------|
| Retrieval Precision@k | Automated — retrieved chunks vs ground-truth |
| Retrieval Recall@k | Automated — ground-truth coverage in top-k |
| Answer Faithfulness | LLM-judge — per-claim grounding check |
| Hallucination Rate | LLM-judge — percentage of ungrounded claims |
| Citation Accuracy | Automated + LLM-judge |
| Inter-judge Agreement | Two independent LLM judges compared |
| Latency | Automated — end-to-end wall-clock time |
| Cost per Query | Automated — from API usage metadata |

## Configuration matrix

Compared across **8 configurations**: 2 chunking strategies × 2 embedding models × 2 retrieval methods.

| Dimension | Options |
|-----------|---------|
| Chunking | Fixed-size (512 tokens, baseline) · Structure-aware (preserves document hierarchy) |
| Embedding | Amazon Titan Text Embeddings V2 · Cohere Embed English v3 |
| Retrieval | Dense (cosine similarity) · Hybrid (dense + BM25 via Reciprocal Rank Fusion) |

## Results

_Results will be added here once the eval pipeline has been run._

## Project status

This project is under active development. See the issue tracker for current progress.

## Architecture

```
Corpus (FCA Handbook API / synthetic policies)
  → Ingestion pipeline (chunking + embedding)
  → S3 Vectors (vector store)
  → Retrieval pipeline (dense / hybrid)
  → Claude Sonnet (generation with citations)
  → Claude Opus + GPT-4o (dual LLM-as-judge evaluation)
  → Comparison tables + analysis
```

## Repository structure

```
rag-eval-framework/
├── scripts/                  # CLI entry points
│   └── scrape_fca.py         # FCA Handbook API scraper
├── src/
│   ├── scraper/              # FCA API client + JSONL writer
│   ├── chunking/             # Fixed-size + structure-aware chunkers
│   ├── embeddings/           # Titan + Cohere via Bedrock
│   ├── vectorstore/          # S3 Vectors client
│   ├── retrieval/            # Dense + hybrid retrieval
│   ├── generation/           # Claude generation with citations
│   └── eval/                 # Judge prompts, metrics, config runner
├── data/
│   ├── prompts/              # Synthetic data generation prompts
│   └── qa/                   # Ground-truth Q&A pairs
├── docs/
│   └── adr/                  # Architecture decision records
└── results/                  # Eval output
```

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) for package management
- AWS account with Bedrock model access (Titan Embeddings V2, Cohere Embed English v3, Claude Sonnet, Claude Opus)
- S3 Vectors bucket provisioned

## Setup

```bash
git clone https://github.com/jacarty/rag-eval-framework.git
cd rag-eval-framework
cp .env.example .env  # fill in your AWS config
uv sync
```

## Licence

MIT
