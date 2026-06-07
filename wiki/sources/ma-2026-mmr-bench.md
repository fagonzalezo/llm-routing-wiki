---
type: source
title: "MMR-Bench: A Comprehensive Benchmark for Multimodal LLM Routing"
authors: ["Haoxuan Ma", "Guannan Lai", "Han-Jia Ye"]
url: "https://arxiv.org/abs/2601.17814"
raw: "raw/Ma 2026 - MMR-Bench A Comprehensive Benchmark for Multimodal LLM Routing.pdf"
ingested: 2026-06-06
tags: [llm-routing, multimodal-llm, model-selection, benchmark]
entities: [mmr-bench]
concepts: [multimodal-llm-routing, model-routing]
created: 2026-06-06
updated: 2026-06-06
---

# MMR-Bench: A Comprehensive Benchmark for Multimodal LLM Routing

## Summary
**MMR-Bench** is a unified, budget-aware offline benchmark designed to isolate the problem of Multimodal Large Language Model (MLLM) routing. Due to differences in architecture, alignment strategies, and training data, no single MLLM is uniformly superior across tasks. Standardizing routing in multimodal settings is challenging due to the modality gap, model heterogeneity across the MLLM zoo, and multi-dimensional cost structures. MMR-Bench addresses this by providing pre-computed outputs, task-specific utilities, and normalized inference costs for over 100,000 query-model pairs across a diverse suite of vision-language benchmarks and candidate models. The authors demonstrate that incorporating multimodal cues (joint text-image representations) significantly improves routing calibration over text-only or image-only baselines. Under budget constraints, the routed system matches or exceeds the accuracy of the strongest candidate model at approximately 33% of its cost.

## Key Claims and Findings
* **Necessity of Multimodal Cues**: Unimodal routers (text-only or image-only) are miscalibrated on vision-governed inputs, such as text-in-image queries, charts, low-resolution crops, or cluttered scenes. Text-only routers tend to overestimate the capability of cheaper models when the text prompt is simple but the visual scene is complex. Joint multimodal embeddings successfully resolve these failures.
* **Cost-Accuracy Frontier Optimization**: In mixed workloads, multimodal routing achieves a strictly superior cost-accuracy trade-off. It achieves a Quality-Neutral Cost (QNC) of less than 1.0 on most tasks, matching the performance of the strongest available models (such as GPT-5) at a fraction of their cost (95% cost savings on simple OCR and overall matched performance at ~33% cost).
* **Zero-Shot Generalization**: Routing policies trained on a subset of models and tasks generalize zero-shot to unseen datasets and transfer effectively to text-only LLM routing benchmarks without retuning.

## Methodology
The benchmark formulates the MLLM routing problem mathematically:
* **Modality Availability**: Let $m_i = (m_i^{\text{text}}, m_i^{\text{img}})$ where $m_i^r \in \{0, 1\}$ denotes whether a modality is active.
* **Score Maximization**: For each query $i$ and candidate model $j \in \{1, \dots, K\}$, the router selects the model that maximizes:
  $$S_{i,j} = u_{i,j} - \lambda c_{i,j}$$
  where $u_{i,j}$ represents the utility, $c_{i,j}$ represents the normalized cost, and $\lambda \geq 0$ is a tunable parameter controlling the cost-accuracy trade-off.
* **Offline Evaluation Environment**: Standardizes evaluation using pre-computed model outputs and utilities, removing the need to run costly MLLM inference during router development.
* **Dataset Composition**: Covers three core scenarios:
  1. *Document-centric OCR & understanding*: OCRBench and SEED-Bench v2 Plus.
  2. *General VQA & grounding*: MMStar and RealWorldQA.
  3. *Multimodal math & diagram reasoning*: MathVerse, MathVista, and MathVision.
* **Evaluated Routers**: Includes KMeans (unsupervised), MLPMF (Multilayer Perceptron Matrix Factorization), LinearMF, KNN, and Oracle.

## Conclusions
The authors conclude that instance-wise model selection via multimodal routing is crucial for deploying heterogeneous MLLMs efficiently. They show that joint text-image signals are necessary to construct accurate routing boundaries, making MMR-Bench a foundational tool for cost-aware multimodal system deployment.

## Where This Fits
* **Multimodal Extension**: Extends the concept of [[model-routing]] and [[dynamic-routing]] from text-only models to MLLMs by bridging the modality gap.
* **Benchmarking**: Serves as a multimodal counterpart to text-only benchmarks like [[routereval]], [[llmrouterbench]], and [[embedllm]].
* **Routing Algorithms**: Validates that matrix factorization (similar to [[embedllm]]'s concepts) and non-parametric estimators like [[knn-routing]] perform well in multimodal environments.
