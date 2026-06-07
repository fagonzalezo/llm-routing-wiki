---
type: concept
title: "User Interest Modeling (LLM Recommendation)"
tags: [llm-recommendation, user-interest-modeling, prompt-engineering, sequential-recommendation]
sources: [xu-2024-llm-recommender]
created: 2026-06-06
updated: 2026-06-06
---

# User Interest Modeling (LLM Recommendation)

**User Interest Modeling** is the component of an LLM-based recommendation prompt that encodes what a user likes or wants, derived from their historical interaction sequence. It is one of the four key prompt components in the [[llm-rs-framework]] identified by Xu et al. (2024).

## Why It Matters

LLMs lack direct access to user databases or interaction logs. The only way an LLM can personalize its recommendations is through what is included in the prompt. User interest modeling determines *how* to represent a user's preferences compactly and accurately within the token budget.

## Approaches

### By Temporal Scope

- **Short-term interest**: Recent interactions reflecting current mood or context.
- **Long-term interest**: Stable patterns across extended history reflecting durable preferences.
- **Combined**: Xu et al. find that combining both with personalized descriptions yields the best results; they are complementary, not redundant.

### By Construction Method

1. **Memory-based (truncation)**: Simply include the N most recent items from history. Simple but suboptimal — naive truncation discards structure and context.
2. **Retrieval-based**: Retrieve the most relevant historical items for a given query or candidate item from a larger interaction store. Outperforms memory-based by maintaining an explicit interest memory.
3. **Generation-based**: Use an LLM (or another model) to synthesize a natural language user profile or interest description from the interaction history. Also outperforms plain truncation.

## Key Empirical Findings (from [[xu-2024-llm-recommender]])

- Retrieval-based and generation-based methods outperform memory-based across the board.
- The *interest memory* — maintaining a richer representation beyond raw item lists — is important.
- Long-term and short-term interest complement each other; personalized descriptions tied to each improve performance.
- Simply truncating to recent items is **not optimal** for short-term interest representation.
- Adding more historical items brings **diminishing gains** beyond a moderate count.
- Personalized user profiles and customized item descriptions provide meaningful assistance.
- Retrieval-enhanced item representations improve sequential comprehension.

## Connection to Routing

User interest modeling is analogous to **query characterization** in LLM routing: just as a router needs a compact representation of a query's difficulty, domain, and intent to make routing decisions, a recommendation prompt needs a compact representation of a user's preferences and recent context. Both require a retrieval or summarization step before the main LLM call.

## See Also

- [[llm-rs-framework]] — The parent framework this component belongs to.
- [[llm-recommendation-prompting]] — The four-component prompt framework in full.
- [[xu-2024-llm-recommender]] — Source paper with empirical comparisons.
- [[collaborative-filtering]] — Traditional approach to capturing user-item affinity.
- [[model-routing]] — Analogous query characterization step in routing pipelines.
