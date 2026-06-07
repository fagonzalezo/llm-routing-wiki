---
type: concept
title: "Dynamic Routing"
tags: [llm-routing, routing-framework]
sources: [jitkrittum-2026-universal-routing, moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Dynamic Routing

**Dynamic Routing** (or routing with a dynamic model pool) is a paradigm in large language model (LLM) routing where the set of candidate models available for selection can change at test time. This contrasts with static routing, which assumes a fixed pool of LLMs that are known during both router training and deployment.

In dynamic routing settings, new models can be added (e.g., when a more performant or cheaper model is released) and old models can be deprecated (e.g., due to serving hardware limits, GPU availability, licensing, or API deprecation) without requiring the router to be retrained from scratch.

## Key Challenges

1. **Retraining Overhead**: Traditional static routers (e.g., MLPs, Matrix Factorization, or BERT-based classification models) have a fixed output dimension (one output per model). Adding or removing a model requires modifying the network architecture, labeling training data with the new model, and retraining the entire router.
2. **Label Efficiency**: Obtaining correctness labels for a new model on a large training corpus is computationally expensive. Dynamic routing frameworks aim to profile new models using only a very small validation sample ($O(10^2)$ to $O(10^3)$ prompts).
3. **Overfitting**: Standard routers retrained on small validation samples are highly susceptible to overfitting, leading to degraded performance at test time.

## Mathematical Formulation

As proved in [[jitkrittum-2026-universal-routing]], under mild conditions, the Bayes-optimal routing rule for a dynamic LLM pool $H$ decomposes across individual models. Given prompt $x$, candidate pool $H$, and a cost-quality trade-off parameter $\lambda_H \geq 0$, the optimal router $r^*$ chooses the model that minimizes the cost-adjusted expected loss:
$$r^*(x, H) = \operatorname{argmin}_{m} [ P(y \neq h^{(m)}(x) | x) + \lambda_H \cdot c(h^{(m)}) ]$$
where $c(h)$ is the inference cost of model $h$.

## Approaches & Frameworks

- **[[uniroute]]**: Represents LLMs as feature vectors based on their average prediction errors on prompt clusters obtained from validation samples. By learning a bilinear scoring function, it can perform zero-shot routing over new models.
- **K-Nearest Neighbors (K-NN) Router**: A non-parametric router that estimates model performance for an input prompt by averaging the accuracy of validation prompts closest to it in embedding space. It requires no retraining but can underperform due to local estimation variance.
- **LLM Bandit**: A reinforcement-learning-based policy gradient approach for dynamic routing that updates routing decisions online.

[[moslem-2026-routing-survey]] classifies dynamic-pool routing under the *clustering-based* and *RL-based* paradigms, noting that bandit methods (e.g., TI-UCB, MetaLLM) are especially suited to settings with shifting model pools, since they update routing decisions from deployment-time feedback without requiring a fixed output space. See [[rl-based-routing]] for details.
