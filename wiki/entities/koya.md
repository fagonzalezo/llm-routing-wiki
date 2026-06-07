---
type: entity
title: "Koya"
tags: [llm-routing, recommender-system, low-resource-nlp, african-languages]
sources: [advanced-architectures-llm-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Koya

**Koya** is a recommender system for Large Language Model selection, introduced by Owodunni & Emezue (AfricaNLP 2023). It is specifically designed for extremely low-resource NLP scenarios — particularly African languages such as Yoruba, Kinyarwanda, and Amharic — where fine-tuning or extensive profiling of candidate models is infeasible.

## Core Mechanism: Koya Pseudo-Perplexity (KPPPL)

Koya's primary contribution is the **Koya Pseudo-Perplexity (KPPPL)** metric, which evaluates the compatibility of a pre-trained LLM with a specific downstream task without requiring fine-tuning or access to gold labels. KPPPL measures a model's internal uncertainty over the task domain using pseudo-likelihood scoring, functioning as a proxy for how well the model's training distribution aligns with the target task.

Given a set of candidate LLMs and a task specification, Koya ranks models by their KPPPL scores and recommends the most compatible model for the task.

## Performance

Koya achieves a reported average recommender accuracy of **95%** across evaluated African language tasks, demonstrating that lightweight pseudo-likelihood-based model selection can effectively substitute for costly full fine-tuning pipelines in resource-constrained settings.

## Relation to the RecSys Isomorphism

Koya is a concrete instantiation of the broader [[collaborative-filtering]] / recommender-system isomorphism applied to LLM selection (see [[advanced-architectures-llm-routing]]). Rather than using matrix factorization over user-item interactions, Koya substitutes KPPPL as the lightweight compatibility signal — adapting the RecSys selection problem to scenarios with zero interaction history (the extreme cold-start case).

## Context and Significance

- **Domain**: African NLP, low-resource language processing.
- **Conference**: 4th Workshop on African Natural Language Processing (AfricaNLP 2023).
- **Reference**: Owodunni, A. T., & Emezue, C. C. (2023). [Link](https://openreview.net/forum?id=5DGm3lou3z)

## See Also

- [[collaborative-filtering]] — the RecSys paradigm Koya instantiates for LLM selection.
- [[model-routing]] — the broader problem Koya addresses.
- [[skill-based-routing]] — an alternative interpretable approach ([[bella]]) that uses capability matrices rather than pseudo-perplexity.
- [[advanced-architectures-llm-routing]] — survey that contextualizes Koya within the RecSys–routing isomorphism.
