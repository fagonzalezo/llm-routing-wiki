---
type: source
title: "EmbedLLM: Learning Compact Representations of Large Language Models"
authors: ["Richard Zhuang", "Tianhao Wu", "Zhaojin Wen", "Andrew Li", "Jiantao Jiao", "Kannan Ramchandran"]
url: "https://arxiv.org/abs/2410.02223"
raw: "raw/Zhuang 2025 - EmbedLLM Learning Compact Representations of Large Language Models.pdf"
ingested: 2026-06-06
tags: [llm-routing, model-embeddings, correctness-forecasting, benchmark-prediction, matrix-factorization]
entities: [embedllm]
concepts: [llm-embeddings, model-routing]
created: 2026-06-06
updated: 2026-06-06
---

# EmbedLLM: Learning Compact Representations of Large Language Models

## Summary
[[zhuang-2025-embedllm]] introduces **EmbedLLM**, a reconstruction-based framework designed to learn compact, low-dimensional vector representations (embeddings) of Large Language Models (LLMs). Instead of repeatedly training task-specific representations for each downstream application, EmbedLLM maps models into a unified, shared latent space. The model is trained using an encoder-decoder architecture to reconstruct a binary correctness matrix of how different LLMs perform on a large set of benchmark questions. The resulting model embeddings can be leveraged for multiple downstream tasks—including correctness forecasting, [[model-routing]], and benchmark accuracy prediction—by training only a simple linear classifier or regression model on top.

## Key Claims & Contributions
* **Unified Model Embeddings**: First work to explicitly represent LLMs as low-dimensional vector embeddings, mapping each LLM to a vector in $\mathbb{R}^{dim_{embed}}$ to capture its strengths and weaknesses.
* **Low Downstream Resource Overhead**: Once embeddings are learned, adapting them to new tasks requires only training a linear layer, drastically reducing compute and latency.
* **High-Speed Routing**: The Matrix Factorization (MF) router executes over 750 model selections per second (15x faster than causal LLM routers like RouteLLM) while consuming less than 1GB of GPU memory (60x cheaper than fine-tuning a Llama-3-8B router).
* **Zero-Shot Accuracy Prediction**: Demonstrates that model performance on unseen benchmarks can be forecast using a linear regression model trained on the embeddings, avoiding millions of tokens of redundant model evaluation.

## Methodology & Formulation
EmbedLLM models the evaluation space as a matrix factorization problem. Let $M$ be the set of models, $P$ be the set of prompts, and $Y \in \{0, 1\}^{|M| \times |P|}$ be the correctness matrix showing whether model $m$ correctly answered prompt $p$.

### Architecture
1. **Encoder**:
   * **Model Embedding Network**: Maps each model index to a latent vector $v_m \in \mathbb{R}^{dim_{embed}}$.
   * **Question Embedding Network**: Takes the text of question $p$, encodes it using a sentence transformer (`all-mpnet-base-v2`) to a vector in $\mathbb{R}^{768}$, and projects it via a linear layer to $v'_q \in \mathbb{R}^{dim_{embed}}$.
2. **Decoder**:
   * Takes the Hadamard product of the model and question embeddings ($v_m \odot v'_q$) and feeds it to a linear classifier to output logits.
   * Outputs the predicted correctness probability $s_{m,q} = \sigma(p^{(m,q)}_1 - p^{(m,q)}_0)$.
3. **Loss Function**: Trained using Binary Cross-Entropy (BCE) loss:
   $$\mathcal{L}(m, q, y) = - (y \log(s_{m,q}) + (1-y) \log(1-s_{m,q}))$$

### Dataset
The dataset comprises the evaluation results of **112 open-source models** responding to **36,054 questions** across 10 benchmarks:
* MMLU, TruthfulQA, SocialQA, PIQA, MedMCQA, MathQA, LogiQA, GSM8K, GPQA, and ASDiv.

## Empirical Results
* **Correctness Forecasting**: Under all training split sizes (1K to 29K), Matrix Factorization consistently outperforms a KNN baseline. At full scale, MF achieves a correctness forecasting accuracy of 74.09% compared to 71.52% for KNN.
* **Model Routing**: The MF-based router selects the model with the highest correctness score for each prompt. It outperforms the weighted random router and achieves overall routing accuracy close to the single-best model router on individual benchmarks, while significantly outperforming it on the combined test set.
* **Benchmark Accuracy Prediction**: Using leave-one-out training (withholding benchmark $B$), a linear regression model on the embeddings predicts average model accuracy on $B$. The correlation is statistically significant (using Kendall's Tau test) on 7 out of 10 benchmarks (MathQA, LogiQA, MedMCQA, PIQA, TruthfulQA, MMLU, GSM8K). It fails on GPQA, ASDiv, and SocialQA due to either extreme difficulty or flat model performance distributions.

## Probing Analysis
* **Community Distance**: Computing L2 distance between model embeddings shows that models sharing key keywords (e.g., `7B`, `13B`, `70B`, `Coding`, `Bio/Med`, `Physics`) lie closer in the latent space (lower intra-community L2 distance than inter-community).
* **Benchmark Interdependencies**: Probing benchmark contributions via leave-one-out experiments reveals that:
  * **MMLU** contributes most to the quality of the learned embeddings, matching its diverse and comprehensive nature.
  * Adding simpler benchmarks to training hurts the ability to predict **GPQA** accuracy, highlighting that reasoning abilities on easy benchmarks do not generalize to graduate-level questions.
  * Math-related benchmarks (GSM8K, MathQA, ASDiv) exhibit strong mutual contribution, confirming that math-specific knowledge is correctly reflected in the embedding structure.

## Where this fits
* **Entities**:
  * [[embedllm]] — The framework introduced in this paper.
* **Concepts**:
  * [[llm-embeddings]] — The core concept of learning compact representations of LLMs.
  * [[model-routing]] — Utilizing the embeddings to build low-latency, resource-efficient routers.
