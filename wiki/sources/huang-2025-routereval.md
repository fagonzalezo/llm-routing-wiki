---
type: source
title: "RouterEval: A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up in LLMs"
authors: ["Zhongzhan Huang", "Guoming Ling", "Yupei Lin", "Yandong Chen", "Shanshan Zhong", "Hefeng Wu", "Liang Lin"]
url: "https://aclanthology.org/2025.findings-emnlp.208"
raw: "raw/Huang 2025 - RouterEval A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up in LLMs.pdf"
ingested: 2026-06-06
created: 2026-06-06
updated: 2026-06-06
tags: [llm-routing, benchmark, model-scaling, resource-efficiency]
entities: [routereval]
concepts: [model-routing, dynamic-routing]
---

# RouterEval: A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up in LLMs

## Overview
**RouterEval** is a comprehensive, open-source evaluation benchmark designed specifically for routing large language models (LLMs), introduced by researchers from Sun Yat-sen University in EMNLP Findings 2025. LLM routing dynamically matches inputs to the best-suited candidate from a model pool, balancing cost, accuracy, and latency.

The paper makes two major contributions:
1. **Model-level Scaling Up Phenomenon**: A novel finding showing that when a router has sufficient routing capability (modeled by probability $p \geq 0.5$ of choosing the optimal LLM), the system's performance scales up rapidly as the number of available candidate LLMs ($m$) increases. This routing-based scaling can exceed the performance of the single best model in the pool and top commercial LLMs, even when the pool is populated by weaker, open-source models.
2. **RouterEval Benchmark**: To resolve the lack of comprehensive and open-source benchmarks for LLM routing, the authors introduce RouterEval, which includes over 200,000,000 performance records of over 8,500 LLMs across 12 popular evaluation benchmarks.

## Model-Level Scaling Up
The authors investigate the relationship between the candidate pool size $m$ and performance using different levels of router capability.
* **Oracle Router ($r_o$)**: A theoretical router that always selects the optimal candidate LLM from the pool for a given input.
* **Noisy Router ($r_o(p)$)**: Formulated as:
  $$r_o(p) = \begin{cases} r_o & \text{with probability } p \\ \omega_m & \text{with probability } 1-p \end{cases}$$
  where $\omega_m$ is a random uniform sampler over the $m$ candidates. When $p \to 1$, $r_o(p)$ approaches the oracle router; when $p \to 0$, it degenerates into a random sampler.
* **Findings**:
  * **Sparse Model-level Scaling**: For $p \geq 0.5$, increasing the pool size $m$ yields rapid performance improvements. The authors analogize this to neural scaling laws, where increasing candidate models acts as an implicit, sparse scaling of parameters.
  * **Weak Candidate Complementarity**: Even when candidate models are individually weak (e.g., all under 30% accuracy on MMLU), their combination under a capable router achieves high accuracy (up to 95% on MMLU). This suggests that diverse, heterogeneous, and small models can achieve fine-grained division of labor.
  * **Small Pool Sufficiency**: A small pool size of $3 \leq m \leq 10$ is often sufficient to achieve most of the scaling benefits and exceed strong baseline models like GPT-4, making routing highly cost-effective and practical.

## RouterEval Benchmark
RouterEval is designed to evaluate, train, and test LLM routers systematically.

### Data Scale & Coverage
RouterEval compiles test performance records across **12 popular LLM evaluations**:
* ARC, HellaSwag, MMLU, TruthfulQA, Winogrande, GSM8k, IFEval, BBH, GPQA, MUSR, MATH Lvl 5, and MMLU-PRO.
* Based on **8,500+ LLMs**, producing over **200,000,000 records**.

### Data Format
The benchmark models routing as a multi-class classification problem. The datasets provide input-label pairs:
$$(X, Y) = \{\kappa(s_j), v_j\}_{j=1}^n$$
* **$\kappa(s_j)$**: Representation/embedding of input $s_j$. RouterEval provides pre-computed embeddings using **Sentence-BERT**, **RoBERTa** (and its last layer), and **Longformer**.
* **$v_j \in \{0, 1\}^m$**: Selection vector where $1$ denotes the optimal LLM candidate(s) for input $s_j$. For discrete tasks, multiple models can be labeled $1$ if they answer correctly. For continuous tasks, models yielding performance within 95% of the optimal model are marked $1$.
* **Train/Val/Test Split**: Standardized at 8:1:1.

### Difficulty Levels & Candidate Grouping
To thoroughly evaluate router capabilities, the benchmark sets:
* **Difficulty Levels**: Easy pools ($m \in \{3, 5\}$) and Hard pools ($m \in \{10, 100, 1000\}$).
* **Pool Group Construction**:
  * *All-Strong Group*: Candidates selected from the top 20% of performant models.
  * *All-Weak Group*: Candidates selected from the bottom 20% of performant models (with performance $>0.1$).
  * *Strong-to-Weak Group*: Candidates selected uniformly across the performance spectrum.

### Extra Training Data
Because direct training data on individual benchmarks can be scarce (hundreds to tens of thousands of samples), RouterEval provides an auxiliary dataset $D$ to support router training.

## Where this fits
* **Dynamic/Open Pool Routing**: RouterEval evaluates routers over large model pools (up to $m=1000$), directly supporting the design of dynamic routing systems like [[uniroute]].
* **Benchmark Evolution**: Serves as a massive-scale counterpart to smaller-scale routing benchmarks. It demonstrates that the key bottleneck in LLM routing is no longer model pools or data availability, but rather router architecture design (e.g., classification-based routers like [[routellm]] and representation-based routers like [[embedllm]] or [[irtnet]]).
* **Scaling Paradigm**: Shifts the focus from scaling single-model parameters (pre-training/post-training) to scaling candidate pools (inference-time sparse model-level scaling).
