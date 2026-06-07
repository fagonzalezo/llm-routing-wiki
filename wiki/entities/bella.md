---
type: entity
kind: product
title: "BELLA"
tags: [llm-routing, framework, skill-profiling, interpretability]
sources: [okokamoto-2026-trust-routing]
created: 2026-06-06
updated: 2026-06-06
graph:
  node_type: product
  relationships:
    - predicate: depends_on
      object: concept:skill-based-routing
      source: okokamoto-2026-trust-routing
      evidence: "We introduce BELLA(Budget-Efficient LLM Selection via Automated skill-profiling), a framework that recommends optimal LLM selection for tasks through interpretable skill-based model selection."
      confidence: high
      status: current
---

# BELLA

**BELLA** (Budget-Efficient LLM Selection via Automated skill-profiling) is a budget-aware, transparent model routing and selection framework introduced by Okamoto et al. in 2026. It decomposes model performance into modular, human-interpretable skill profiles, matching them to task requirements to select the most cost-effective model that satisfies capability and resource constraints.

## Core Architecture

BELLA consists of four stages:

1.  **Benchmarking**: Evaluating candidate LLMs on tasks to collect accuracy/F1 metrics, operational costs (latency, API fees), and model outputs (including reasoning traces).
2.  **Skill Profiling via Critic LLM**: Using a strong critic model to review instance inputs, outputs, and ground-truth answers to extract demonstrated strengths, missing weaknesses, and their criticality, without relying on predefined taxonomies.
3.  **Skill Clustering**: Canonicalizing raw critic descriptions using sentence embeddings (Sentence Transformers) and clustering (K-Means / hierarchical clustering) to produce a consistent skill taxonomy and encode models/tasks into structured matrices.
4.  **Skill-aware Model Selection**: Filtering the model pool for those meeting capability thresholds, then optimizing to select the model that maximizes estimated performance within the budget constraint.

## Capability Matrix Representations

BELLA represents the routing problem using three structured components:
*   **Model Capability Matrix ($C \in [0,1]^{M \times S}$)**: Represents model $m$'s proficiency at skill $s$.
*   **Task Requirement Matrix ($R \in \{0,1\}^{T \times S}$)**: Identifies whether task $t$ requires skill $s$.
*   **Cost Vector ($c \in \mathbb{R}^M$)**: Represents model operational costs.

These matrices support several recommendation paradigms, including similarity-based cosine retrieval, non-negative matrix factorization collaborative filtering, and supervised prediction of performance scores.

## Where this fits

*   [[okokamoto-2026-trust-routing]] — The original research paper proposing BELLA.
*   [[skill-based-routing]] — The underlying concept of using granular skill profiles for routing.
*   [[model-routing]] — The general practice of dynamic query dispatching between LLMs.
