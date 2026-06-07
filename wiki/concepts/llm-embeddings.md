---
type: concept
title: "LLM Embeddings"
tags: [representation-learning, llm-routing, model-evaluation]
sources: [zhuang-2025-embedllm]
created: 2026-06-06
updated: 2026-06-06
---

# LLM Embeddings

**LLM Embeddings** (or model embeddings) represent entire Large Language Models (LLMs) as compact, low-dimensional vectors in a latent space. Unlike traditional text embeddings that encode semantic meanings of words or sentences, LLM embeddings represent the capability profiles, domain expertise, and performance characteristics of individual neural models.

The paradigm was introduced in [[zhuang-2025-embedllm]] via the [[embedllm]] framework to simplify model comparison, evaluation, and selection across a large pool of candidate models.

## Core Idea
As the landscape of machine learning features hundreds of thousands of specialized and general-purpose LLMs, traditional evaluation (benchmarking) and inference routing (sending queries to the best model) have become computationally prohibitive. LLM embeddings map each model $M_i$ to a vector $v_m \in \mathbb{R}^d$. By placing both models and questions in a shared vector space, downstream tasks can predict model behavior using simple, fast vector operations.

## Training Methodologies
The primary methodology for learning LLM embeddings is **matrix reconstruction**:
* **Matrix Factorization**: A correctness matrix $Y$ of size $|M| \times |P|$ is constructed, where $Y_{ij} \in \{0, 1\}$ represents whether model $i$ answered prompt $j$ correctly.
* **Encoder-Decoder Architecture**:
  * An encoder maps models to $v_m \in \mathbb{R}^d$ and prompts to $v_p \in \mathbb{R}^d$ (often projecting pre-computed sentence embeddings).
  * A decoder uses these vectors (e.g., via the Hadamard product $v_m \odot v_p$ followed by a linear layer) to predict correctness, training the weights via Binary Cross-Entropy loss.

Alternative paradigms, such as Item Response Theory (IRT), are also used to represent model abilities based on parameterized curves of question difficulty and model proficiency.

## Downstream Applications
1. **Model Routing**: Predicting the correctness probability for every candidate model on a given query, allowing a router to select the optimal model. This avoids costly and slow multi-LLM scoring.
2. **Benchmark Performance Forecasting**: Predicting a model's average accuracy on an unseen benchmark by training a regression model on the embeddings, saving significant computation.
3. **Similarity and Probing**: Probing the embedding space shows that models with similar traits (e.g., parameter sizes like 7B, 13B, 70B, or task specializations like coding, medical QA, and physics) cluster together in L2 distance.

## Key Limitations
* **Static Nature**: In traditional matrix factorization approaches, adding new models to the pool requires retraining the embedding network.
* **Granularity**: Current implementations rely on binary correctness datasets, which may lose details compared to full text outputs.

## See Also
* [[zhuang-2025-embedllm]] — The source paper introducing LLM embeddings.
* [[embedllm]] — The framework designed to learn these representations.
