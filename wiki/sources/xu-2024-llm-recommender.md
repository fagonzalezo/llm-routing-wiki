---
type: source
title: "Tapping the Potential of Large Language Models as Recommender Systems: A Comprehensive Framework and Empirical Analysis"
authors: ["Lanling Xu", "Junjie Zhang", "Bingqian Li", "Jinpeng Wang", "Sheng Chen", "Wayne Xin Zhao", "Ji-Rong Wen"]
url: "https://arxiv.org/abs/2401.04997"
raw: "raw/Xu 2024 - Prompting Large Language Models for Recommender Systems A Comprehensive Framework and Empirical Analysis.pdf"
ingested: 2026-06-06
tags: [llm-recommendation, prompt-engineering, recommender-systems, empirical-study, user-interest-modeling]
entities: []
concepts: [llm-rs-framework, user-interest-modeling, llm-recommendation-prompting, collaborative-filtering]
created: 2026-06-06
updated: 2026-06-06
---

# Xu 2024 — LLM as Recommender Systems: Framework & Empirical Analysis

## Summary

This paper (published January 2025, arXiv 2401.04997) from Renmin University of China and Meituan Group proposes **LLM-RS**, a general framework for employing Large Language Models as recommender systems via prompt engineering. The work is primarily empirical: rather than proposing a specific model, it systematically dissects every design decision involved in using an LLM as a recommender and reports controlled experiments on two public datasets.

The framework decomposes the problem along two axes:

1. **LLMs** — choice of foundation model (open vs. closed source, architecture, parameter scale, context length, tuning strategy).
2. **Prompts** — four components: (a) task description, (b) user interest modeling, (c) candidate items construction, (d) prompting strategies.

## Key Contributions

- Proposes **LLM-RS**, a unified framework generalizable to multiple recommendation scenarios (rating prediction, sequential recommendation, top-N ranking, explanation generation).
- Formalizes LLM inputs for recommendation as structured natural language prompts with user interest and candidate item modules.
- Provides extensive controlled experiments isolating the effect of each design choice, producing a set of *new findings* and *re-validated findings* (see Table 1 in the paper).

## Core Empirical Findings

### On LLMs (foundation model axis)

- **Scale helps**: Larger parameter counts consistently improve recommendation quality.
- **Context length hurts**: A longer *maximum* context window correlates with *worse* recommendations — models optimized for very long contexts may be less focused on recommendation cues.
- **Slow-thinking LLMs (e.g., o1-style)** are tuned for math and coding and are *not* well-suited to recommendation tasks.
- **Full fine-tuning > LoRA**: Fine-tuning all parameters outperforms parameter-efficient LoRA, though it is costlier. Within LoRA, higher rank generally helps.
- **Zero-shot LLMs lag traditional recommenders** but fine-tuned LLMs can surpass them.
- **Instruction tuning** enhances fine-tuning results on recommendation tasks.
- **Few-shot regimes**: LLMs adapt to recommendation faster than traditional models with limited training data.
- **Known limitations**: position bias (LLMs favor items appearing in certain positions in the prompt) and lack of domain-specific knowledge.

### On Prompts — User Interest Modeling

- **Retrieval-based and generation-based** interest modeling outperform simple memory-based (truncation) methods; maintaining an explicit interest memory is important.
- **Long-term + short-term interest** are complementary; combining them with personalized descriptions yields the best results.
- Simply truncating recent interaction history to represent short-term interest is *not* optimal.
- Increasing the number of historical items yields **diminishing returns**.
- Personalized user profiles and customized item descriptions are beneficial.
- Retrieval-enhanced items improve sequential comprehension.

### On Prompts — Candidate Items Construction

- LLMs have difficulty retaining critical information about long candidate lists, leading to **hallucination** and task deviation.
- **Description-based identifiers** (natural language names) outperform token-based (ID) identifiers for item grounding.
- A retrieve-then-rerank pipeline (traditional model retrieves, LLM reranks) outperforms end-to-end LLM selection.

### On Prompts — Prompting Strategies

- **Chain-of-Thought (CoT)**: Generic CoT doesn't help; recommendation-specific problem decomposition is needed.
- **Few-shot prompting** offers only insignificant advantages over zero-shot for recommendation.
- **Explicit feedback** (e.g., ratings) is more useful than implicit feedback for fine-tuning.
- LLMs need **explicit temporal guidance** to correctly prioritize recent items, even when the history is presented in chronological order.
- **Role-playing / expert-like prompts** can unlock LLM capabilities.

## Methodology

- Datasets: two public recommendation benchmarks (consistent with standard RecBole datasets such as MovieLens and Amazon product reviews).
- Evaluation: standard recommendation metrics (Hit Rate, NDCG) for ranking tasks.
- Baselines: traditional collaborative filtering models (NCF, GNN-based), pre-trained language model recommenders, and various LLM variants.
- Framework instantiated across: rating prediction, sequential recommendation, top-N ranking, and explanation generation tasks.

## Where This Fits

This paper is the most comprehensive empirical treatment of **LLMs as recommenders** in the wiki. It complements routing-focused work by showing that LLMs can serve as the *end-to-end recommendation engine* rather than a query router, and that prompt engineering is as critical for recommendation as it is for routing.

Key connections:
- [[collaborative-filtering]] — The paper benchmarks CF baselines; fine-tuned LLMs can exceed them.
- [[prompt-recommendation]] — The four-component prompt framework directly informs how prompts should be structured for recommendation tasks.
- [[llm-rs-framework]] — Unified LLM-RS framework introduced here.
- [[user-interest-modeling]] — User interest component of the recommendation prompt.
- [[llm-recommendation-prompting]] — Four-component prompting framework for recommendation.
- [[model-routing]] — Retrieve-then-rerank pipelines connect to routing: a traditional retriever routes candidate selection, then an LLM re-ranks.
- [[llm-cascade]] — Sequential retrieve-then-rerank is architecturally similar to cascade routing.
- [[nelson-2025-ethical-rec]] — The other source using CF for LLM-adjacent recommendation; Xu 2024 provides a much broader empirical basis.
