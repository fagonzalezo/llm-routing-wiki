---
type: source
title: "Online Multi-LLM Selection via Contextual Bandits Under Unstructured Context Evolution"
authors: ["Manhin Poon", "Xiangxiang Dai", "Xutong Liu", "Fang Kong", "John C.S. Lui", "Jinhang Zuo"]
url: "https://arxiv.org/abs/2506.17670"
raw: "raw/Poon 2026 - Online Multi-LLM Selection via Contextual Bandits Under Unstructured Context Evolution.pdf"
ingested: 2026-06-06
tags: [llm-routing, contextual-bandits, online-learning, multi-step-interaction, cost-optimization, regret-minimization]
entities: []
concepts: [contextual-bandits-routing, model-routing, deployment-time-learning, llm-cascade]
created: 2026-06-06
updated: 2026-06-06
---

# Online Multi-LLM Selection via Contextual Bandits Under Unstructured Context Evolution

**Poon et al. (2026) — AAAI-26**

## Summary

This paper proposes the first contextual bandit framework for *sequential*, multi-step LLM selection under **unstructured context evolution** — a realistic setting in which the prompt changes dynamically after each model response through a black-box, potentially stochastic process that cannot be modeled or simulated. The key insight is that because future prompts are unpredictable (the evolution function `g` is non-differentiable, non-stationary, and often proprietary), conventional planning-based methods such as reinforcement learning are unsuitable. Instead, the authors decompose the interaction into a sequence of myopic, per-step decisions and introduce a new regret notion — **myopic regret** — that makes the problem theoretically tractable without requiring trajectory modeling.

## Problem Setting

The system interacts with users over T rounds, each consisting of up to H multi-step exchanges. At each step `h` of round `t`, the learner observes a prompt context vector `x_{t,h} ∈ ℝ^d`, selects one of K LLMs, receives binary satisfaction feedback `r_{t,h} ∈ {0,1}`, and then observes the next context `x_{t,h+1} = g(x_{t,h}, a_{t,h}, R_{t,h}, r_{t,h})` — where `g` is the unstructured black-box context-evolution function. A linear reward model is assumed: `E[r_{t,h} | x_{t,h}, a_{t,h}] = <x_{t,h}, theta*_{a_{t,h}}>`. The interaction terminates when the user is satisfied (`r = 1`) or after H steps.

## Key Contributions

### 1. Myopic Regret Formulation
Rather than tracking sequence-wise regret (which requires modeling `g`), the paper defines **myopic regret** as the per-step shortfall compared to the best LLM for the *current* context:

```
Reg_{t,h} = max_k <x_{t,h}, theta*_k> - <x_{t,h}, theta*_{a_{t,h}}>
```

Total myopic regret is summed across all T rounds and H steps. This avoids the combinatorial complexity of trajectory regret and keeps the problem tractable without assumptions on future context evolution.

### 2. Greedy LinUCB Algorithm
The core algorithm maintains a separate ridge-regression model `(A_k, b_k)` for each LLM k. At each step it computes an Upper Confidence Bound:

```
UCB_k = <x_{t,h}, theta_hat_k> + alpha * sqrt(x_{t,h}^T A_k^{-1} x_{t,h})
```

and selects the arm with the highest UCB. After observing feedback, it updates the matrices for the selected LLM.

**Regret bound (Theorem 1):** With probability >= 1-delta:

```
R(T) = O(d * sqrt(KTH) * (SL + sqrt(lambda*S)) * log(KTL^2 / lambda*delta))
```

This matches standard LinUCB bounds up to an additional sqrt(H) factor for the multi-step setting.

### 3. Budget-Aware Extension
Extends to settings where each LLM query incurs a stochastic cost drawn from an unknown distribution. The score for arm selection becomes:

```
Score_k = UCB_k(x_{t,h}) / max{c_hat_k - beta_k, epsilon}
```

where `c_hat_k` is the empirical cost mean and `beta_k` is its confidence interval. Arms with upper-bound cost exceeding the remaining budget are excluded. The resulting regret decomposes into a reward term `O~(dSL*sqrt(KTH))` and a cost-estimation term growing with sqrt(T) amplified by small mean costs.

### 4. Positionally-Aware Knapsack Heuristic (PAKH)
Introduces a heuristic that incorporates **positional utility** — the empirical observation that users prefer high-quality responses *early* in a multi-turn interaction and may disengage if early attempts fail. PAKH integrates UCB reward scores and cost estimates into a dynamic knapsack-style allocation across steps, prioritizing early deployment of capable models rather than deferring them to save budget.

## Methodology & Experiments

Experiments span diverse benchmarks (including GPQA, MMLU-Pro, and others) using models of varying capability and cost. The paper evaluates accuracy, cost-efficiency, and performance across the three algorithm variants. Results show consistent outperformance over existing LLM routing strategies — including static policies, offline-trained classifiers, and stateless multi-turn methods like AutoMix and MixLLM — in both accuracy and cost-efficiency. Ablations confirm that tracking context evolution provides meaningful signal over turn-independent baselines.

## Theoretical Novelty

- First paper to formally define the **unstructured context evolution** problem for LLM routing and to show why RL-based methods are inapplicable.
- Introduces **myopic regret** as a practical and theoretically grounded alternative to sequence-wise regret in interactive, multi-step LLM settings.
- Achieves provably sublinear regret without offline training, model internals access, or context evolution modeling.

## Positioning & Comparisons

| Approach | Offline Training | Multi-step | Context-Aware | Online Adaptation | Proven Sublinear Regret |
|:---|:---:|:---:|:---:|:---:|:---:|
| Static classifiers (e.g., RouteLLM) | Yes | No | Partial | No | No |
| AutoMix / MixLLM | Yes | Stateless | No | No | No |
| Bandit-based (prior, e.g. Dai 2024) | Partial | No | Partial | Yes | Partial |
| **Poon 2026 (this work)** | No | Yes | Yes | Yes | Yes |

## Where This Fits

This paper slots directly into the **[[model-routing]]** research area, extending it to multi-step online sequential decision-making. It is closely related to **[[deployment-time-learning]]** (learning from deployment-time feedback without offline datasets) and **[[contextual-bandits-routing]]** (the specific bandit methodology it formalizes and champions). The budget-aware extension overlaps with the cost-optimization themes in **[[frugalgpt]]** and **[[bella]]**, while the cascade-like multi-step structure echoes **[[llm-cascade]]** and **[[cascade]]** — though unlike CASCADE, this work uses no episodic memory and makes no use of model internals.

The notion of a black-box, unlearnable context-evolution function is new to this wiki and represents a distinct challenge beyond the dynamic pool setting studied in **[[uniroute]]** or **[[dynamic-routing]]**.
