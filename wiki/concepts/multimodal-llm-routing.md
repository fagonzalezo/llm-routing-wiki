---
type: concept
title: "Multimodal LLM Routing"
tags: [llm-routing, multimodal-llm, cost-optimization]
sources: [ma-2026-mmr-bench, moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Multimodal LLM Routing

**Multimodal LLM Routing** (or Multimodal Model Selection) is the practice of dynamically dispatching multimodal queries (e.g., text, images, video) to the most appropriate Multimodal Large Language Model (MLLM) from a pool of candidates. It extends traditional text-only [[model-routing]] to handle heterogeneous inputs while optimization aims to balance performance against inference costs, token budgets, and latency.

## Core Objective and Formulation
In real-world settings, multimodal workloads are highly diverse, ranging from simple OCR to complex visual mathematics. Since MLLMs vary significantly in capability and cost (the "MLLM Zoo"), using a single model for all queries is inefficient. 

Formally, a multimodal router selects a model index $j^*$ for query $i$ by maximizing a cost-adjusted utility score:
$$j^* = \operatorname{argmax}_{j} (u_{i,j} - \lambda c_{i,j})$$
where $u_{i,j}$ is the predicted utility of model $j$ on query $i$, $c_{i,j}$ is its normalized inference cost, and $\lambda \geq 0$ is a tunable parameter managing the trade-off.

To handle cases where some input modalities are missing, a modality availability vector $m_i = (m_i^{\text{text}}, m_i^{\text{img}})$ is introduced, dictating which features the router can observe.

## Unique Challenges

1. **Modality Gap**: Routers must process and align heterogeneous inputs (e.g., text prompts and high-resolution images) to assess query difficulty.
2. **Visual Miscalibration (Unimodal Failure)**: Unimodal routers (text-only or image-only) struggle to locate accurate decision boundaries:
   * *Text-only routers* tend to overestimate the accuracy of cheaper models on queries with simple text but high visual complexity (e.g., text-in-image or cluttered scenes).
   * *Image-only routers* fail when the visual input is simple but the prompt demands complex reasoning, calculation, or multi-step logic.
3. **Multi-dimensional Cost Modeling**: Cost computation is complex because MLLMs charge differently based on input resolution, image-to-token projection methods, and modality combinations.

## Fused Representation Strategies
Effective multimodal routing relies on joint text-image feature extraction. Common approaches include:
* **Late Fusion**: Extracting text embeddings (e.g., via Sentence-BERT) and image embeddings (e.g., via CLIP) separately and concatenating them.
* **Early Fusion / Cross-Modal Embedding**: Passing joint prompts through unified multimodal encoders to capture spatial-textual relationships before making routing decisions.

Empirical studies on [[mmr-bench]] confirm that routers using fused representations achieve a strictly better cost-accuracy frontier than unimodal alternatives. Under optimized configurations, a routed system can achieve the accuracy of the strongest available proprietary models at roughly 33% of their deployment cost.

## See Also
* [[model-routing]] — Core dynamic routing concepts for text-only models.
* [[mmr-bench]] — Standardised benchmark for multimodal LLM routing.
* [[knn-routing]] — Non-parametric model selection evaluated on multimodal datasets.
* [[moslem-2026-routing-survey]] — Section 8 covers multimodal routing; notes that video/audio modalities beyond text+image remain largely unaddressed open challenges.
