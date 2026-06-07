---
type: entity
title: "IrtNet"
tags: [llm-routing, framework, model-embeddings, item-response-theory]
sources: [chen-2025-irtnet]
created: 2026-06-06
updated: 2026-06-06
---

# IrtNet

**IrtNet** is a psychometrics-inspired machine learning framework designed to learn compact, low-dimensional vector representations of Large Language Models (LLMs) and queries. Based on **Item Response Theory (IRT)**, IrtNet models the probability of a model correctly answering a query as a function of the model's latent abilities, the query's difficulty, and the query's ability to discriminate between different models. It was introduced in [[chen-2025-irtnet]] by researchers from Nanjing University, Shanghai AI Laboratory, Fudan University, and USC.

## Overview
Evaluating and routing queries to a large pool of LLMs is computationally expensive. Traditional techniques require running extensive model evaluations or training query-specific classifiers. Like [[embedllm]], IrtNet represents LLMs as vectors in a shared latent space ($\theta_m \in \mathbb{R}^d$). However, IrtNet moves beyond simple matrix factorization by integrating the 2-parameter logistic (2PL) model from psychometrics, explicitly separating query difficulty and query discrimination.

## Architecture
IrtNet is trained end-to-end using a Mixture-of-Experts (MoE) network:
1. **Query Encoder**: Maps input query text to a dense vector via a sentence transformer (`all-mpnet-base-v2`) and processes it using a **Dense Mixture-of-Experts (MoE)** layer. The MoE layer activates all $N=40$ experts and outputs a hidden representation $h_q$.
2. **Item Response Parameters**: Projects $h_q$ through two independent linear layers:
   * **Discrimination Vector** ($\alpha_q \in \mathbb{R}^d$, where $d=232$): Specifies the importance of each latent ability dimension.
   * **Difficulty Scalar** ($\beta_q \in \mathbb{R}$): Represents the question's overall hardness.
3. **LLM Embedding**: Represents each LLM $m$ as a learnable ability vector $\theta_m \in \mathbb{R}^d$.
4. **Response Function**: Computes the output correctness probability using the standard 2PL IRT response function:
   $$P(y=1|m, q) = \sigma(\alpha_q^\top \theta_m - \beta_q)$$
5. **Loss**: Trained using Binary Cross-Entropy loss on correctness matrices.

## Key Applications
* **[[model-routing]]**: By calculating $P(y=1|m, q)$ for all models $m$ in a candidate pool, queries are routed to the model with the highest predicted success probability. IrtNet achieves state-of-the-art routing accuracy (67.4% micro average on 10 benchmarks), outperforming [[embedllm]] (60.2%) and Avengers-Pro (62.1%).
* **Benchmark Prediction**: Predicts LLM performance on unseen benchmark datasets. IrtNet exhibits high data efficiency, requiring only 1,000 queries to match the performance of models trained on entire datasets. It reduces Out-of-Distribution (OOD) prediction error (RMSE) by nearly 10% compared to [[embedllm]].

## Interpretability
The psychometric framing of IrtNet yields highly interpretable parameters:
* **Query Difficulty ($\beta_q$)**: Exhibits a $-0.9721$ Pearson correlation with actual model accuracies, validating it as a measure of empirical query hardness.
* **Query Discrimination ($\alpha_q$)**: In t-SNE projections, queries from the same benchmark naturally cluster together in semantic groups, capturing the unique capability profile demanded by each benchmark.
* **Model Ability ($\theta_m$)**: LLM embeddings geometrically cluster according to architectural lineage (e.g., Llama and Gemma families) and task specialization (e.g., Math and Coding models).

## See Also
* [[chen-2025-irtnet]] — The original paper proposing IrtNet.
* [[embedllm]] — The predecessor matrix factorization framework.
* [[llm-embeddings]] — The concept of representing LLM capabilities as vectors.
* [[model-routing]] — Dynamically dispatching queries to suitable models.
