---
type: concept
title: "kNN Routing"
tags: [llm-routing, non-parametric, methodology]
sources: [li-2025-predictive-routing, hu-2024-routerbench]
created: 2026-06-06
updated: 2026-06-06
graph:
  relationships:
    - predicate: depends_on
      object: concept:model-routing
      source: li-2025-predictive-routing
      evidence: "kNN routing is an approach to LLM routing where a router selects the optimal model... by retrieving similar queries"
      confidence: high
      status: current
---

# kNN Routing

**kNN Routing** (or $k$-Nearest Neighbors Routing) is a non-parametric approach to [[model-routing]] where a router selects the optimal model for a given input query by retrieving semantically similar queries from a pre-populated support set of validation data and averaging their performance and cost history. 

Unlike parametric routers that train complex models (such as neural networks or matrix factorization) to predict model performance, kNN routing is entirely non-parametric, leveraging the inherent locality of queries in an embedding space.

## Core Mechanism

Given a target query $x$, a candidate pool of models $M = \{m_1, m_2, \dots, m_M\}$, and a cost-performance trade-off parameter $\lambda$, kNN routing operates as follows:

1. **Embedding**: The target query $x$ is converted into a vector embedding using a pre-trained embedding model (e.g., text embeddings or vision-language embeddings).
2. **Neighborhood Retrieval**: The router finds the $k$ nearest neighbors $N_k(x)$ of query $x$ in a historical support set $D_{\text{support}} = \{(x_i, m, s(x_i, m), c(x_i, m))\}$, where $s$ is the performance score and $c$ is the cost.
3. **Utility Estimation**: The performance and cost of each candidate model $m$ are estimated by averaging the results of the retrieved neighbors:
   $$\hat{s}(x, m) = \frac{1}{k} \sum_{i \in N_k(x)} s(x_i, m)$$
   $$\hat{c}(x, m) = \frac{1}{k} \sum_{i \in N_k(x)} c(x_i, m)$$
4. **Model Selection**: The model with the highest predicted utility is selected:
   $$m^* = \operatorname{argmax}_{m \in M} [\hat{s}(x, m) - \lambda \cdot \hat{c}(x, m)]$$

## Advantages & Strengths

According to [[li-2025-predictive-routing]], kNN routing has several key advantages:
* **Zero Retraining (Dynamic Adaptation)**: Since it is non-parametric, new models or new training data can be added to the support set $D_{\text{support}}$ instantly without retraining the router. This makes it highly compatible with [[dynamic-routing]].
* **Computational Efficiency**: Test-time inference only requires a vector search (which can be accelerated using vector indexes) and simple averaging, bypassing the forward pass of complex neural network architectures.
* **Robustness to Distribution Shift**: Shows higher stability and performance under out-of-distribution (OOD) queries compared to overparameterized parametric models that might overfit to the training distribution.
* **Sample Efficiency**: Theoretical analysis shows that when the embedding space has low intrinsic dimension and the performance function exhibits strong locality (similar queries yield similar model performance), kNN routing has lower sample complexity than parametric routing.

## Constraints & Limitations
* **Dependency on Support Set Quality**: Performance is highly dependent on having a representative and sufficiently dense support set.
* **Embedding Quality**: The effectiveness of the similarity metric relies heavily on the quality and domain-alignment of the underlying embedding space.
* **Fails to beat the Zero Router**: [[hu-2024-routerbench]] provides early empirical evidence that KNN routers, despite matching the best single LLM, do not significantly improve AIQ over the cost-free Zero Router (NDCH baseline) on most tasks — a finding later corroborated at larger scale by [[li-2025-predictive-routing]].

## See Also
* [[model-routing]] — Dynamic dispatching of queries across a pool of LLMs.
* [[dynamic-routing]] — Handling pools of candidate models that change at test time.
* [[llm-embeddings]] — Transforming prompt textual semantics into mathematical vectors.
* [[li-2025-predictive-routing]] — The original source page demonstrating that kNN can beat complex learned routers.
