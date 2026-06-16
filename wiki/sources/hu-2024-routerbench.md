---
type: source
title: "RouterBench: A Benchmark for Multi-LLM Routing System"
authors: ["Qitian Hu", "Jacob Bieker", "Xiuyu Li", "Nan Jiang", "Benjamin Keigwin", "Gaurav Ranganath", "Kurt Keutzer", "Shriyash Kaustubh Upadhyay"]
url: "https://arxiv.org/abs/2403.12031"
raw: "raw/Hu 2024 - RouterBench A Benchmark for Multi-LLM Routing System.pdf"
ingested: 2026-06-07
created: 2026-06-07
updated: 2026-06-07
tags: [llm-routing, benchmark, cost-performance, evaluation]
entities: [routerbench]
concepts: [model-routing, pre-generation-routing, post-generation-routing, llm-cascade, knn-routing, oracle-gap]
---

# RouterBench: A Benchmark for Multi-LLM Routing System

## Overview

**RouterBench** (arXiv:2403.12031, ICML 2024 workshop) is the **foundational benchmark** for systematic evaluation of multi-LLM routing systems, developed at UC Berkeley (Prof. Kurt Keutzer's lab). Prior to this work, no standardized evaluation framework existed for comparing routing strategies across a common testbed.

The paper makes three primary contributions:
1. **RouterBench dataset** — 405,000+ inference outcome records across 11 LLMs and 8 tasks/datasets, extensible to new models and tasks.
2. **Theoretical evaluation framework** — A cost-quality (c–q) plane formalism using linear interpolation, extrapolation, non-decreasing convex hulls, and the **AIQ** (Area under Interpolated-quality curve) scalar metric to compare routers on a fair basis.
3. **Empirical evaluation** — Comparative analysis of predictive (KNN, MLP) and non-predictive (cascading) router designs across all benchmark tasks.

## Dataset

[[routerbench]] aggregates inference outcomes across:
- **11 LLMs**: WizardLM-13B, Mistral-7B, Mixtral-8x7B, CodeLlama-34B, Yi-34B, GPT-3.5, Claude Instant V1, Llama-70B, Claude V1, Claude V2, GPT-4.
- **8 evaluation tasks**: MMLU, HellaSwag, ARC-Challenge, Winogrande, GSM8k, MBPP, MT-Bench, RAG.
- **405,000+ records**, each with: sample id, model name, prompt, model response, performance (binary), cost (dollars), true label.
- **Cost model**: API pricing for proprietary models; Together AI pricing for open-source models.
- **Inference settings**: 5-shot for MMLU/HellaSwag/GSM8K/ARC/Winogrande; 0-shot for MBPP/MT-Bench/RAG. GPT-4 used as judge for open-ended tasks.

## Theoretical Framework

The paper introduces a rigorous mathematical framework for comparing heterogeneous routers:

- **Cost-Quality (c–q) Plane**: Each router is characterized by its expected cost $c_{R_\theta}$ and expected performance $q_{R_\theta}$ across a dataset, plotted as a point.
- **Linear Interpolation**: Two routers $R_{\theta_1}$, $R_{\theta_2}$ can be combined stochastically to achieve any cost-quality tradeoff on the line segment between them.
- **Non-Decreasing Convex Hull (NDCH)**: The Pareto-optimal frontier in the c–q plane; points below/right of the hull are dominated and can be replaced by superior affine combinations.
- **Zero Router ($R_{zero}$)**: A baseline router using only the NDCH of the LLM pool itself (no learned component) — routes probabilistically to maximize expected quality at a given cost budget. A router is only considered significant if it outperforms $R_{zero}$.
- **AIQ (Area under Interpolated-Quality curve)**: A scalar metric integrating performance across a normalized cost range $[c_{min}, c_{max}]$, enabling fair scalar comparison between routing systems with different operating cost ranges.

## Router Types Evaluated

### Predictive Routers (pre-generation)
Select the optimal LLM without generating outputs first.
- **KNN router**: Estimates per-sample model performance by averaging correctness of $k$ nearest neighbors in embedding space. Best results with $k=40$, `all-MiniLM-L12-v2` embeddings.
- **MLP router**: Two-hidden-layer MLP (100 neurons/layer, ReLU) predicting performance score per model. Trained on 70% of each task's data; evaluated on 30%.

### Non-Predictive Routers (post-generation / cascade)
Generate outputs first, then select based on scoring.
- **Cascading router**: Sequences LLMs from cheapest to most expensive; uses a scoring function $g$ with threshold $t$ to decide when to escalate. Parameterized by total cost budget $T$ and error rate $\epsilon$.
- **Overgenerate-and-rerank**: Generates all outputs from all LLMs and selects the best per a reward function (high cost, shown for reference only).

## Key Results

- **Oracle potential**: The Oracle router achieves near-optimal performance at low cost — confirming substantial routing opportunity. GPT-4 is rarely selected by the Oracle, as cheaper models suffice for most queries.
- **Routing cost savings**: Monetary costs of LLM services vary by **2–5×** for comparable performance levels across benchmark tasks.
- **Predictive routers ≈ Zero router**: KNN and MLP predictive routers achieve performance comparable to the best individual LLM at lower cost, but **do not significantly outperform the Zero router (NDCH baseline)** in AIQ across most tasks.
- **Cascading routers beat Zero router**: With a near-perfect scoring function (error ≈ 0), cascading routers achieve substantially higher AIQ (e.g., 0.901 vs 0.763 on MMLU). Performance degrades gracefully as scoring error $\epsilon$ increases.
- **Over-alignment issue**: Some models (notably Claude 2) frequently refuse to answer — a problem the benchmark explicitly documents and attributes to over-alignment fine-tuning.
- **Out-of-domain generalization**: Routers trained on held-out tasks show degraded but non-zero transfer, suggesting some generalization potential.

## Where this fits

- **Foundational prior work to [[llmrouterbench]]**: LLMRouterBench (2026) explicitly builds on RouterBench, scaling the evaluation from 8 tasks/11 models to 21 datasets/33 models with 10 baselines.
- **[[knn-routing]]**: RouterBench provides one of the earliest large-scale empirical evaluations of KNN-based routing, establishing that simple KNN approaches match but don't substantially beat the Zero router baseline.
- **[[llm-cascade]]**: The cascading router experiments establish the empirical effectiveness of cascade architectures when the scoring function is reliable, complementing [[frugalgpt]]'s theoretical framing.
- **[[oracle-gap]]**: The Oracle results underscore the existence of a large gap between the theoretical best router and any practical implementation — a gap subsequently characterized more rigorously in [[li-2026-llmrouterbench]].
- **[[pre-generation-routing]]** and **[[post-generation-routing]]**: RouterBench is one of the first works to systematically compare these two paradigms on common tasks.
- **Referenced in [[jitkrittum-2026-universal-routing]]**: Used as an evaluation benchmark for UniRoute's dynamic pool routing experiments.
