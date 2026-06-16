---
type: source
title: "Universal Model Routing for Efficient LLM Inference"
authors:
  - "Wittawat Jitkrittum"
  - "Harikrishna Narasimhan"
  - "Ankit Singh Rawat"
  - "Jeevesh Juneja"
  - "Congchao Wang"
  - "Zifeng Wang"
  - "Alec Go"
  - "Chen-Yu Lee"
  - "Pradeep Shenoy"
  - "Rina Panigrahy"
  - "Aditya Krishna Menon"
  - "Sanjiv Kumar"
url: ""
raw: "raw/Jitkrittum 2026 - Universal Model Routing for Efficient LLM Inference.pdf"
ingested: 2026-06-06
tags: [llm-routing, dynamic-routing, cost-efficiency]
entities: [uniroute]
concepts: [dynamic-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Universal Model Routing for Efficient LLM Inference

In this paper, Jitkrittum et al. address the challenge of **dynamic model routing**, where the pool of candidate LLMs changes at test time (e.g., when new models are released or old ones are deprecated). They propose **[[uniroute]]**, a novel routing framework that represents both prompts and LLMs as feature vectors to generalize to unseen models without retraining.

## Core Contributions & Methodology

### 1. Dynamic Routing Setup
Traditional ("static") model routers learn parameters for a fixed pool of LLMs. Adding or removing models requires costly retraining and redeployment. In contrast, the dynamic routing setting allows the test-time LLM pool $H_{te}$ to be disjoint from the training pool $H_{tr}$. 

The authors prove that the Bayes-optimal routing rule for a dynamic pool decomposes across individual models, choosing the model $h$ that minimizes:
$$r^*(x, H) = \operatorname{argmin}_{m} [ P(y \neq h^{(m)}(x) | x) + \lambda \cdot c(h^{(m)}) ]$$
where $c(h)$ is the cost of the model and $\lambda \geq 0$ is a trade-off parameter.

### 2. UniRoute Architecture
UniRoute parameterizes the predicted error using a bilinear form:
$$\gamma_{uni}(x, h) = \Phi(x)^\top \Psi(h)$$
- **Prompt Representation $\Phi(x) \in \mathbb{R}^K$**: Captures the characteristics of the prompt.
- **LLM Representation $\Psi(h) \in \mathbb{R}^K$**: Formulated as the prediction error vector on a small, labeled validation set $S_{val}$ (akin to semantic output codes for zero-shot classification):
  $$\Psi(h) = F([1(y^{(j)} \neq h(x^{(j)}))]_{j \in [N_{val}]})$$

### 3. Instantiations of UniRoute
The authors propose two cluster-based instantiations of the bilinear model:
- **UniRoute (K-Means)** (Unsupervised Clustering): Centroids are found by clustering training prompt embeddings from $S_{tr}$ (no labels required). Validation prompts in $S_{val}$ are assigned to these clusters. For a new test model $h$, $\Psi(h)$ is computed as the vector of its average errors on the validation prompts in each cluster.
- **UniRoute (LearnedMap)** (Supervised Clustering): Learns a parameterized cluster assignment map $\Phi_{clust}(x; \theta) \propto \exp(\theta_k^\top \phi(x))$ where $\phi(x)$ is a general prompt embedding. The parameter $\theta$ is optimized on the training set $S_{tr}$ using correctness profiles of the training LLMs to minimize the cross-entropy log loss.

## Theoretical Analysis

The paper establishes an excess risk bound (Proposition 2) indicating that the quality gap between cluster-based routing and the Bayes-optimal router is bounded by the discrepancy between the per-cluster and per-prompt errors. This provides a theoretical guarantee for representing LLM capabilities via coarse-grained cluster-level performance.

## Empirical Findings

The authors evaluate UniRoute across several benchmarks, including EmbedLLM, [[routerbench]], SPROUT o3-mini, and Headlines:
- **Zero-Shot Generalization**: UniRoute effectively routes queries among 30+ unseen test LLMs without any router retraining.
- **Performance**: On EmbedLLM, UniRoute (LearnedMap) achieves a Quality-Neutral Cost (QNC) of **33.1%** (meaning it matches the best model's accuracy at 33.1% of its cost), outperforming ZeroRouter (87.5%), K-NN (45.9%), and retrained static MLPs (35.9%).
- **Data Efficiency**: UniRoute remains effective even with small validation sets (e.g., $N_{val} \approx 400$ samples), whereas static MLPs and matrix factorization methods overfit when retrained on such small validation samples.
- **Comparison to LLM Bandit**: In comparative evaluations against LLM Bandit (a reinforcement learning approach), UniRoute achieves the same accuracy as the largest model in the pool (Qwen2.5-72B-Instruct) at **80.2%** of its cost, compared to $>90\%$ QNC for LLM Bandit.

## Limitations

- **Performance in Static Settings**: In a fully static pool environment, UniRoute is not guaranteed to outperform custom-tailored static routers.
- **Coreset Selection**: The validation set $S_{val}$ is currently selected randomly; optimizing for a diverse prompt coreset could further improve LLM representation efficiency.

## Where this fits
- [[uniroute]] — The routing system introduced in this paper.
- [[dynamic-routing]] — The core concept of routing with a changing pool of LLMs.
