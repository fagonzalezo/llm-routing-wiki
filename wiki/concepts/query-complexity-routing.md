---
type: concept
title: "Query Complexity Routing"
tags: [llm-routing, cost-optimization, pre-generation-routing]
sources: [varangot-reille-2025-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Query Complexity Routing

**Query complexity routing** is a [[pre-generation-routing]] strategy that estimates the *difficulty* of a user query for a given LLM, then routes the query to the cheapest model with sufficient ability to answer it correctly. The central insight is that not all queries require the same model capacity: a simple factual question can be answered by a small model, while multi-hop reasoning over long documents requires a larger one.

This is the most prevalent strategy in the routing literature (Varangot-Reille et al. 2025, §4.2.3), appearing across supervised, similarity-based, and generative implementation families.

## Complexity Taxonomy

Varangot-Reille et al. define query complexity within RAG-based conversational agents as follows:

| Level | Description | Example |
|---|---|---|
| **Low** | Simple greeting or chitchat; no retrieval needed | "Hello! What can you do?" |
| **Intermediate** | Explicit information extraction from a single document | "What is the capital mentioned in paragraph 3?" |
| **High** | Implicit reasoning across multiple documents | "How did the policy changes in 2020 affect outcomes described in reports A, B, and C?" |

## Why Complexity Matters

Different LLMs differ in parameter count (e.g., Llama-3.2-3B vs. Llama-3.1-405B) and domain coverage. Routing all queries to the largest model wastes resources on easy queries. Routing all queries to the smallest model produces poor results on hard queries. Complexity estimation is the mechanism that allocates resources proportionally to demand.

## Implementation Approaches

### Supervised Complexity Estimation
Train a lightweight classifier on (query, difficulty-label) pairs:
- Small BERT-based models (DeBERTa variants, DistilBERT) trained to predict difficulty.
- Labels derived from: expert annotation, model accuracy on held-out queries, LLM-as-judge scoring.

### Generative Complexity Estimation
Prompt an LLM to assess its own confidence or estimate difficulty before generating a full response:
- Low cost if using a small meta-LLM as the complexity estimator.
- Sensitive to prompt formulation.

### Similarity-Based Proxy
Use nearest-neighbor lookup: if a query is similar to past queries that a small model answered correctly, route to the small model. [[knn-routing]] page covers this.

### Confidence / Uncertainty Signals
- **Semantic entropy**: high entropy across multiple sampled outputs signals high uncertainty → route to a larger model.
- **Log-probability calibration**: low token log-probs from a draft model signal the query exceeds its capability.

## Key Trade-offs and Limitations

- **Labelling cost**: supervised complexity estimators require labelled training data that may be expensive to obtain.
- **Generalisation**: complexity is domain-dependent; a model trained on one domain's complexity distribution may fail on another.
- **Calibration**: under-estimation routes hard queries to weak models (quality loss); over-estimation routes easy queries to strong models (cost waste).
- **Circular dependency**: to evaluate whether a model can handle a query, you may need the model to attempt the query — which is what you're trying to avoid.

## Where This Fits

- [[varangot-reille-2025-routing-survey]] — §3.1 and §4.2.3; the primary source and taxonomy.
- [[pre-generation-routing]] — parent concept; complexity routing is a sub-strategy.
- [[knn-routing]] — similarity-based proxy for complexity estimation.
- [[model-routing]] — the broader routing paradigm this serves.
- [[llm-cascade]] — post-generation routing alternative that avoids complexity estimation by evaluating actual outputs.
- [[irtnet]] — applies Item Response Theory to learn explicit difficulty scores per query and ability scores per model, providing a principled complexity framework.
- [[routereval]] — benchmark that evaluates routing strategies across three difficulty levels (easy/medium/hard), implicitly operationalising query complexity.
