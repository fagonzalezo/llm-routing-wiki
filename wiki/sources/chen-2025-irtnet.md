---
type: source
title: "Learning Compact Representations of LLM Abilities via Item Response Theory"
authors: ["Jianhao Chen", "Chenxu Wang", "Gengrui Zhang", "Peng Ye", "Lei Bai", "Wei Hu", "Yuzhong Qu", "Shuyue Hu"]
url: "https://arxiv.org/abs/2510.00844"
raw: "raw/Chen 2025 - Learning Compact Representations of LLM Abilities via Item Response Theory.pdf"
ingested: 2026-06-06
tags: [llm-routing, model-embeddings, item-response-theory, benchmark-prediction, mixture-of-experts]
entities: [irtnet, embedllm]
concepts: [llm-embeddings, model-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Learning Compact Representations of LLM Abilities via Item Response Theory

## Summary
[[chen-2025-irtnet]] introduces **[[irtnet]]**, a psychometrics-inspired framework that applies **Item Response Theory (IRT)** to learn compact, low-dimensional vector embeddings of Large Language Models (LLMs). Framing LLM evaluation as estimating the probability that a model will answer a specific query correctly, IrtNet models this probability as a function of the model's multi-skill latent ability embedding ($\theta_m$), the query's discrimination vector ($\alpha_q$), and the query's difficulty scalar ($\beta_q$). To learn these parameters jointly and end-to-end, the framework employs a Mixture-of-Experts (MoE) network to capture multi-faceted query characteristics. Empirical results show that IrtNet achieves state-of-the-art performance in both [[model-routing]] and benchmark prediction, while learning representations that are highly interpretable.

## Key Claims & Contributions
* **IRT Formulation for LLMs**: First work to formally apply the psychometric 2-parameter logistic (2PL) Item Response Theory model to represent LLM capabilities, decomposing query-model interactions into latent abilities, item difficulty, and item discrimination.
* **State-of-Art Model Routing**: Achieves an average micro accuracy of 67.4% across 10 benchmarks, outperforming baseline methods such as RouterDC (54.9%), MODEL-SAT (56.7%), Avengers-Pro (62.1%), and [[embedllm]] (60.2%).
* **Data-Efficient Benchmark Prediction**: Successfully predicts model accuracy on unseen benchmarks with high data efficiency. With just 1,000 queries (<4% of training data), it achieves 69.9% prediction accuracy, matching [[embedllm]]'s performance using the full training set.
* **Interpretable Embedding Properties**: Validates that learned parameters capture real-world attributes:
  * Query difficulty ($\beta_q$) correlates near-perfectly ($r = -0.9721$) with empirical model accuracy.
  * Query discrimination ($\alpha_q$) clusters cleanly by benchmark without labels.
  * Model embeddings ($\theta_m$) group geometrically by both architectural family (e.g., Llama, Qwen, Gemma) and domain specialization (e.g., Code, Math).

## Methodology & Formulation
The relationship between a model $m \in M$ and a query $q \in Q$ is modeled as a binary outcome $y \in \{0, 1\}$, where $y=1$ signifies a correct answer.

### Mathematical Formulation
Inspired by the 2-parameter logistic (2PL) model in Item Response Theory:
$$P(y=1 | m, q) = \sigma(\alpha_q^\top \theta_m - \beta_q) = \frac{1}{1 + e^{-(\alpha_q^\top \theta_m - \beta_q)}}$$
Where:
* $\theta_m \in \mathbb{R}^d$ represents the compact $d$-dimensional latent ability vector of LLM $m$ ($d = 232$).
* $\alpha_q \in \mathbb{R}^d$ represents the query $q$'s discrimination vector, showing the importance of each ability dimension.
* $\beta_q \in \mathbb{R}$ represents the query $q$'s difficulty.
* $\sigma(\cdot)$ is the logistic sigmoid link function.

The dot product $\alpha_q^\top \theta_m$ measures how well the model's abilities align with the specific demands of the query.

### IrtNet Architecture
IrtNet learns these parameters jointly in an end-to-end manner:
1. **Query Text Embedding**: Each query $q$ is converted into a 768-dimensional embedding $v_q$ using a pre-trained sentence transformer (`all-mpnet-base-v2`).
2. **Dense Mixture-of-Experts (MoE) Layer**: To capture diverse, multi-faceted understanding of queries, $v_q$ is fed into a dense MoE layer (activating all $N=40$ experts) with an auxiliary-loss-free load balancing strategy to produce hidden representation $h_q$:
   $$h_q = \text{SharedExpert}(v_q) + \sum_{i=1}^N w_i \cdot \text{RoutedExpert}_i(v_q)$$
3. **Parameter Projection**: Two independent linear layers project $h_q$ to query parameters:
   $$\alpha_q = \text{Linear}(h_q, d), \quad \beta_q = \text{Linear}(h_q, 1)$$
4. **Optimization**: The model embeddings $\theta_m$ are represented as learnable parameters. The entire network is optimized using Binary Cross-Entropy (BCE) loss:
   $$\mathcal{L} = -\sum_{(m,q,y) \in D} [y \log(o(m,q)) + (1-y) \log(1-o(m,q))]$$
   where $o(m,q) = \sigma(\alpha_q^\top \theta_m - \beta_q)$.

### Dataset
IrtNet is trained and evaluated on the same dataset as [[embedllm]], containing **112 open-source language models** and **35,673 queries** across 10 benchmarks:
* Math & Logic: ASDiv, GSM8K, MathQA, LogiQA
* General & Academic: GPQA, MMLU
* Domain-Specific & Commonsense: MedMCQA, SocialIQA, PIQA, TruthfulQA

## Empirical Results

### Model Routing Accuracy
Queries are routed to the model $m^* = \arg\max_{m} f_\theta(m, q)$. IrtNet achieves superior micro- and macro-averaged accuracy on the combined test set across the 10 benchmarks:

| Method | Micro Avg (%) | Macro Avg (%) |
| :--- | :---: | :---: |
| RouterDC | 54.9 | 52.2 |
| [[embedllm]] | 60.2 | 54.3 |
| MODEL-SAT | 56.7 | 49.1 |
| Avengers-Pro | 62.1 | 55.7 |
| **IrtNet (Ours)** | **67.4** | **62.0** |

### Benchmark Prediction
* **In-Distribution (ID)**: IrtNet displays extreme data efficiency.
  * With 1K queries, it achieves **69.9%** correctness prediction accuracy, outperforming KNN (62.6%) and [[embedllm]] (60.8%).
  * On the full training dataset (29K queries), it reaches **72.2%** accuracy (vs. 70.6% for [[embedllm]]).
* **Out-of-Distribution (OOD)**: Leave-one-out prediction on held-out benchmarks.
  * IrtNet achieves an overall Root Mean Square Error (RMSE) of **0.19** (a 10% error reduction from [[embedllm]]'s 0.21).

### Ablation Study
Ablating the MoE layer (replacing it with an MLP of equivalent parameter size) demonstrates its critical role, particularly in model routing:
* Full IrtNet: 67.4% routing accuracy, 72.2% correctness accuracy.
* w/o MoE: 64.0% routing accuracy ($\downarrow 3.4$), 71.3% correctness accuracy ($\downarrow 0.9$).
* The MoE layer is vital for generating highly discriminative $\alpha_q$ representations, capturing distinctions among model abilities.

## Interpretability Analysis
* **Query Discrimination ($\alpha_q$)**: Projecting $\alpha_q$ using t-SNE shows that queries from the same benchmark naturally cluster together in semantic groups, even though IrtNet was trained without dataset labels.
* **Query Difficulty ($\beta_q$)**: The average learned difficulty $\beta_q$ correlates near-perfectly with the empirical average model error ($r = -0.9721$ with average model accuracy).
* **Model Embeddings ($\theta_m$)**: Evaluating L2 distances shows that the average intra-community L2 distance (e.g., within Llama family, Gemma family, or Math/Code specialist groups) is significantly smaller than the inter-community L2 distance, showing that the embedding space geometrically encodes architectural lineage and functional specialization.

## Where this fits
* **Entities**:
  * [[irtnet]] — The IRT-based framework introduced in this paper.
  * [[embedllm]] — The key baseline and predecessor that IrtNet is evaluated against.
* **Concepts**:
  * [[llm-embeddings]] — The broader concept of learning compact representations of LLMs.
  * [[model-routing]] — Selecting the best model from a candidate pool dynamically.
