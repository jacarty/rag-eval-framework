# RAG Evaluation Results

Generated: 2026-06-07 16:57 UTC

## Configuration Comparison

| Config | Precision@k | Recall@k | % Grounded | % Ungrounded | Citation Acc | Latency (p50) | Cost/Query | Judge Agreement |
|--------|-------------|----------|------------|--------------|--------------|---------------|------------|-----------------|
| fixed-titan | 13.5% | 98.7% | 89.1% | 1.7% | 100.0% | 12548ms | $0.0983 | 76.8% |
| fixed-cohere | 12.1% | 96.2% | 91.8% | 1.3% | 100.0% | 12566ms | $0.0952 | 76.8% |
| structure-titan | 38.2% | 97.4% | 90.2% | 2.0% | 99.2% | 12760ms | $0.0965 | 77.9% |
| structure-cohere | 33.1% | 96.2% | 90.4% | 1.8% | 99.9% | 13327ms | $0.0965 | 75.5% |

*Based on 78 Q&A pairs per config*

## Metric Definitions

- **Precision@k**: Fraction of retrieved chunks that match ground-truth source sections
- **Recall@k**: Fraction of ground-truth source sections found in retrieved chunks
- **% Grounded**: Claims fully supported by retrieved context (primary judge)
- **% Ungrounded**: Claims with no supporting evidence (hallucination rate)
- **Citation Acc**: Fraction of model citations pointing to actual retrieved chunks
- **Latency (p50)**: Median end-to-end pipeline latency
- **Cost/Query**: Estimated Bedrock API cost (generation + judge calls)
- **Judge Agreement**: Claim-level agreement between primary and secondary judges
