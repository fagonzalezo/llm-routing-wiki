---
type: concept
title: "LLM Recommendation Prompting"
tags: [llm-recommendation, prompt-engineering, prompting-strategies, candidate-construction]
sources: [xu-2024-llm-recommender]
created: 2026-06-06
updated: 2026-06-06
---

# LLM Recommendation Prompting

**LLM Recommendation Prompting** refers to the structured design of natural language prompts that enable a Large Language Model to serve as a recommender system. In the [[llm-rs-framework]] (Xu et al. 2024), recommendation prompts are decomposed into four key components:

1. **Task Description** — Specifies the recommendation task type and constraints.
2. **User Interest Modeling** — Encodes user preferences from historical interactions (see [[user-interest-modeling]]).
3. **Candidate Items Construction** — Defines the pool of items the LLM should select from or rank.
4. **Prompting Strategies** — Higher-level techniques (CoT, few-shot, role-playing) applied on top of the base prompt.

## Component 1: Task Description

Frames the recommendation problem for the LLM: what to do (rank, select, explain), what domain it is in, and any constraints (e.g., budget, recency). Role-playing and expert-persona framing ("You are a movie recommendation expert") have been shown to improve performance.

## Component 2: User Interest Modeling

See [[user-interest-modeling]] for a detailed treatment. The short version: retrieval-based and generation-based methods outperform simple truncation; combining long-term and short-term signals with personalized descriptions works best.

## Component 3: Candidate Items Construction

How the set of candidate items is presented to the LLM for selection or ranking.

**Item Identifiers:**
- **Description-based** (natural language titles/descriptions): Outperforms token/ID-based identifiers. Grounding via text gives the LLM semantic anchors.
- **Token-based** (arbitrary item IDs): The LLM cannot leverage world knowledge with opaque tokens; performance is worse.

**Candidate Source:**
- **End-to-end LLM**: Let the LLM generate candidates from scratch. Suffers from hallucination and candidate list retention failures.
- **Retrieve-then-rerank**: A traditional retrieval model (e.g., BM25 or CF-based) narrows the candidate pool; the LLM reranks. This is the strongest pipeline — the retriever handles recall, the LLM handles precision.

**Failure mode**: LLMs struggle to retain all candidates in a long list from the prompt context, leading to hallucinated or off-task responses. Keeping candidate lists short and salient mitigates this.

## Component 4: Prompting Strategies

| Strategy | Verdict |
|----------|---------|
| **Zero-shot** | Baseline; LLMs under-perform traditional recommenders without fine-tuning |
| **Few-shot** | Insignificant gains over zero-shot for recommendation — adds tokens but little improvement |
| **Chain-of-Thought (CoT)** | Generic CoT is ineffective; *recommendation-specific problem decomposition* is required |
| **Role-playing / Expert persona** | Consistently helpful — frames the task and domain for the LLM |
| **Explicit temporal ordering** | Necessary — LLMs need explicit guidance to prioritize recent items even when history is chronologically ordered |
| **Feedback type** | Explicit ratings > implicit clicks for fine-tuning |

## Design Principles (synthesized from Xu 2024)

1. Use **description-based item identifiers** to leverage LLM world knowledge.
2. Use a **retrieve-then-rerank** pipeline rather than end-to-end LLM generation.
3. Model **both long-term and short-term user interest** with retrieval or generation, not raw truncation.
4. Apply **domain-specific decomposition** when using chain-of-thought, not generic CoT.
5. Include **explicit recency cues** to prevent the LLM from treating all history as equally weighted.
6. Use **role-playing or expert-persona framing** in the task description.

## Relationship to LLM Routing

The prompt engineering challenges here mirror those in routing:
- **Task description** ↔ query featurization in routing (characterizing what kind of task this is).
- **Candidate construction** ↔ model pool selection in routing (which models to consider).
- **Retrieve-then-rerank** ↔ [[llm-cascade]] (cheap model/retriever first, expensive LLM second).
- **Few-shot strategies** ↔ deployment-time few-shot adaptation in routing classifiers.

## See Also

- [[llm-rs-framework]] — Parent framework.
- [[user-interest-modeling]] — Deep-dive on component 2.
- [[xu-2024-llm-recommender]] — Source paper.
- [[llm-cascade]] — Structurally analogous retrieve-then-rerank pattern.
- [[prompt-recommendation]] — Related concept: recommending prompts *to* users (vs. prompting LLMs *for* recommendations).
- [[collaborative-filtering]] — Traditional retrieval backbone in retrieve-then-rerank pipelines.
