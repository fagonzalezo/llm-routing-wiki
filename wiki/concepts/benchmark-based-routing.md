---
type: concept
title: "Benchmark-Based Routing"
tags: [llm-routing, benchmark, methodology, ood-generalization, binary-classification]
sources: [shnitzer-2024-benchmark-routing]
created: 2026-06-06
updated: 2026-06-06
graph:
  relationships:
    - predicate: depends_on
      object: concept:model-routing
      source: shnitzer-2024-benchmark-routing
      evidence: "We propose a new formulation for the problem, in which benchmark datasets are repurposed to learn a 'router' model for LLM selection"
      confidence: high
      status: current
    - predicate: depends_on
      object: concept:knn-routing
      source: shnitzer-2024-benchmark-routing
      evidence: "we embed all inputs with a sentence transformer and use a k-nearest neighbors classifier as the correctness predictors"
      confidence: high
      status: current
---

# Benchmark-Based Routing

**Benchmark-Based Routing** is an approach to [[model-routing]] where the training signal for a router comes not from query-level human preference labels or real-time generation scoring, but from the **byproducts of existing benchmark evaluations** — specifically, the per-sample correctness records generated when LLMs are evaluated against standard benchmarks like HELM or MMLU.

## Core Idea

When a benchmark evaluates $M$ LLMs across $D$ tasks and $N$ samples, it produces a matrix of per-sample correctness signals $y(x^d_i, m) \in \{0, 1\}$ for each input $x$, model $m$, and task $d$. Standard benchmarking discards this information after aggregating to a single leaderboard score. Benchmark-based routing recycles it: these correctness signals become supervision labels for training a family of classifiers $\{g_m\}_{m=1}^M$, where $g_m(x) \approx P(\text{LLM } m \text{ answers } x \text{ correctly})$.

For a new, unseen task with inputs $\{x_i\}$, the router scores each candidate LLM and selects the one with the highest predicted aggregate correctness.

## Key Distinction from Other Routing Paradigms

| Paradigm | Training Signal | Test-Time Cost |
|---|---|---|
| Benchmark-based (this) | Benchmark eval byproducts | Input-only; 1 LLM call |
| Preference-based ([[routellm]]) | Human preference labels | Input-only; 1 LLM call |
| Generation-scoring ([[frugalgpt]]) | Ground-truth answers | All candidates must generate |
| Query-kNN ([[knn-routing]]) | Per-query historical outcomes | Input-only; 1 LLM call |

The key advantage over generation-scoring approaches is **efficiency at test time**: no generation from unchosen models is required. The key advantage over query-kNN is that training data comes from standardized public benchmarks rather than deployment history — enabling routing before any production traffic has accumulated.

## Routing Scores

Shnitzer et al. (2024) propose three score variants for aggregating per-sample correctness predictions into a model-level routing decision:

- **S1** (raw probability): $S_1(m, d') = \frac{1}{n}\sum_i g_m(x_i)$. Directly averages predicted probabilities; sensitive to OOD miscalibration.
- **S2** (thresholded): $S_2(m, d') = \frac{1}{n}\sum_i \mathbb{1}[g_m(x_i) > t]$. Thresholding makes it more robust when calibration degrades OOD.
- **S3** (OOD-aware): Modulates S2 by an estimated OOD confidence $p(d', m)$ — the probability that the correctness predictor makes the right call on the new task. Derived from the similarity of the new task's embedding distribution to training benchmark tasks; connected to meta-learning theory. Consistently best empirically.

## Implementation

The simplest realization (Shnitzer et al. 2024) uses:
1. **Sentence-transformer embeddings** to encode all benchmark inputs and new task inputs into a shared vector space.
2. **kNN classifiers** ($g_m$) — non-parametric, require no hyperparameter tuning, handle complex multi-task decision boundaries via locality.
3. **Task-distribution similarity** for S3's OOD confidence, computed in embedding space.

More expressive variants replace kNN with learned model representations: [[embedllm]] uses matrix factorization to learn compact model-and-query embeddings for correctness prediction; [[irtnet]] applies Item Response Theory (IRT) to parametrically model difficulty and model ability from benchmark data.

## Strengths

- **Data efficiency**: No new LLM inference needed for training — benchmark evaluation byproducts are already available.
- **Multi-task generalization**: Training across many benchmark tasks and domains encourages learning generalizable model strength profiles.
- **Input-only at test time**: Only the chosen model is invoked, keeping inference cost minimal.
- **Theoretically grounded OOD correction**: S3's derivation draws on PAC-Bayes and meta-learning, providing formal intuition for why it outperforms S1/S2.

## Limitations

- **Benchmark coverage requirement**: Candidate models must have been evaluated on the available benchmarks. Cold-start models (not in any benchmark) cannot be routed.
- **OOD degradation**: Correctness predictors lose accuracy on tasks semantically far from the training benchmark distribution. S3 partially mitigates this but does not eliminate it.
- **Accuracy-only objective**: The Shnitzer et al. formulation optimizes correctness without explicit cost modeling — cost-performance trade-offs require extensions.
- **Benchmark staleness**: If a new task type is under-represented in available benchmarks, the routing signal may be weak.

## See Also

- [[model-routing]] — The overarching paradigm; benchmark-based routing is one of several training strategies.
- [[knn-routing]] — Non-parametric backbone used by Shnitzer et al. for correctness prediction.
- [[embedllm]] — More expressive correctness-prediction approach using learned model embeddings.
- [[irtnet]] — IRT-based correctness modeling from benchmark data.
- [[routellm]] — Contrasting approach using human preference data instead of benchmark byproducts.
- [[frugalgpt]] — Contrasting approach requiring test-time generation from all candidates.
- [[shnitzer-2024-benchmark-routing]] — Original source proposing and evaluating this concept.
