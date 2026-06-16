---
type: entity
title: "RouterBench"
kind: product
tags: [llm-routing, benchmark, evaluation, open-source]
sources: [hu-2024-routerbench]
created: 2026-06-07
updated: 2026-06-07
---

# RouterBench

## Definition

**RouterBench** is the foundational open-source benchmark for evaluating multi-LLM routing systems, introduced by Hu et al. (2024) from UC Berkeley (Prof. Kurt Keutzer's lab). It provides **405,000+ pre-computed inference outcome records** across **11 LLMs** and **8 evaluation tasks**, paired with a theoretical cost-quality framework and the **AIQ** metric for fair router comparison.

RouterBench is the precursor to [[llmrouterbench]] (2026), which scales its approach to 33 models, 21 datasets, and 10 routing baselines.

## Dataset Coverage

| Task | Type | Inference |
|---|---|---|
| MMLU | Multiple choice (knowledge) | 5-shot |
| HellaSwag | Multiple choice (commonsense) | 5-shot |
| ARC-Challenge | Multiple choice (reasoning) | 5-shot |
| Winogrande | Multiple choice (commonsense) | 5-shot |
| GSM8k | Math word problems | 5-shot |
| MBPP | Code generation | 0-shot |
| MT-Bench | Multi-turn instruction following | 0-shot |
| RAG | Retrieval-augmented generation | 0-shot |

## Model Pool (11 LLMs)

| Model | Type |
|---|---|
| WizardLM-13B, Mistral-7B, Mixtral-8x7B, CodeLlama-34B, Yi-34B, Llama-70B | Open-source |
| GPT-3.5, GPT-4 | OpenAI proprietary |
| Claude Instant V1, Claude V1, Claude V2 | Anthropic proprietary |

## Key Theoretical Contributions

- **Cost-Quality (c–q) Plane**: Represents each router as a point $(c, q)$ enabling geometric comparison.
- **Non-Decreasing Convex Hull (NDCH)**: The Pareto frontier of routers; dominated points can be replaced by stochastic mixtures of superior ones.
- **Zero Router ($R_{zero}$)**: A strong, parameter-free baseline that uses only the NDCH of the LLM pool itself. Routers are only considered meaningful if they improve over $R_{zero}$.
- **AIQ Metric**: Area under the Interpolated-quality curve over a normalized cost range — a scalar for fair cross-router comparison.

## Key Empirical Findings

- LLM costs vary **2–5×** for comparable performance, confirming strong routing opportunity.
- The Oracle router achieves near-optimal quality at low cost; GPT-4 is rarely selected.
- Simple KNN and MLP predictive routers **match but don't significantly exceed** the Zero router (NDCH baseline) in AIQ.
- Cascading (non-predictive) routers **substantially outperform** the Zero router when the scoring function is reliable (error ≈ 0), but degrade with scoring errors.

## References
- Introduced in [[hu-2024-routerbench]].
- Succeeded and extended by [[llmrouterbench]] (Li 2026).
- Used as evaluation benchmark in [[jitkrittum-2026-universal-routing]].
