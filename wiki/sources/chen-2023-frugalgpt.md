---
type: source
title: "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance"
authors:
  - "Lingjiao Chen"
  - "Matei Zaharia"
  - "James Zou"
url: "https://arxiv.org/abs/2305.05176"
raw: "raw/Chen 2023 - FrugalGPT How to Use Large Language Models More Cheaply and Get Better Results.pdf"
ingested: 2026-06-06
tags: [llm-routing, cost-optimization, llm-cascade]
created: 2026-06-06
updated: 2026-06-06
---

# FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

FrugalGPT is a research framework developed by researchers at Stanford University (Chen, Zaharia, and Zou) to address the high financial and computational costs of querying commercial Large Language Model (LLM) APIs. The paper proposes three classes of strategies—**prompt adaptation**, **LLM approximation**, and **LLM cascades**—and introduces [[frugalgpt]] as a concrete instantiation of a learned LLM cascade. The experiments demonstrate that FrugalGPT can match the accuracy of the best individual model (e.g., GPT-4) while reducing costs by up to 98%, or improve accuracy over GPT-4 by 4% under the same cost budget.

## Problem Formulation & Cost Heterogeneity

The authors formalize the problem of **budget-aware LLM API usage**. Given a natural language query $q$ from a distribution $\mathcal{Q}$ and $K$ different commercial LLM APIs $\{f_i(\cdot)\}_{i=1}^K$, the goal is to find a routing/generation strategy $s$ that maximizes expected accuracy or reward:

$$\max_{s} \mathbb{E}_{(q, a) \sim \mathcal{Q} \times \mathcal{A}} [r(a, \hat{a}(s, q))]$$

subject to a user-defined cost budget constraint $b$:

$$\mathbb{E}_{q \sim \mathcal{Q}} [c(s, q)] \le b$$

where:
* $a$ is the ground-truth answer.
* $\hat{a}(s, q)$ is the generated answer under strategy $s$.
* $c(s, q)$ is the query cost under strategy $s$.
* $r(\cdot, \cdot)$ is a performance reward function.

### Cost Model
The cost of querying a single API $f_i$ using prompt $p$ is defined as:

$$c_i(p) \triangleq \tilde{c}_{i,2} \|f_i(p)\| + \tilde{c}_{i,1} \|p\| + \tilde{c}_{i,0}$$

where $\tilde{c}_{i,1}$ is the prompt cost per token, $\tilde{c}_{i,2}$ is the generation cost per token, and $\tilde{c}_{i,0}$ is a flat fee per query. 

The authors document that pricing is highly heterogeneous across providers (e.g., OpenAI, AI21, CoHere, Textsynth), with prompt costs differing by up to two orders of magnitude (e.g., $30 per 10M tokens for GPT-4 vs. $0.20 per 10M tokens for GPT-J hosted on Textsynth).

---

## Cost-Saving Strategies

The paper outlines three main strategies for reducing LLM inference costs:

### 1. Prompt Adaptation
Prompt adaptation optimizes the input sent to the LLM to minimize prompt token count:
*   **Prompt Selection**: Identifying and utilizing only a high-quality subset of in-context examples (few-shot exemplars) rather than long, exhaustive prompts.
*   **Query Concatenation**: Combining multiple queries into a single API call to share overhead prompt contexts.

### 2. LLM Approximation
LLM approximation aims to mimic high-performing, expensive models using cheaper alternatives:
*   **Completion Cache**: Storing and reusing past LLM responses for semantically identical or highly similar queries.
*   **Model Fine-Tuning**: Using outputs from expensive models (like GPT-4) to fine-tune smaller, open-source models (like GPT-J) on task-specific datasets.

### 3. LLM Cascade
An **LLM cascade** (detailed in [[llm-cascade]]) is a dynamic sequential routing mechanism:
1.  **Sequential Querying**: A query is sent to a sequence of models starting with the cheapest/lightest model (e.g., GPT-J -> ChatGPT -> GPT-4).
2.  **Quality Assessment**: A lightweight scorer (e.g., a fine-tuned DistilBERT classifier) evaluates the quality/reliability of the generated answer.
3.  **Threshold-Based Stop**: If the reliability score exceeds a calibrated threshold $\tau_i$, the cascade stops and accepts the answer. Otherwise, it escalates the query to the next, more powerful model in the sequence.
4.  **Threshold Calibration**: The thresholds are optimized using validation data to find the optimal trade-off between cost and performance.

---

## Experimental Results

The framework was evaluated across multiple query-answering datasets (including HEADLINES, CoQA, and others) using combinations of 12 commercial APIs.
*   **Cost Reductions**: On the HEADLINES financial news classification dataset, FrugalGPT matched GPT-4's accuracy while reducing costs by 98%.
*   **Accuracy Enhancements**: Under a budget constraint equivalent to the cost of GPT-4, FrugalGPT improved accuracy over GPT-4 by 4% by routing complex queries through combinations of models and prompt strategies.
*   **Reliability**: Multi-provider cascading mitigates single-API downtime risks, improving application availability.

## Where this fits
*   [[frugalgpt]] — The specific cascade implementation proposed in this paper.
*   [[llm-cascade]] — The core algorithmic concept of cascading models sequentially.
