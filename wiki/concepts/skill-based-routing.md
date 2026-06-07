---
type: concept
title: "Skill-Based Routing"
tags: [llm-routing, methodology, capability-matching, interpretability]
sources: [okokamoto-2026-trust-routing]
created: 2026-06-06
updated: 2026-06-06
graph:
  relationships:
    - predicate: depends_on
      object: concept:model-routing
      source: okokamoto-2026-trust-routing
      evidence: "recommends optimal LLM selection for tasks through interpretable skill-based model selection"
      confidence: high
      status: current
---

# Skill-Based Routing

**Skill-Based Routing** (or Skill-Based LLM Selection) is an approach to [[model-routing]] that matches the granular capabilities required by a task with the demonstrated capability profiles of candidate models. Unlike black-box routing frameworks that predict performance purely from raw prompt texts or aggregate metrics, skill-based routing maps tasks and models to a structured, human-interpretable skill space.

## Key Motivations

1.  **Transparency & Trust**: Traditional routers (e.g., [[routellm]]) operate as classifiers predicting a single routing score or binary target. They do not explain why a model is chosen. Skill-based routing offers natural-language rationales and auditable performance profiles.
2.  **Granularity**: Standard benchmark scores average out specific model strengths and weaknesses. A model might have high average accuracy but fail at specific skills like temporal reasoning or formatting, which could be critical for a given task.
3.  **Generalization**: High-level skills (e.g., text extraction, arithmetic, logical reasoning) generalize across tasks. Representing new tasks as vectors of required skills enables zero-shot routing without retraining routers.

## General Architecture

A typical skill-based routing framework involves:

1.  **Capability Profiling**: Evaluating models at an instance level to identify strengths (demonstrated skills) and weaknesses (lacking skills). A common approach is using a critic LLM to analyze inputs, reference answers, and model rationales (as seen in [[bella]]).
2.  **Clustering & Labeling**: Canonicalizing unstructured feedback from critics into a reduced, stable taxonomy of skills using embeddings and clustering algorithms.
3.  **Alignment & Selection**: Matching the task's required skills with model proficiencies. This is typically formulated as an optimization problem where model selection maximizes quality under budget/latency constraints:
    $$\max_{m \in M_{\text{capable}}} \text{Expected\_Performance}(m) \quad \text{s.t.} \quad \text{Cost}(m) \leq B$$

## Related Paradigms

*   [[model-routing]] — The parent concept of dispatching queries dynamically.
*   [[knn-routing]] — Matches queries based on embedding similarity rather than explicit semantic skill proficiencies.
*   [[llm-embeddings]] — Low-rank latent representations of model capabilities (e.g., Item Response Theory) are mathematical abstractions of capability, whereas skill-based routing maps to human-readable labels.

## Implementations

*   [[bella]] — Budget-Efficient LLM Selection via Automated skill-profiling, which builds capability matrices to execute cost-constrained, explainable LLM selection.
