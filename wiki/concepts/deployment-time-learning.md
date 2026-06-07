---
type: concept
title: "Deployment-Time Learning"
tags: [llm-routing, deployment-time-learning, online-learning]
sources: [guo-2026-cascade]
created: 2026-06-06
updated: 2026-06-06
---

# Deployment-Time Learning

**Deployment-Time Learning** (DTL) is a paradigm that formalizes online, experiential policy improvement as the third distinct stage in the Large Language Model (LLM) lifecycle, following pre-training and alignment fine-tuning. DTL allows LLM agents to continually learn, adapt, and improve their decision-making from interaction experience and environmental feedback during deployment, without changing the underlying model's weights.

DTL was formally proposed and conceptualized in [[guo-2026-cascade]].

---

## The LLM Lifecycle

In traditional workflows, learning stops when a model is deployed. DTL extends the lifecycle by adding a continuous online learning phase:

```
  ┌─────────────────┐       ┌─────────────────┐       ┌───────────────────────────┐
  │  I. Pre-training │ ────> │  II. Fine-tuning │ ────> │ III. Deployment-Time Lrng │
  │ (Next-Token Pred)│       │  (SFT & RLFT)   │       │   (Online Adaptation)     │
  └─────────────────┘       └─────────────────┘       └───────────────────────────┘
```

1. **Pre-training**: Large-scale next-token prediction on static web corpora.
2. **Fine-tuning**: Supervised Fine-Tuning (SFT) and Reinforcement Learning from Feedback (RLFT) to align models and improve reasoning.
3. **Deployment-Time Learning**: Continuous, parameter-free adaptation during online interactions.

---

## Operational Constraints of DTL

DTL operates under a set of constraints that distinguish it from standard machine learning:

* **Online Stream**: The agent observes tasks sequentially and must act in real-time. It does not have access to future tasks or a pre-defined validation set.
* **Experience-Driven (Weak Feedback)**: Unlike supervised learning which relies on gold-standard labels, DTL is driven by experience, often utilizing simple scalar or binary feedback (e.g., success or failure).
* **Fixed Foundation Model**: The base LLM's parameters remain unchanged. This constraint is critical because modifying model parameters is computationally prohibitive at LLM scale and methodologically impossible when accessing proprietary models via black-box APIs (e.g., OpenAI, Anthropic).

---

## The Locus of Adaptation

Because the base model parameters are frozen, the locus of learning shifts to the **agentic components** that surround the model:

* **Prompts & In-Context Exemplars**: Dynamically selecting which demonstrations, instructions, or rules are passed to the model.
* **Memory Systems**: Accumulating a database of past successful interactions (episodic memory) to guide future tasks.
* **Retrieval Policies**: Adapting the mechanism that determines which memory elements or tools are selected for a given query.
* **Decision-Making Wrappers**: Contextual bandits or online reinforcement learning policies that sit between the user query and the LLM API.

---

## Comparison with Related Paradigms

| Paradigm | Learns Across Tasks? | Updates Model Weights? | Operational Phase | Examples |
| :--- | :---: | :---: | :---: | :--- |
| **Supervised / RL Fine-Tuning** | Yes | Yes | Offline (Pre-deployment) | SFT, RLHF, DPO |
| **Offline Agent Optimization** | Yes (on train set) | No | Offline (Pre-deployment) | DSPy, GEPA |
| **Test-Time Adaptation** | No (single-query) | No | Online (Deployment) | Reflexion, TextGrad |
| **Deployment-Time Learning (DTL)** | **Yes** | **No** | **Online (Deployment)** | **[[cascade]]**, LLM Bandit |

---

## Instantiations

* **Case-Based Reasoning (CBR) with Bandits**: The **[[cascade]]** framework is a core instantiation of DTL. It represents successful past experiences in an episodic memory bank and uses a contextual bandit algorithm to learn which case to retrieve for a new query.
* **Online Prompt Optimization**: Dynamically adjusting instructions or routing paths based on streaming performance metrics.
* **Adaptive Tool Selection**: Learning which external tools (APIs, calculators, search engines) are most effective for different query contexts under online usage constraints.

---

## See Also

* [[guo-2026-cascade]] — The foundational paper on DTL.
* [[cascade]] — A case-based, contextual bandit instantiation of DTL.
* [[model-routing]] — Selecting and dispatching queries to suitable models.
* [[dynamic-routing]] — Model routing when the pool of candidate LLMs varies dynamically.
