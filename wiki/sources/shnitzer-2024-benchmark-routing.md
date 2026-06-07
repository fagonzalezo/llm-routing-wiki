---
type: source
title: "Large Language Model Routing with Benchmark Datasets"
authors: ["Tal Shnitzer", "Anthony Ou", "Míriam Silva", "Kate Soule", "Yuekai Sun", "Justin Solomon", "Neil Thompson", "Mikhail Yurochkin"]
url: "https://arxiv.org/abs/2309.15789"
raw: "raw/Shnitzer 2024 - Large Language Model Routing with Benchmark Datasets.pdf"
ingested: 2026-06-06
tags: [llm-routing, benchmark, binary-classification, knn-routing, methodology, ood-generalization]
entities: []
concepts: [benchmark-based-routing, knn-routing, model-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Large Language Model Routing with Benchmark Datasets

## Summary

Shnitzer et al. (2024) address the challenge of selecting the best LLM from a pool of models for an *unseen* new task, proposing a framework that **repurposes existing benchmark evaluation byproducts** — specifically, per-sample correctness records across tasks and domains — to learn lightweight "router" models. The core insight is that running expensive LLM inference for benchmark evaluation is already paid for; the resulting per-sample pass/fail signals can be recycled to train a router without any additional LLM calls. The problem is reduced to a collection of **M independent binary classification tasks** (one per candidate LLM), each predicting whether that LLM will answer a new query correctly.

## Key Contributions

1. **Problem formulation.** The paper formalizes LLM routing as learning a correctness predictor $g_m(x) \approx P(y(x,m)=1|x)$ for each model $m$, trained across all benchmark tasks jointly. The "correctness" label $y(x,m) \in \{0,1\}$ is derived by thresholding the raw benchmark metric $f^d_{im}$ above a task-specific threshold $\eta^d$.

2. **Three routing scores.** Given a new task $d'$ with inputs $\{x_i\}$, the authors propose three ways to aggregate correctness predictions into an LLM-level score:
   - **S1** — Average raw predicted probability: $\frac{1}{n}\sum_i g_m(x_i)$. Simple but sensitive to miscalibration on OOD data.
   - **S2** — Average thresholded prediction: $\frac{1}{n}\sum_i \mathbb{1}[g_m(x_i) > t]$. More robust than S1 when calibration degrades OOD, but ignores predictor uncertainty.
   - **S3 (OOD-aware)** — Incorporates an estimated task-level OOD confidence $p(d', m)$ — the probability that $\bar{g}_m$ makes the right call on task $d'$. The estimator is derived via meta-learning analogies and similarity of the new task's embedding distribution to benchmark tasks. S3 is theoretically grounded and consistently best empirically.

3. **Implementation.** The correctness predictor uses **sentence-transformer embeddings** (Reimers & Gurevych, 2019) as input features and **k-Nearest Neighbors (kNN) classifiers** as the model family — a deliberately simple, non-parametric choice to demonstrate that routing utility does not require complex architectures.

4. **Empirical evaluation.** Experiments span:
   - **HELM** (29 tasks): QA, text classification, reasoning, summarization. 18 candidate LLMs (codegen-16b-mono to llama-2-70b).
   - **MixInstruct**: instruction-following datasets.
   - Routing **outperforms the single best model** in all settings across all score variants.

5. **Robustness analyses.** (a) OOD predictor accuracy degrades but routing remains net positive; (b) larger/more diverse benchmark pools improve routing; (c) routing smaller LLMs can reduce costs with some accuracy trade-offs.

## Candidate LLMs (HELM experiments)

18 models: codegen-16b-mono (acc=0.451), dial-flant5-xl (0.454), falcon-40b (0.641), flan-t5-xl (0.650), flan-t5-xxl (0.658), flan-ul2 (0.668), gpt-jt-6b-v1 (0.576), gpt-neox-20b (0.492), mpt-7b-instruct (0.514), mt0-xxl (0.543), llama-2-13b (0.624), llama-2-13b-chat (0.623), llama-2-70b (0.688, best single model), llama-2-70b-chat (0.687), llama-2-7b (0.610), llama-2-7b-chat (0.605), starcoder (0.587). Routing consistently exceeds the 0.688 single-model ceiling.

## Methodology Details

- **Binary cross-entropy loss** for training correctness predictors per LLM.
- **Sentence-transformer embeddings** encode inputs; kNN retrieves nearest labeled benchmark samples at test time.
- **OOD confidence estimation (S3):** $p(d', m)$ estimated by comparing new task's embedding distribution to benchmark task distributions, with Laplace-smoothed meta-accuracy. Connected to PAC-Bayes and meta-learning theory.
- **No LLM calls at test time** beyond the single chosen model — the router is fully input-only, contrasting with generation-scoring approaches like [[frugalgpt]].

## Limitations

- Correctness predictors degrade on tasks semantically far from the benchmark distribution.
- S3's OOD confidence estimation is approximate.
- Requires candidate LLMs to have benchmark evaluation records — cannot route cold-start models.
- Cost is not modeled in the routing objective (accuracy-only optimization).

## Where This Fits

An early (Sep 2023) systematic treatment of [[benchmark-based-routing]] — a paradigm distinct from query-level routing where benchmark evaluation byproducts are recycled as router training data. Complements [[knn-routing]] by using kNN as the correctness predictor backbone. Contrasts with [[frugalgpt]] (requires scoring every candidate's generation at test time) and [[routellm]] (trains on human preference data). The OOD challenge central to S3 resurfaces in [[li-2025-predictive-routing]], which independently advocates non-parametric approaches under distribution shift. Later work in [[embedllm]] and [[irtnet]] can be seen as more expressive variants of the correctness-prediction approach.
