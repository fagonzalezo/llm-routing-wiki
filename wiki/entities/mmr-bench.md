---
type: entity
title: "MMR-Bench"
kind: product
tags: [llm-routing, multimodal-llm, benchmark, evaluation]
sources: [ma-2026-mmr-bench]
created: 2026-06-06
updated: 2026-06-06
---

# MMR-Bench

## Definition
**MMR-Bench** is a comprehensive, budget-aware offline evaluation benchmark designed specifically for routing across a heterogeneous pool of Multimodal Large Language Models (MLLMs). It standardizes the evaluation of model-selection policies on mixed vision-language workloads under fixed candidate sets and unified cost models.

## Core Design

### 1. Offline Evaluation Sandbox
Rather than requiring live model inference, MMR-Bench operates as an offline evaluation environment. It contains:
* Over **100,000 pre-computed query-model pairs** mapping inputs to model outputs.
* Task-specific utility scores (e.g., exact match accuracy).
* Normalized inference costs computed under a unified pricing scheme.
This structure ensures deterministic, zero-cost, and reproducible evaluations of new routing policies.

### 2. Modality Availability Vector
To test routers under varying input constraints, each sample $i$ is associated with a modality availability vector $m_i = (m_i^{\text{text}}, m_i^{\text{img}})$, where $m_i^r \in \{0, 1\}$. This allows testing:
* **Text-Only Routing**: Using only the text prompt embedding $\phi^{\text{text}}(x_i)$.
* **Image-Only Routing**: Using only the image embedding $\phi^{\text{img}}(x_i)$.
* **Multimodal Routing**: Using joint text-image embeddings $\phi^{\text{mm}}(x_i)$.

### 3. Broad Scenario Coverage
MMR-Bench covers 100k+ samples compiled from several vision-language datasets:
* **Document-Centric OCR & Layouts**: OCRBench, SEED-Bench v2 Plus.
* **General VQA & Grounding**: MMStar, RealWorldQA.
* **Multimodal Mathematical Reasoning**: MathVerse, MathVista, MathVision.

### 4. Candidate Model Pool
The candidate pool consists of heterogeneous closed-source and open-weight models, enabling testing of cost-accuracy boundaries across:
* **Frontier Models**: GPT-5, Gemini 2.5 Pro, Gemini 2.5 Flash, Claude 3.7V.
* **Open-Weight Models**: Qwen2.5-VL (3B, 7B, 72B), InternVL3 (78B).

## Key Applications
* **Calibration & Modality Analysis**: Used to show that text-only or image-only routers suffer from severe miscalibration. For instance, text-only routers overestimate cheaper models on simple text prompts that contain complex visual details (like text-in-image).
* **Cost-Efficiency Optimization**: Evaluates how routers trace the cost-accuracy trade-off frontier. Policies evaluated on MMR-Bench demonstrate that multimodal routing matches the performance of frontier models at roughly 33% of their deployment cost.
* **Zero-Shot Transferability**: Serves as a testbed for checking if routing policies generalize to unseen tasks, candidate models, or text-only environments.

## References
* Introduced in [[ma-2026-mmr-bench]].
