---
type: source
title: "Collaborative Device-Cloud LLM Inference through Reinforcement Learning"
authors: ["Anonymous"]
url: ""
raw: "raw/Fang 2025 - Collaborative Device-Cloud LLM Inference through Reinforcement Learning.pdf"
ingested: 2026-06-06
tags: [llm-routing, device-cloud-collaboration, reinforcement-learning, policy-gradient, math-reasoning]
entities: [gapg]
concepts: [model-routing, llm-cascade, collaborative-inference]
created: 2026-06-06
updated: 2026-06-06
---

# Collaborative Device-Cloud LLM Inference through Reinforcement Learning

## Summary
This paper (submitted to ICLR 2026) proposes a unified reinforcement learning (RL) post-training framework that allows a lightweight on-device LLM ($\pi_\theta$) to coordinate dynamically with a powerful cloud LLM ($\pi_c$). Instead of relying on decoupled external routers (which often struggle to predict task difficulty from prompt surface features), the on-device model is fine-tuned to either solve the problem independently or call for cloud assistance at the end of (or during) its own reasoning process. 

To achieve this, the authors frame collaboration as a constrained reward maximization problem. They identify that standard [[dynamic-routing]] or post-training algorithms like Group Relative Policy Optimization ([[routellm]] / GRPO) fail in this setting due to standard-deviation normalization distorting hierarchical rewards and the lack of budget enforcement. To resolve this, they introduce the **[[gapg]]** (Group-Adaptive Policy Gradient) algorithm, featuring an unbiased group-level policy gradient estimator and an **Adaptive Prompt Filtering** mechanism to satisfy the cloud budget constraint.

## Key Claims & Contributions
* **Intrinsic Routing Model**: Rather than training a separate classifier, the routing capability is embedded directly into the on-device LLM during post-training, simplifying system complexity and leveraging the model's self-assessment capability.
* **Failure Analysis of GRPO**: Proves that standard GRPO's variance normalization distorts hierarchical rewards, treating independent correct answers and offloaded correct answers with equal advantage. This causes the policy to collapse into over-relying on the cloud.
* **Group-Adaptive Policy Gradient (GAPG)**: A novel policy gradient algorithm that uses an unbiased, non-normalized group gradient estimator combined with adaptive prompt filtering to enforce a hard cloud offloading budget $\rho$.
* **Emergent Early-Exit Behavior**: Demonstrates that the on-device model naturally learns to stop generating and call the cloud early in the reasoning chain when faced with highly complex queries, preserving local device compute resources.
* **Empirical Benefits**: Outperforms classical two-stage routing classifiers (e.g., DeBERTa-v3-large) by 6–8% on average across math benchmarks, achieving performance close to a pure cloud model while respecting a strict 30% offloading budget.

## Methodology & Formulation

### Problem Formulation
The goal is to maximize the expected task reward of the collaborative system under a budget constraint on the frequency of cloud LLM invocations:
$$\max_{\theta} \mathbb{E}_{x \sim D} [R(\theta, x)] := \mathbb{E}_{x \sim D} \mathbb{E}_{y_\theta \sim \pi_\theta(x)} [r(x, y)]$$
$$\text{subject to } \mathbb{E}[1_{\{y \sim (\pi_\theta, \pi_c)\}}] \le \rho \mathbb{E}[1_{\{y \sim \pi_\theta\}}]$$
where:
* $D$ is the prompt dataset.
* $r(x, y)$ is a collaboration-aware hierarchical reward.
* $y$ is the complete response, generated either solely by the on-device LLM ($y = y_\theta$) or collaboratively ($y = [y_\theta, y_c]$).
* $\rho$ governs the maximum allowed ratio of cloud calls to local generations.

### Collaboration-Aware Hierarchical Reward
The reward function $r(x, y)$ incentivizes correct answers, structural formatting, and cost-effective collaboration:
$$r(x, y) = \begin{cases} 
\alpha_a + \alpha_f & \text{if } y = y_\theta \text{ is correct and formatted} \\ 
\alpha_a & \text{if } y = y_\theta \text{ is correct but violates format} \\ 
\alpha_c & \text{if } y = [y_\theta, y_c] \text{ is correct (cloud assisted)} \\ 
\alpha_f & \text{if } y = y_\theta \text{ is incorrect but formatted} \\ 
0 & \text{otherwise} 
\end{cases}$$
To prioritize local accuracy over offloading, weights are set such that $\alpha_a > \alpha_c > \alpha_f$ (e.g., $\alpha_a = 2.0$, $\alpha_c = 0.5$, $\alpha_f = 0.2$ for Countdown).

### Group-Adaptive Policy Gradient (GAPG)
GAPG addresses optimization stability and budget constraints through two core mechanisms:

#### 1. Group-Level Policy Gradient Estimator
Instead of normalizing by standard deviation (which distorts relative advantages), the gradient is computed using an unbiased group-based estimator derived from the log-likelihood trick:
$$\nabla_\theta R(\theta, x) = \frac{G}{G - 1} \frac{1}{G} \sum_{i=1}^G \nabla_\theta \log \pi_\theta(y_{\theta, i} | x) (r_i - \bar{r})$$
where $G$ is the group size, $r_i$ is the reward of completion $i$, and $\bar{r} = \frac{1}{G} \sum_{j=1}^G r_j$ is the group mean. Removing the standard-deviation denominator preserves the true absolute difference between independent solving ($\alpha_a$) and offloading ($\alpha_c$).

#### 2. Adaptive Prompt Filtering
To satisfy the budget constraint during offline post-training, the batch of sampled prompts $D_b$ is dynamically filtered into two subsets before updating the model:
* **Set $D_b^1$**: Prompts where at least one response in the group is correctly solved by the local model $\pi_\theta$ alone. (Teaches independent problem-solving).
* **Set $D_b^2$**: Prompts where the local model fails on all group responses, but the cloud model $\pi_c$ yields a correct answer. To enforce the budget, the size of this set is constrained to at most $\rho |D_b^1|$ prompts.
The policy update is performed only on prompts in $D_b^1 \cup D_b^2$.

## Empirical Evaluation
* **Tasks & Benchmarks**: 
  * Countdown (math game, 5K train / 1K test).
  * MATH-lighteval (12.5K problems, 7.5K train / 5K test).
  * Out-of-distribution evaluation: MATH-500, AMC23, AIME24, MinervaMath.
* **Models**: 
  * Cloud model: DeepSeek-R1.
  * On-device models: Qwen2.5-3B-Instruct (Countdown), Llama-3.2-1B-Instruct, Qwen2.5-1.5B-Instruct, Llama-3.2-3B-Instruct (MATH).
* **Results**:
  * **Inference Efficiency**: At a 30% cloud budget, GAPG improves on-device model accuracy by up to 30% on Countdown, narrowing the gap to the pure cloud upper bound.
  * **Generalization**: When evaluated on mathematical benchmarks, GAPG out-performed a two-stage classifier baseline (DeBERTa-v3-large) by an average of 6–8%. For instance, on Qwen2.5-1.5B, GAPG achieved 56.2% average accuracy vs. 51.6% for the Router and 33.3% for Task-Tuning Only.
  * **Routing Behavior**: Case studies confirm that on-device models trained with GAPG can exit early. For example, faced with a highly complex algebra problem, the model outputs a few steps of initial setup and then generates the `<unknown> I need external assistance </unknown>` tag, avoiding wasting compute cycles on a problem it cannot solve.

## Where this fits
* **Links**:
  * [[model-routing]] — GAPG represents an intrinsic on-device routing architecture.
  * [[llm-cascade]] — The collaborative device-cloud system operates as an end-to-end learned, confidence-based cascading mechanism with early-exit capability.
* **Entities**:
  * [[gapg]] — The Group-Adaptive Policy Gradient algorithm introduced in this source.
  * [[routellm]] — A comparative baseline framework that relies on external classifiers trained on preference data.
* **Concepts**:
  * [[collaborative-inference]] — The paradigm of splitting model workloads between edge devices and the cloud dynamically.
