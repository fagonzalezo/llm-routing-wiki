---
type: entity
title: "Group-Adaptive Policy Gradient"
tags: [llm-routing, reinforcement-learning, edge-ai, policy-gradient]
sources: [fang-2025-device-cloud]
created: 2026-06-06
updated: 2026-06-06
---

# Group-Adaptive Policy Gradient (GAPG)

**Group-Adaptive Policy Gradient (GAPG)** is a reinforcement learning (RL) post-training algorithm designed to jointly optimize a lightweight on-device LLM's task-solving capabilities and its collaboration strategies with a cloud LLM. Introduced in [[fang-2025-device-cloud]], GAPG embeds query routing decisions directly into the on-device model, eliminating the need for separate external classifiers.

## Core Mechanisms

GAPG addresses the optimization challenges of collaborative device-cloud LLM systems through two main components:

### 1. Group-Level Policy Gradient Estimator
Standard policy gradient algorithms (like GRPO) use standard-deviation normalization to scale token-level advantages:
$$A_i = \frac{r_i - \text{mean}(\{r\})}{\text{std}(\{r\})}$$
In collaborative settings with hierarchical rewards, this normalization distorts the true values of different responses. For example, a group with an independent correct answer (reward $\alpha_a = 2.0$) and a group with a cloud-offloaded correct answer (reward $\alpha_c = 0.5$) might receive identical normalized advantages. This leads to policy collapse, where the model over-relies on the cloud LLM.

GAPG avoids this distortion by employing an unbiased, non-normalized group gradient estimator derived via the log-likelihood trick:
$$\nabla_\theta R(\theta, x) = \frac{G}{G - 1} \frac{1}{G} \sum_{i=1}^G \nabla_\theta \log \pi_\theta(y_{\theta, i} | x) (r_i - \bar{r})$$
where:
* $G$ is the group size of sampled completions (typically $G \ge 8$).
* $r_i$ is the reward for response $i$.
* $\bar{r}$ is the mean reward of the group.

Removing the standard-deviation denominator preserves the absolute reward hierarchy, ensuring the model prefers independent correct solving over cloud offloading.

### 2. Adaptive Prompt Filtering
To prevent over-reliance on the cloud and strictly enforce a cloud offloading budget $\rho$, GAPG filters training prompts in each batch $D_b$ into two dynamic subsets:
* **Set $D_b^1$ (Local Success)**: Prompts where at least one response in the group of size $G$ is generated correctly by the local model $\pi_\theta$ alone. Training on these prompts reinforces independent problem-solving.
* **Set $D_b^2$ (Cloud Escalation)**: Prompts where the local model fails on all group responses, but the cloud model $\pi_c$ yields a correct answer. The size of this set is capped at $\rho |D_b^1|$ to satisfy the budget constraint.

The policy parameters $\theta$ are updated via gradient ascent only on prompts in $D_b^1 \cup D_b^2$.

## Key Advantages
* **Unified Post-Training**: Routing logic and task-solving are optimized together in a single stage, avoiding separate training steps for routers.
* **Preservation of Edge Compute (Early Exit)**: Rather than completing a full reasoning chain before routing, models trained with GAPG learn to halt early and generate a cloud call tag (`<unknown> I need external assistance </unknown>`) when confidence is low.
* **Robustness & Generalization**: Unlike binary classifier routers that overfit to query surface patterns, GAPG leverages the model's inner reasoning path to make offloading decisions.

## See Also
* [[fang-2025-device-cloud]] — The research paper introducing GAPG.
* [[collaborative-inference]] — The concept of coordinating workloads between edge devices and the cloud.
* [[model-routing]] — The general paradigm of dispatching queries to suitable models.
* [[llm-cascade]] — Sequential execution and confidence-based escalation.
