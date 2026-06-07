---
type: source
title: "Rethinking Predictive LLM Routing: When Simple KNN Beats Complex Learned Routers"
authors:
  - "Yang Li"
url: "https://arxiv.org/abs/2505.12601"
raw: "raw/Li 2025 - Rethinking Predictive Modeling for LLM Routing When Simple kNN Beats Complex Learned Routers.pdf"
ingested: 2026-06-06
tags: [llm-routing, knn, non-parametric, benchmark]
entities: []
concepts:
  - knn-routing
  - model-routing
  - dynamic-routing
created: 2026-06-06
updated: 2026-06-06
graph:
  relationships:
    - predicate: contradicts
      object: source:zhuang-2025-embedllm
      source: li-2025-predictive-routing
      evidence: "In this work, we fundamentally rethink LLM routing by questioning whether such complexity is necessary. We show that a well-tuned k-Nearest Neighbors (kNN) approach not only matches but often outperforms state-of-the-art learned routers"
      confidence: high
      status: current
    - predicate: contradicts
      object: source:chen-2025-irtnet
      source: li-2025-predictive-routing
      evidence: "Our investigation yields a surprising finding: when carefully implemented and tuned, a simple kNN-based router not only matches but often outperforms a wide range of complex learned approaches across diverse routing scenarios"
      confidence: high
      status: current
---

# Rethinking Predictive LLM Routing: When Simple KNN Beats Complex Learned Routers

## Summary
[[li-2025-predictive-routing]] fundamentally rethinks the trend toward increasingly complex, parametric LLM routing architectures (such as graph neural networks, attention mechanisms, and multi-layered predictive models). The author, Yang Li, demonstrates that when carefully implemented and tuned, a simple, non-parametric **[[knn-routing]]** approach not only matches but often outperforms state-of-the-art learned routers across diverse text and vision-language benchmarks, while offering substantial advantages in computational efficiency, robustness to distribution shift, and test-time adaptability.

## Key Claims & Contributions
* **KNN Superiority**: A well-tuned $k$-Nearest Neighbors (kNN) router achieves competitive or superior performance to complex learned routers while requiring a fraction of the computational and training resources.
* **Locality in Embedding Space**: Model performance exhibits strong locality properties in embedding spaces (i.e., semantically similar queries benefit from similar models). Non-parametric methods exploit this to achieve lower sample complexity than parametric models.
* **Standardized Evaluation Benchmark Suite**: Introduces standardized text and vision-language (multi-modal) routing benchmarks to resolve the inconsistent evaluation setups in prior routing literature.
* **VLM Routing Benchmark**: Proposes the first multi-modal routing benchmark between Vision-Language Models (VLMs), built on vHELM, covering 5 diverse visual question-answering and reasoning datasets.
* **Theoretical Sample Complexity Bounds**: Shows that under the locality assumption and low intrinsic embedding dimension, the sample complexity of a kNN router is $\Theta( (C_{X,d}/\delta^d) \log(1/\alpha) )$, which is significantly lower than the $\Omega(L/\epsilon^2)$ bound for parametric routers.

## Methodology & Formulation
The paper formalizes predictive LLM routing by choosing between two classes of routers: direct selection policies (policy-gradient analog) and utility prediction models (Q-learning analog).

### Utility Prediction Framework
For a query $x$ and model pool $M = \{m_1, \dots, m_M\}$, the utility is:
$$m^* = \arg\max_{m \in M} [ s(x, m) - \lambda \cdot c(x, m) ]$$
where $s(x, m)$ is the performance score, $c(x, m)$ is the resource cost, and $\lambda$ is a cost-performance trade-off parameter.

### KNN Routing with Support Sets
Rather than training a parametric model to estimate $s(x, m)$ and $c(x, m)$ directly, the non-parametric kNN router retrieves the $k$ most semantically similar queries $N_k(x)$ from a historical support set $D_{\text{support}} = \{(x_i, m, s(x_i, m), c(x_i, m))\}$ using prompt embeddings:
$$\hat{s}(x, m) = \frac{1}{k} \sum_{i \in N_k(x)} s(x_i, m)$$
$$\hat{c}(x, m) = \frac{1}{k} \sum_{i \in N_k(x)} c(x_i, m)$$
Routing is then performed by selecting the model that maximizes the estimated utility.

## Evaluation Protocols
To compare routing formulations, the paper proposes two protocols:
1. **Utility Prediction Evaluation (Recommended)**: Evaluates routers by measuring the Area Under the Curve (AUC) of the non-decreasing convex hull in the cost-performance space as $\lambda$ varies. The maximum AUC score is normalized to 100.
2. **Selection-Based Evaluation**: Evaluates routers under three fixed cost-performance preference settings: low-cost, balanced, and high-performance. The author notes that selection-based evaluation has limitations, as high accuracy can simply reflect selecting expensive models rather than intelligent routing decisions.

### Benchmarks
* **Text-Based Benchmark**: Constructed from AlpacaEval, Open LLM Leaderboard v2, and HELM-Lite. Incorporates three model families with multiple variants per family. Costs are computed using actual API pricing based on input/output tokens.
* **Vision-Language Routing Benchmark**: Developed using vHELM, incorporating leading VLMs from Claude and OpenAI families across 5 visual question answering and visual reasoning datasets.

## Theoretical Analysis
The paper provides a sample complexity analysis to guarantee a regret bound $O(\epsilon(\delta))$:
* **kNN Router Sample Complexity**: $\Theta\left( \frac{C_{X,d}}{\delta^d} \log \frac{1}{\alpha} \right)$, where $d$ is the intrinsic dimension of the embedding space, and $\alpha$ is the failure probability.
* **Parametric Router Sample Complexity**: $\Omega\left( \frac{L}{\epsilon(\delta)^2} \right)$, where $L$ is the complexity of the parametric class.
* **Locality Effect**: If $\epsilon(\delta)$ (error difference) decreases rapidly with $\delta$ (semantic distance), and the intrinsic dimension $d$ of the embedding space is low, the kNN router requires quadratically fewer samples than parametric routers for high-accuracy requirements.

## Where this fits
* [[knn-routing]] — The non-parametric routing method investigated and championed in this work.
* [[model-routing]] — The general problem of dynamically selecting LLMs.
* [[dynamic-routing]] — kNN routers require zero retraining, making them ideally suited for dynamic model pools.
* [[zhuang-2025-embedllm]] — A parametric embedding baseline which claims matrix factorization outperforms KNN, which this paper challenges.
* [[chen-2025-irtnet]] — A parametric Item Response Theory routing baseline which this paper challenges.
