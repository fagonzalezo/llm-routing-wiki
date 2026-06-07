---
type: concept
title: "LLM Cascade"
tags: [llm-routing, cost-optimization]
sources: [chen-2023-frugalgpt, varangot-reille-2025-routing-survey, moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# LLM Cascade

An **LLM Cascade** is an inference-time routing architecture that routes a natural language query sequentially through a chain of Large Language Models of increasing cost and capability. At each step, a decision mechanism evaluates the generated response's quality and either returns the answer to the user (terminating the cascade) or escalates the query to the next, more powerful model in the sequence.

## Core Mechanisms

An LLM cascade is characterized by three main structural components:

1.  **Sequential Ordering**: Models are ordered from lowest cost/complexity (e.g., small, local, or cheap models) to highest cost/complexity (e.g., large commercial API models).
2.  **Scoring Function**: A scoring mechanism assesses the likelihood that the candidate model's generation is correct. This can be implemented using:
    *   An auxiliary lightweight classifier (e.g., DistilBERT trained on prediction accuracy).
    *   Model-based self-evaluation or log-probability calibration (where supported by the API).
3.  **Stop Judger**: A comparison of the score against a threshold $\tau$. If $\text{score} \ge \tau$, the answer is accepted and the process stops.

## Optimization Problem

The design of an LLM cascade involves finding:
*   The optimal sequence of models.
*   The optimal stopping thresholds $\{\tau_i\}$ for each model in the sequence.

These parameters are usually optimized on validation data to maximize the expected reward/accuracy under a given average cost constraint. A lower budget shifts the thresholds downward (accepting more answers from cheaper models), while a higher budget shifts them upward (routing more queries to higher-tier models).

## Contrast with Static Routing

Unlike static routing (which selects a single destination model *before* generating any output based on query features), cascading is an dynamic, iterative process. It evaluates the *actual generated content* before making the final routing decision, allowing cheaper models a chance to answer first.

## Additional Cascade Implementations

[[moslem-2026-routing-survey]] catalogues several further cascade systems beyond [[frugalgpt]]:

- **AutoMix**: Automatically mixes outputs from a small and large model based on query complexity, with a self-verification step.
- **Self-REF**: Uses the model's own reflexive evaluation to decide whether to escalate.
- **LM-Blender**: Combines outputs from multiple LLMs using a learned blending function as an alternative to strict escalation.
- **Cascade Routing**: A generalisation that treats escalation thresholds as learned routing parameters.

The survey also notes that cascades can embed *safety checks* on both input queries and output generations — extending cascading beyond cost-quality optimisation to policy enforcement.

## Where This Fits
*   [[chen-2023-frugalgpt]] — The primary reference paper introducing cascading for commercial LLM APIs.
*   [[frugalgpt]] — A specific implementation of a learned LLM cascade.
*   [[varangot-reille-2025-routing-survey]] — §3.2 defines cascade routing as the post-generation timing paradigm; also introduces multi-choice cascading.
*   [[post-generation-routing]] — The broader timing concept of which LLM cascading is the primary architectural instantiation.
*   [[pre-generation-routing]] — The complementary approach that decides before any model generates.
*   [[moslem-2026-routing-survey]] — Comprehensive survey that taxonomises cascading as one of six multi-LLM routing paradigms.
*   [[uncertainty-based-routing]] — Uncertainty estimation is the canonical scoring function within a cascade.
