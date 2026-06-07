---
type: entity
title: "RouteLLM"
kind: product
tags: [llm-router, open-source, preference-learning]
sources: [ong-2025-routellm, moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# RouteLLM

## Definition
RouteLLM is an open-source framework and Python library designed to build, evaluate, and serve routing models that dynamically dispatch queries between "strong" (expensive, high-quality) and "weak" (cost-effective) large language models. Developed by researchers at UC Berkeley, LMSYS, Anyscale, and Canva, RouteLLM uses human preference data (e.g. from Chatbot Arena) to learn optimal cost-performance routing policies.

## Key Architectures
RouteLLM supports several router classifiers:
* **Matrix Factorization (MF)**: Projects queries and models into a joint low-rank latent embedding space, calculating win probability via a bilinear model-query inner product.
* **Similarity-Weighted (SW) Ranking**: A non-parametric classifier that calculates the weighted Elo rating of the current query based on its cosine similarity to historical Chatbot Arena prompts.
* **BERT Classifier**: Uses a `bert-base-uncased` text classification network to output binary win probabilities.
* **Causal LLM Classifier**: Fine-tunes a generative model (like Llama 3) to output win probabilities as a classification task.

## Key Datasets & Training
* **Chatbot Arena Battles**: Over 80,000 anonymized pairwise battles where human judges voted on outputs from competing LLMs.
* **Nectar Dataset**: Used for LLM-judge data augmentation, generating 120,000 synthetic labels evaluated by GPT-4 to enrich router training signals.

## Performance
Empirical evaluations demonstrate that RouteLLM routers can:
* Achieve over **85% cost savings** on MT-Bench, **45%** on MMLU, and **35%** on GSM8K.
* Retain **95% of GPT-4's performance** when routing between GPT-4 (strong) and Mixtral-8x7B (weak).
* Generalize to unseen model pairs (e.g. Claude, Llama 3) without retraining.

## Repository & Toolkit
The open-source repository provides:
1. Training scripts for both parametric and non-parametric routers.
2. A unified evaluation harness over public benchmarks.
3. An OpenAI-compatible API server to deploy routers in production pipelines.

## References
* Introduced in [[ong-2025-routellm]].
* Cited in [[moslem-2026-routing-survey]] as the canonical example of *preference-aligned routing* — a paradigm that learns routing decisions from human pairwise comparison data.
