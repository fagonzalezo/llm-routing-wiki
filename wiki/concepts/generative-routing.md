---
type: concept
title: "Generative-Based Routing"
tags: [llm-routing, generative-routing, model-routing, timing-routing]
sources: [varangot-reille-2025-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Generative-Based Routing

**Generative-based routing** is a family of [[model-routing]] techniques that use the internal states, token outputs, or reasoning capabilities of Large Language Models (LLMs) themselves to make routing decisions, rather than training external, non-generative classifiers (like SVMs, kNN, or BERT-based classifiers).

Because it relies on generative models to determine where to dispatch queries, it can range from zero-shot prompting strategies (which require no training) to supervised fine-tuning of small routing LLMs.

## Key Techniques

According to the classification by Varangot-Reille et al. (2025), generative routing comprises several distinct mechanisms:

### 1. Token Probability Routing
The router estimates model confidence or choice by inspecting the probability distribution of the first generated token. This is often used for binary routing: a small model generates the first token of an answer, and if the token probability falls below a threshold, the query is immediately routed to a larger model.

### 2. Sequence Probability
Instead of checking only the first token, this approach scores and compares the probability of entire generated sequences to judge which model is likely to provide the highest utility.

### 3. Prompt-Based Routing
The simplest implementation of generative routing: a small generalist LLM (the "meta-router") is prompted with a list of candidate models, their capability descriptions, and the user query, and is instructed to output the name of the best candidate. 
- *Advantage*: Zero-shot, highly interpretable, and training-free.
- *Limitation*: Can introduce significant prompt-processing latency and is highly sensitive to prompt formatting and model biases.

### 4. Router Fine-Tuning
A small LLM is explicitly fine-tuned to act as a router. The training targets are target model slugs or routing actions (e.g., "route to GPT-4" vs "route to Llama-3-8B"). This bridges the gap between structured classification and language modeling.

### 5. Repeated Calls (Self-Consistency)
Generating multiple draft responses from one or more models, then selecting the final response or model using consistency checks or secondary LLM-as-a-judge scorers.

### 6. Code Execution Verification
For tool-use or mathematical tasks, the router generates code first. The code is executed in a sandboxed environment; if it runs successfully and passes tests, the response is accepted. If execution fails, the query is escalated to a more powerful model. This serves as a highly robust, non-probabilistic stop criterion in cascades.

## Strengths and Limitations

### Strengths
- **Rich Context Integration**: Generative models can process highly complex, long-context queries and instruction nuances that simple embedding-based classifiers or kNNs struggle to represent.
- **Explainability**: Prompt-based routers can generate natural-language rationales alongside their routing decisions (similar to [[bella]]).
- **Flexibility**: Can adapt to new candidate models by simply updating the router's prompt descriptions.

### Limitations
- **High Latency**: Invoking a generative model to decide where to route another query adds generation time, which can defeat the latency-saving goals of pre-generation routing.
- **Cost**: Generative routing is more computationally expensive than executing a small classifier (like an MLP or kNN search).
- **Stochasticity**: Unless temperature is set to 0 and outputs are strictly parsed, prompt-based routers can output invalid model names or hallucinate.

## Where This Fits

- [[varangot-reille-2025-routing-survey]] — §4.4; primary taxonomy and definition source.
- [[pre-generation-routing]] — Prompt-based and fine-tuned LLM routers are typically run as pre-generation steps.
- [[post-generation-routing]] — Token probability, sequence probability, and code execution are used as stop criteria in cascades.
- [[model-routing]] — parent concept.
- [[llm-cascade]] — generative signals are frequently used to score responses inside cascades.
