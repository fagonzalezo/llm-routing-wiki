---
type: entity
title: "RouterEval"
kind: product
tags: [llm-routing, benchmark, evaluation, open-source]
sources: [huang-2025-routereval]
created: 2026-06-06
updated: 2026-06-06
---

# RouterEval

## Definition
**RouterEval** is a comprehensive, open-source benchmark specifically designed for routing large language models (LLMs). Developed by researchers at Sun Yat-sen University, RouterEval aims to provide a standardized, large-scale training and evaluation sandbox for LLM routers. It contains over **200,000,000 performance records** from more than **8,500 different LLMs** on 12 popular evaluation tasks.

## Key Components

### 1. Constituent Benchmarks
RouterEval aggregates performance data across 12 diverse LLM evaluations covering reasoning, comprehension, and instruction following:
* **ARC** (AI2 Reasoning Challenge)
* **HellaSwag**
* **MMLU** (Massive Multitask Language Understanding)
* **TruthfulQA**
* **Winogrande**
* **GSM8k** (Grade School Math 8k)
* **IFEval** (Instruction Following Evaluation)
* **BBH** (BIG-bench Hard)
* **GPQA** (Graduate-Level Google-Proof Q&A Benchmark)
* **MUSR** (Multistep Soft Reasoning)
* **MATH Lvl 5** (High School Math Competition problems)
* **MMLU-PRO**

### 2. Pre-computed Embeddings
To standardize input representations, RouterEval provides pre-computed text embeddings for the benchmarks' questions using four models:
* **Sentence-BERT**
* **RoBERTa** (and its last hidden layer)
* **Longformer**

### 3. Model Pool Configs
The benchmark constructs model pools of varying sizes and difficulties to evaluate router scalability:
* **Pool Sizes ($m$)**: Easy level ($m \in \{3, 5\}$) and Hard level ($m \in \{10, 100, 1000\}$).
* **Pool Groupings**:
  * *All-Strong*: Candidate models selected from the top 20% of performant models.
  * *All-Weak*: Candidate models selected from the bottom 20% of models (retaining models with accuracy $>0.1$).
  * *Strong-to-Weak*: Candidate models sampled uniformly across the entire performance distribution.

## Key Applications
* **Model-Level Scaling Analysis**: Used to show that routers with moderate-to-high capability ($p \geq 0.5$) trigger a model-level scaling phenomenon where overall system performance improves as candidate pool size ($m$) increases.
* **Router Training**: Serves as a dataset for training classification-based and representation-based routing systems, such as [[routellm]], [[embedllm]], and [[irtnet]].
* **Dynamic Pool Testing**: Tests the generalization of routers (like [[uniroute]]) to open pools of unseen candidate models.

## References
* Introduced in [[huang-2025-routereval]].
