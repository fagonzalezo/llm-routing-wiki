---
type: entity
kind: product
title: "UniRoute"
tags: [llm-routing, routing-framework]
sources: [jitkrittum-2026-universal-routing]
created: 2026-06-06
updated: 2026-06-06
---

# UniRoute

**UniRoute** (Universal Routing) is an LLM routing framework designed for **[[dynamic-routing]]** settings, where the set of candidate LLMs varies at test time (e.g., when models are added, removed, or deprecated). Introduced in [[jitkrittum-2026-universal-routing]], UniRoute represents both prompts and LLMs as feature vectors in a shared space to predict routing performance without requiring router retraining for new models.

## Architecture & Core Mechanics

UniRoute models the performance of a candidate LLM $h$ on prompt $x$ using a bilinear form:
$$\gamma_{uni}(x, h) = \Phi(x)^\top \Psi(h)$$
where:
- $\Phi(x) \in \mathbb{R}^K$ is a prompt embedding representing the input.
- $\Psi(h) \in \mathbb{R}^K$ is the LLM feature representation.

### LLM Capability Profiling
UniRoute profiles the capabilities of an LLM by evaluating its performance on a small validation set $S_{val}$ (typically $O(10^2)$ to $O(10^3)$ prompts). The model is represented by its prediction error vector (a correctness profile) across these prompts:
$$\Psi(h) = F([1(y^{(j)} \neq h(x^{(j)}))]_{j \in [N_{val}]})$$
This allows the router to leverage any new, black-box LLM at test time simply by evaluating it on the validation set once, bypassing the need for gradient updates or retraining.

### Model Variants
1. **UniRoute (K-Means)**: 
   - An unsupervised approach that clusters prompt embeddings from the training set $S_{tr}$ using K-Means.
   - Validation set prompts are assigned to these clusters.
   - The LLM representation $\Psi(h)$ is the vector of average per-cluster errors of the model on the validation set.
2. **UniRoute (LearnedMap)**:
   - A supervised approach that replaces the hard K-Means mapping with a parameterized soft-cluster assignment map $\Phi_{clust}(x; \theta) \propto \exp(\theta_k^\top \phi(x))$.
   - The mapping parameters $\theta$ are trained on the training set $S_{tr}$ using correctness labels from training LLMs to minimize cross-entropy loss.

## Performance & Evaluation

UniRoute was evaluated against traditional static and dynamic routers (such as K-NN and ZeroRouter) on datasets like EmbedLLM (comprising over 30 unseen LLMs at test time) and SPROUT o3-mini:
- **Zero-Shot Routing**: UniRoute routes to unseen models at test time, achieving a Quality-Neutral Cost (QNC) of **33.1%** on EmbedLLM compared to **45.9%** for K-NN and **87.5%** for ZeroRouter.
- **Robustness**: Unlike static MLP and Matrix Factorization routers that overfit when retrained on small validation sets, UniRoute generalizes effectively with minimal validation samples ($N_{val} \approx 400$).
- **Cost-Efficiency**: UniRoute achieves the performance of the largest model (Qwen2.5-72B-Instruct) at **80.2%** of its cost, outperforming RL-based policy gradient methods (LLM Bandit).
