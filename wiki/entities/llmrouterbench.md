---
type: entity
title: "LLMRouterBench"
kind: benchmark
tags: [llm-routing, benchmark, evaluation-framework, open-source]
sources: [li-2026-llmrouterbench, hu-2024-routerbench]
created: 2026-06-06
updated: 2026-06-06
---

# LLMRouterBench

## Definition
LLMRouterBench is an open-source, large-scale benchmarking suite and unified framework for evaluating and developing Large Language Model (LLM) routing systems. It aggregates over 400,000 structured inference instances from 21 datasets across 33 open-source and proprietary models, providing standardized environments and metrics for both performance-oriented and performance-cost tradeoff routing.

## Architecture & Core Modules
The framework is designed with a modular structure consisting of three primary components:
1. **Collector**: Standardizes interactions with candidate LLMs, managing cached responses, execution retries, and API/token cost accounting.
2. **Evaluator**: Implements strict, dataset-specific evaluation metrics to determine correct answers for various tasks.
3. **Adaptor**: Transforms standardized outputs into algorithm-specific input formats (such as prompt texts or model confidence scores) for the downstream routers while enforcing reproducible dataset splits.

## Standardized Environments
LLMRouterBench supports two distinct routing environments:
* **Performance-Oriented Pool**: Consists of 20 lightweight (~7B parameter) open-source LLMs (e.g., Qwen3-8B, DS-Qwen3) designed to assess the router's ability to exploit complementary strengths between similar-scale models.
* **Performance-Cost Pool**: Consists of 13 flagship and proprietary models (e.g., GPT-5, Gemini-2.5 Pro, Claude-4.1-Opus, DeepSeek-R1) to evaluate routers under realistic cost, speed, and quality constraints.

## Integrated Router Baselines
The benchmark integrates 10 representative routing baselines:
* **Performance-Oriented**: `RouterDC`, `MODEL-SAT`, `EmbedLLM`, `Avengers`, and `HybridLLM`.
* **Performance-Cost Tradeoff**: `RouteLLM`, `GraphRouter`, `FrugalGPT`, `Avengers-Pro`, and commercial auto-routers (represented by `OpenRouter`).

## Key Benchmarking Insights
Systematic re-evaluation using LLMRouterBench revealed several key insights:
* **The Oracle Gap & Recall Failures**: All contemporary routers fall significantly short of the Oracle ceiling. This is primarily caused by *model-recall failures*—where a query can only be solved by a single model in the pool, but the router fails to select it.
* **Marginal Embedding Impact**: The choice of query embedding model (size, provider, quality) has little to no impact on routing accuracy.
* **Curation over Ensemble Scaling**: Expanding the model pool has diminishing returns. Curating a small, highly complementary subset of models yields better performance-cost trade-offs than scaling the ensemble size.
* **Baseline Competitiveness**: Many recent routing algorithms show indistinguishable performance from one another under a unified evaluation, and some commercial routers fail to outperform a simple Best Single model baseline.

## Repository
The benchmark codebase is available at [github.com/ynulihao/LLMRouterBench](https://github.com/ynulihao/LLMRouterBench).

## References
* Introduced in [[li-2026-llmrouterbench]].
* Direct successor to [[routerbench]] (Hu et al. 2024), which established the foundational c–q plane framework and AIQ metric on 11 models × 8 tasks.
