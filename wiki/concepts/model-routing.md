---
type: concept
title: "Model Routing"
tags: [llm-routing, dynamic-routing, cost-optimization]
sources: [chen-2025-irtnet, zhuang-2025-embedllm, jitkrittum-2026-universal-routing, chen-2023-frugalgpt, varangot-reille-2025-routing-survey, moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Model Routing

**Model Routing** (or LLM Routing) is the practice of dynamically selecting and dispatching user queries to the most appropriate Large Language Model (LLM) from a pool of candidate models. The primary objective is to balance performance (accuracy, quality) against cost (latency, API fees, compute resources) by utilizing smaller, cheaper models for simpler queries and invoking larger, more expensive proprietary models only when necessary.

## Core Objective
With the proliferation of LLMs ranging from small, specialized edge models (e.g., 1B–8B parameters) to giant proprietary APIs (e.g., GPT-4, Claude 3.5 Sonnet), executing all queries on the largest models is highly inefficient. Model routing frames this as an optimization problem:
$$\min_{m \in M} \text{Cost}(m) \quad \text{subject to} \quad \text{Quality}(m, q) \geq \tau$$
or maximizing expected quality under a budget constraint.

## Routing Architectures
Routers typically fall into several categories based on how they evaluate the suitability of a model for a given query:

1. **Classification-Based Routers**: A router (often a smaller model like a BERT variant or an MLP classifier) is trained directly on preference data to predict which candidate model will perform best on a given query (e.g., RouteLLM).
2. **Representation-Based Routers**: Represent both models and queries in a shared, low-dimensional embedding space.
   * **[[embedllm]]**: Uses matrix factorization to learn model and question embeddings, predicting correctness via the Hadamard product.
   * **[[irtnet]]**: Applies **Item Response Theory (IRT)** to model the correct response probability as $\sigma(\alpha_q^\top \theta_m - \beta_q)$ based on latent model abilities ($\theta_m$), query difficulty ($\beta_q$), and query discrimination ($\alpha_q$).
3. **Dynamic Routing**: Allowing the model pool to change at test time without retraining the router (e.g., **[[uniroute]]**).
4. **LLM Cascading**: Querying models sequentially (e.g., starting with a small model, verifying its output, and escalating to a larger model if the confidence is low).

## Downstream Benefits
* **Cost Reduction**: Can reduce API and inference costs by 50%–80% with minimal loss in quality compared to always using the largest model.
* **Latency Optimization**: Smaller models have much faster time-to-first-token and overall generation speeds.
* **Ensemble Intelligence**: Combines the specialized strengths of different models (e.g., math-tuned vs. code-tuned LLMs) to create a system that outperforms any single model.

## Survey Coverage

[[moslem-2026-routing-survey]] provides the most comprehensive taxonomy of multi-LLM routing as of 2026, organising methods across six paradigms:

- **Difficulty-aware**: heuristic or classifier-based complexity estimation (pre-generation)
- **Preference-aligned**: learning from human pairwise comparisons (e.g., [[routellm]])
- **Clustering-based**: unsupervised query grouping to specialist models (e.g., [[uniroute]])
- **Reinforcement learning**: bandit and policy-gradient routing (see [[rl-based-routing]])
- **Uncertainty-based**: post-generation confidence-triggered escalation (see [[uncertainty-based-routing]])
- **Cascading**: sequential multi-model escalation (see [[llm-cascade]], [[frugalgpt]])

The survey also introduces a three-dimensional design-space framework (When / What / How) that reveals how real-world systems combine multiple paradigms.

## Routing Taxonomy (Varangot-Reille 2025)
[[varangot-reille-2025-routing-survey]] provides the most comprehensive taxonomy of routing strategies. It organises the field along two orthogonal axes:

- **Timing axis**: [[pre-generation-routing]] (decide before any generation; lower latency) vs. [[post-generation-routing]] (evaluate actual outputs; higher latency but more accurate).
- **Implementation axis**: [[similarity-based-routing]] (kNN, clustering, preference), supervised (recommendation systems, domain classification, [[query-complexity-routing]]), RL-based, and generative.

The survey formalises routing as: `argmax_{M∈ℳ} s(q,M) s.t. C_M(q) ≤ B` — distinct from MoE (which operates internally) and from ensembles (which aggregate all outputs).

## See Also
* [[pre-generation-routing]] — Routing before any model generates a response.
* [[post-generation-routing]] — Cascade routing that evaluates actual outputs.
* [[similarity-based-routing]] — Routing based on query embedding similarity.
* [[query-complexity-routing]] — Estimating query difficulty to allocate the right model.
* [[dynamic-routing]] — Routing when the pool of candidate models is dynamic.
* [[llm-cascade]] — Sequential routing and confidence-based fallback.
* [[llm-embeddings]] — Representing LLM abilities as vectors for routing.
* [[rl-based-routing]] — RL and bandit methods for adaptive/online routing.
* [[uncertainty-based-routing]] — Post-generation confidence-based routing.
* [[knowledge-mindmap]] — Visual mindmap taxonomy organizing the LLM routing and selection landscape.

