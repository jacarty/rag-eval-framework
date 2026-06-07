# RAG Evaluation Results

Generated: 2026-06-07 07:05 UTC

## Configuration Comparison

| Config | Precision@k | Recall@k | % Grounded | % Ungrounded | Citation Acc | Latency (p50) | Cost/Query | Judge Agreement |
|--------|-------------|----------|------------|--------------|--------------|---------------|------------|-----------------|
| structure-titan | 45.0% | 100.0% | 100.0% | 0.0% | 100.0% | 7106ms | $0.2105 | 100.0% |

*Based on 2 Q&A pairs per config*

## Metric Definitions

- **Precision@k**: Fraction of retrieved chunks that match ground-truth source sections
- **Recall@k**: Fraction of ground-truth source sections found in retrieved chunks
- **% Grounded**: Claims fully supported by retrieved context (primary judge)
- **% Ungrounded**: Claims with no supporting evidence (hallucination rate)
- **Citation Acc**: Fraction of model citations pointing to actual retrieved chunks
- **Latency (p50)**: Median end-to-end pipeline latency
- **Cost/Query**: Estimated Bedrock API cost (generation + judge calls)
- **Judge Agreement**: Claim-level agreement between Claude Opus and gpt-oss-120b judges
