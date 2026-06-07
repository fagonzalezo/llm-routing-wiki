---
type: entity
kind: product
title: "FrugalGPT"
tags: [llm-routing, framework]
sources: [chen-2023-frugalgpt, moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
graph:
  node_type: product
  relationships:
    - predicate: depends_on
      object: concept:llm-cascade
      source: chen-2023-frugalgpt
      evidence: "As an example, we propose FrugalGPT, a simple yet flexible instantiation of LLM cascade"
      confidence: high
      status: current
---

# FrugalGPT

FrugalGPT is a budget-aware pipeline optimization framework introduced by Chen et al. in 2023. It is designed to reduce the cost of running Large Language Model (LLM) queries while maintaining or improving accuracy. FrugalGPT dynamically routes user queries through a cascade of increasingly powerful and expensive models, stopping as soon as a model generates an answer of sufficient quality.

## Architecture & Core Mechanics

FrugalGPT implements the [[llm-cascade]] pattern using three key components:

1.  **Model Sequence**: A predefined list of LLM APIs ordered by increasing cost and performance (e.g., GPT-J, ChatGPT, GPT-4).
2.  **Generation Scorer**: A lightweight, task-specific classifier (such as a fine-tuned DistilBERT model) trained to estimate the probability that a given LLM output is correct for a specific query. The scorer takes both the query and the LLM's generated response as input and outputs a scalar reliability score.
3.  **Threshold-Based Stop Judger**: A decision rule that evaluates the reliability score against a set of optimized thresholds $\{\tau_i\}$. If the score for the $i$-th model's answer is greater than or equal to $\tau_i$, the pipeline terminates, and the answer is returned. Otherwise, the query escalates to the $(i+1)$-th model.

## Optimization & Training

FrugalGPT's routing logic is optimized using a validation or calibration dataset containing queries, model completions, and ground-truth answers.
*   **Threshold Calibration**: The thresholds $\{\tau_i\}$ are optimized as hyperparameters on validation data to maximize downstream accuracy while keeping the average query cost below a user-defined budget limit $b$.
*   **API Downtime Mitigation**: By cascading across multiple providers, FrugalGPT acts as an orchestrator that improves overall service robustness and availability.

## Where this fits
*   [[chen-2023-frugalgpt]] — The original research paper proposing FrugalGPT.
*   [[llm-cascade]] — The core cascade mechanism utilised by FrugalGPT.
*   [[moslem-2026-routing-survey]] — FrugalGPT is listed as the primary cascading case study in the 2026 survey's taxonomy of multi-LLM routing paradigms.
