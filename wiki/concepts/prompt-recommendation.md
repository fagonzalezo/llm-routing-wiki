---
type: concept
title: "Prompt Recommendation"
tags: [prompt-engineering, prompt-recommendation, user-experience, safety]
sources: [nelson-2025-ethical-rec, xu-2024-llm-recommender]
created: 2026-06-06
updated: 2026-06-06
---

# Prompt Recommendation

**Prompt Recommendation** (also referred to as **Prompt Guidance** or **Prompt Suggestion**) is the dynamic selection and suggestion of input prompts to users during their interactions with Large Language Models (LLMs). Rather than requiring users to manually design complex inputs (a process known as prompt engineering), a prompt recommendation system suggests pre-vetted, high-quality, or contextually relevant prompts.

## Motivation & Benefits

* **Reducing User Cognitive Load**: Writing effective prompts requires understanding LLM-specific behaviors (e.g., specifying roles, structured output formats, few-shot examples). Prompt recommendation lowers the barrier to entry for non-technical users.
* **Pre-emptive Safety & Alignment**: Traditional moderation checks are applied to the LLM's output (post-generation), which can be computationally wasteful or bypassed via adversarial prompt injections. Suggesting safe and ethical prompts pre-empts harmful generation at the input stage.
* **Improving Quality & Accuracy**: Guiding users toward structured prompts helps them obtain more accurate, bug-free, and complete model outputs (e.g., in code generation tasks).

## Architectures & Techniques

1. **Collaborative Filtering**: Suggests prompts by analyzing historical user-prompt ratings or selection frequencies. For example, [[nelson-2025-ethical-rec]] employs a **two-agent system** where a collaborative filtering recommender calculates similarities between user inputs and a dataset of rated prompts using the Pearson correlation coefficient.
2. **Retrieval-Augmented Guidance**: Analyzes the semantic content of the user's initial input and retrieves relevant templates or in-context exemplars from a database.
3. **Interactive Prompt Refinement**: Engages the user in a dialogue or questionnaire to iteratively build a complex prompt, shielding the user from prompt syntax.

## See Also
* [[nelson-2025-ethical-rec]] — Source paper applying collaborative filtering to prompt recommendations for ethical AI.
* [[xu-2024-llm-recommender]] — Comprehensive empirical analysis of using LLMs as recommenders; the four-component prompt framework directly applies to recommendation task design.
* [[llm-recommendation-prompting]] — The four-component prompting framework (task description, user interest, candidate construction, prompting strategies) for LLM-based recommendation.
* [[collaborative-filtering]] — The recommendation algorithm used to identify similar prompts.
* [[model-routing]] — Selecting and dispatching queries to different models based on capabilities.
