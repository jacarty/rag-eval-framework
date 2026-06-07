"""RAG evaluation runner.

Runs ground-truth Q&A pairs through pipeline configurations, scores results
using LLM-as-judge and automated metrics, and outputs comparison tables.

Usage:
    # Run all 4 configs
    uv run python scripts/run_eval.py --all

    # Single config
    uv run python scripts/run_eval.py --chunking structure --embedding titan

    # Subset of questions (first 5)
    uv run python scripts/run_eval.py --all --limit 5

    # Skip judge calls (retrieval + generation metrics only)
    uv run python scripts/run_eval.py --all --skip-judges

    # Single judge only (faster)
    uv run python scripts/run_eval.py --all --primary-judge-only
"""

import argparse
import json
import logging
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.judge import JudgeResult, run_dual_judges, run_judge  # noqa: E402
from src.metrics import (  # noqa: E402
    AggregateMetrics,
    QueryMetrics,
    compute_aggregate_metrics,
    compute_citation_metrics,
    compute_cost,
    compute_faithfulness_metrics,
    compute_inter_judge_agreement,
    compute_retrieval_metrics,
)
from src.pipeline import (  # noqa: E402
    PipelineConfig,
    _get_bedrock_runtime_client,
    query_pipeline,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

QA_PATH = Path("data/qa/qa_pairs.json")
OUTPUT_DIR = Path("data/eval")

ALL_CONFIGS = [
    ("fixed", "titan"),
    ("fixed", "cohere"),
    ("structure", "titan"),
    ("structure", "cohere"),
]


# ---------------------------------------------------------------------------
# Q&A loading
# ---------------------------------------------------------------------------


def load_qa_pairs(path: Path = QA_PATH, *, limit: int | None = None) -> list[dict]:
    """Load ground-truth Q&A pairs."""
    with open(path) as f:
        pairs = json.load(f)
    if limit:
        pairs = pairs[:limit]
    logger.info("Loaded %d Q&A pairs", len(pairs))
    return pairs


# ---------------------------------------------------------------------------
# Single query evaluation
# ---------------------------------------------------------------------------


def evaluate_single(
    qa_pair: dict,
    config: PipelineConfig,
    judge_client,
    *,
    skip_judges: bool = False,
    primary_only: bool = False,
    profile: str | None = None,
) -> dict:
    """Evaluate a single Q&A pair against a single config.

    Returns a dict with pipeline result, judge results, and computed metrics.
    """
    question = qa_pair["question"]
    question_id = qa_pair["question_id"]
    source_sections = qa_pair["source_sections"]
    config_label = f"{config.chunking}-{config.embedding}"

    logger.info("Evaluating %s on %s", question_id, config_label)

    # --- Run pipeline ---
    try:
        result = query_pipeline(question, config=config, profile=profile)
    except Exception as e:
        logger.error("Pipeline failed for %s on %s: %s", question_id, config_label, e)
        return {"question_id": question_id, "config": config_label, "error": str(e)}

    # --- Retrieval metrics ---
    chunk_dicts = [c.model_dump() for c in result.retrieved_chunks]
    retrieved_ids = {c.chunk_id for c in result.retrieved_chunks}
    retrieval_metrics = compute_retrieval_metrics(source_sections, chunk_dicts)

    # --- Citation metrics ---
    from src.metrics import resolve_relevant_chunks

    relevant_ids = resolve_relevant_chunks(source_sections, chunk_dicts)
    citation_metrics = compute_citation_metrics(
        result.citations,
        retrieved_ids,
        relevant_ids,
    )

    # --- Judge evaluation ---
    primary_result = JudgeResult(claims=[], judge_model="skipped", latency_ms=0)
    secondary_result = JudgeResult(claims=[], judge_model="skipped", latency_ms=0)

    if not skip_judges:
        if primary_only:
            primary_result = run_judge(
                judge_client,
                question,
                result.answer,
                chunk_dicts,
            )
            secondary_result = JudgeResult(
                claims=[],
                judge_model="skipped",
                latency_ms=0,
            )
        else:
            primary_result, secondary_result = run_dual_judges(
                judge_client,
                question,
                result.answer,
                chunk_dicts,
            )

    # --- Faithfulness metrics ---
    faith_primary = compute_faithfulness_metrics(primary_result)
    faith_secondary = compute_faithfulness_metrics(secondary_result)

    # --- Cost ---
    cost = compute_cost(
        result.usage,
        primary_result.usage,
        secondary_result.usage,
    )

    # --- Inter-judge agreement ---
    agreement = 0.0
    if primary_result.claims and secondary_result.claims:
        agreement = compute_inter_judge_agreement(
            primary_result.claims,
            secondary_result.claims,
        )

    # --- Assemble query metrics ---
    query_metrics = QueryMetrics(
        question_id=question_id,
        config_label=config_label,
        retrieval=retrieval_metrics,
        citation=citation_metrics,
        faithfulness_primary=faith_primary,
        faithfulness_secondary=faith_secondary,
        latency_ms=result.latency_ms,
        retrieval_latency_ms=result.retrieval_latency_ms,
        generation_latency_ms=result.generation_latency_ms,
        cost=cost,
    )

    return {
        "question_id": question_id,
        "config": config_label,
        "question": question,
        "ground_truth_answer": qa_pair["answer"],
        "source_sections": source_sections,
        "difficulty": qa_pair.get("difficulty", "unknown"),
        "type": qa_pair.get("type", "unknown"),
        "generated_answer": result.answer,
        "citations": result.citations,
        "confidence": result.confidence,
        "insufficient_context": result.insufficient_context,
        "retrieved_chunks": [
            {
                "chunk_id": c.chunk_id,
                "score": c.score,
                "section": c.metadata.get("section", "unknown"),
            }
            for c in result.retrieved_chunks
        ],
        "metrics": query_metrics.model_dump(),
        "judge_primary": primary_result.model_dump() if primary_result.claims else None,
        "judge_secondary": secondary_result.model_dump() if secondary_result.claims else None,
        "inter_judge_agreement": agreement,
        "latency_ms": result.latency_ms,
        "usage": result.usage,
    }


# ---------------------------------------------------------------------------
# Config-level evaluation
# ---------------------------------------------------------------------------


def evaluate_config(
    qa_pairs: list[dict],
    chunking: str,
    embedding: str,
    *,
    skip_judges: bool = False,
    primary_only: bool = False,
    profile: str | None = None,
) -> tuple[list[dict], AggregateMetrics]:
    """Evaluate all Q&A pairs against a single config.

    Returns:
        Tuple of (per-query results list, aggregate metrics)
    """
    config = PipelineConfig(chunking=chunking, embedding=embedding)
    config_label = f"{chunking}-{embedding}"
    judge_client = _get_bedrock_runtime_client(profile)

    results = []
    query_metrics_list = []

    for i, qa_pair in enumerate(qa_pairs, 1):
        logger.info(
            "[%d/%d] %s on %s",
            i,
            len(qa_pairs),
            qa_pair["question_id"],
            config_label,
        )

        result = evaluate_single(
            qa_pair,
            config,
            judge_client,
            skip_judges=skip_judges,
            primary_only=primary_only,
            profile=profile,
        )
        results.append(result)

        if "error" not in result:
            query_metrics_list.append(QueryMetrics(**result["metrics"]))

    # Aggregate
    aggregate = compute_aggregate_metrics(query_metrics_list, config_label)

    # Compute overall inter-judge agreement
    if not skip_judges and not primary_only:
        agreements = [
            r["inter_judge_agreement"]
            for r in results
            if "error" not in r and r.get("inter_judge_agreement", 0) > 0
        ]
        if agreements:
            import statistics

            aggregate.inter_judge_agreement = statistics.mean(agreements)

    return results, aggregate


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def save_results(
    all_results: dict[str, list[dict]],
    all_aggregates: dict[str, AggregateMetrics],
    output_dir: Path,
) -> None:
    """Save evaluation results to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    # Per-question detail (JSON)
    detail_path = output_dir / f"eval_detail_{timestamp}.json"
    with open(detail_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    logger.info("Saved detail results to %s", detail_path)

    # Aggregate results (JSON)
    agg_path = output_dir / f"eval_aggregate_{timestamp}.json"
    agg_data = {k: v.model_dump() for k, v in all_aggregates.items()}
    with open(agg_path, "w") as f:
        json.dump(agg_data, f, indent=2, default=str)
    logger.info("Saved aggregate results to %s", agg_path)

    # Comparison table (Markdown)
    md_path = output_dir / f"eval_comparison_{timestamp}.md"
    md_content = format_comparison_table(all_aggregates)
    with open(md_path, "w") as f:
        f.write(md_content)
    logger.info("Saved comparison table to %s", md_path)

    # Also save as latest (for easy access)
    latest_detail = output_dir / "eval_detail_latest.json"
    latest_agg = output_dir / "eval_aggregate_latest.json"
    latest_md = output_dir / "eval_comparison_latest.md"
    with open(latest_detail, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    with open(latest_agg, "w") as f:
        json.dump(agg_data, f, indent=2, default=str)
    with open(latest_md, "w") as f:
        f.write(md_content)


def format_comparison_table(aggregates: dict[str, AggregateMetrics]) -> str:
    """Format aggregate metrics as a Markdown comparison table."""
    lines = [
        "# RAG Evaluation Results",
        "",
        f"Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Configuration Comparison",
        "",
        "| Config | Precision@k | Recall@k | % Grounded | % Ungrounded | Citation Acc | Latency (p50) | Cost/Query | Judge Agreement |",
        "|--------|-------------|----------|------------|--------------|--------------|---------------|------------|-----------------|",
    ]

    for label, agg in aggregates.items():
        lines.append(
            f"| {label} "
            f"| {agg.retrieval_precision_mean:.1%} "
            f"| {agg.retrieval_recall_mean:.1%} "
            f"| {agg.grounded_pct_mean:.1%} "
            f"| {agg.ungrounded_pct_mean:.1%} "
            f"| {agg.citation_precision_mean:.1%} "
            f"| {agg.latency.median_ms:.0f}ms "
            f"| ${agg.cost_per_query_mean:.4f} "
            f"| {agg.inter_judge_agreement:.1%} |"
        )

    lines.extend(
        [
            "",
            f"*Based on {next(iter(aggregates.values())).n_queries} Q&A pairs per config*",
            "",
            "## Metric Definitions",
            "",
            "- **Precision@k**: Fraction of retrieved chunks that match ground-truth source sections",
            "- **Recall@k**: Fraction of ground-truth source sections found in retrieved chunks",
            "- **% Grounded**: Claims fully supported by retrieved context (primary judge)",
            "- **% Ungrounded**: Claims with no supporting evidence (hallucination rate)",
            "- **Citation Acc**: Fraction of model citations pointing to actual retrieved chunks",
            "- **Latency (p50)**: Median end-to-end pipeline latency",
            "- **Cost/Query**: Estimated Bedrock API cost (generation + judge calls)",
            "- **Judge Agreement**: Claim-level agreement between Claude Opus and gpt-oss-120b judges",
        ]
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run RAG evaluation across pipeline configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--chunking",
        choices=["fixed", "structure"],
        default="structure",
        help="Chunking strategy (default: structure)",
    )
    parser.add_argument(
        "--embedding",
        choices=["titan", "cohere"],
        default="titan",
        help="Embedding model (default: titan)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run across all 4 KB configurations",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of Q&A pairs to evaluate",
    )
    parser.add_argument(
        "--skip-judges",
        action="store_true",
        help="Skip judge calls (retrieval + generation metrics only)",
    )
    parser.add_argument(
        "--primary-judge-only",
        action="store_true",
        help="Run primary judge (Claude Opus) only, skip secondary",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OUTPUT_DIR),
        help=f"Output directory (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="AWS profile name",
    )
    parser.add_argument(
        "--qa-file",
        type=str,
        default=str(QA_PATH),
        help=f"Path to Q&A pairs file (default: {QA_PATH})",
    )
    args = parser.parse_args()

    qa_pairs = load_qa_pairs(Path(args.qa_file), limit=args.limit)
    configs = ALL_CONFIGS if args.all else [(args.chunking, args.embedding)]
    output_dir = Path(args.output_dir)

    all_results = {}
    all_aggregates = {}

    total_start = time.perf_counter()

    for chunking, embedding in configs:
        config_label = f"{chunking}-{embedding}"
        logger.info("=" * 60)
        logger.info("Starting evaluation: %s", config_label)
        logger.info("=" * 60)

        results, aggregate = evaluate_config(
            qa_pairs,
            chunking=chunking,
            embedding=embedding,
            skip_judges=args.skip_judges,
            primary_only=args.primary_judge_only,
            profile=args.profile,
        )

        all_results[config_label] = results
        all_aggregates[config_label] = aggregate

        logger.info(
            "%s: precision=%.1f%% recall=%.1f%% grounded=%.1f%% latency_p50=%.0fms",
            config_label,
            aggregate.retrieval_precision_mean * 100,
            aggregate.retrieval_recall_mean * 100,
            aggregate.grounded_pct_mean * 100,
            aggregate.latency.median_ms,
        )

    total_elapsed = (time.perf_counter() - total_start) / 60

    # Save results
    save_results(all_results, all_aggregates, output_dir)

    # Print comparison table
    print("\n")
    print(format_comparison_table(all_aggregates))
    print(f"\nTotal evaluation time: {total_elapsed:.1f} minutes")
    print(f"Results saved to {output_dir}/")


if __name__ == "__main__":
    main()
