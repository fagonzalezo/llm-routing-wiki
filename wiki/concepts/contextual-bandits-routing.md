---
type: concept
title: "Contextual Bandits for LLM Routing"
tags: [llm-routing, contextual-bandits, online-learning, regret-minimization, multi-step-interaction]
sources: [poon-2026-contextual-bandits]
created: 2026-06-06
updated: 2026-06-06
---

# Contextual Bandits for LLM Routing

**Contextual Bandits for LLM Routing** is an online learning approach to the model selection problem in which the router is formalized as a contextual bandit agent that learns which LLM to select for each query by continuously improving from deployment-time feedback — without offline training, model internals, or access to future query information.

This approach is distinct from purely static routing (which trains a classifier offline) and from reinforcement learning approaches (which require a simulatable environment). It occupies the middle ground: stateful, adaptive, and theoretically grounded, but requiring neither historical datasets nor a model of how interactions evolve.

## Core Setup

- **Arms**: The K available LLMs, each with an unknown preference vector `theta*_k` capturing its alignment with user preferences across prompt contexts.
- **Context**: A `d`-dimensional feature vector `x_t` derived from the current prompt (e.g., an embedding).
- **Reward**: Binary user satisfaction `r ∈ {0, 1}` observed after each LLM response.
- **Feedback loop**: The agent selects an arm, observes the reward, and updates its estimates. No label curation or offline replay is needed.

## LinUCB as the Core Mechanism

The most natural algorithm family for this setting is **LinUCB**, which assumes a linear relationship between the context vector and the expected reward for each LLM:

```
E[r | x, k] = <x, theta*_k>
```

At each step, the algorithm computes an Upper Confidence Bound for each LLM combining the predicted reward with an exploration bonus inversely proportional to how many times that LLM has been queried in similar contexts. This drives exploration of under-tested LLMs while exploiting known high-performers.

## Multi-Step Extension: Myopic Regret

A key difficulty in applying bandits to multi-turn LLM interactions is that the prompt evolves between steps in a black-box, unlearnable way (the **unstructured context evolution** problem). Because future prompts cannot be predicted, sequence-level planning is infeasible.

[[poon-2026-contextual-bandits]] addresses this by introducing **myopic regret**: rather than comparing the agent's full trajectory to the optimal sequence, regret is measured per decision step against the best LLM for the *current* context. This makes the problem tractable without modeling how contexts evolve and allows provably sublinear regret bounds even in unstructured sequential environments.

The myopic regret of the Greedy LinUCB algorithm satisfies (with high probability):

```
R(T) = O(d * sqrt(KTH) * log(KTL^2 / lambda*delta))
```

where T = total rounds, H = max steps per round, K = number of LLMs, d = context dimensionality.

## Extensions

### Budget-Aware Contextual Bandits
When LLM queries have stochastic, unknown costs, the arm-selection criterion is extended to a **cost-normalized UCB score**:

```
Score_k = UCB_k / max{cost_estimate_k - confidence_k, epsilon}
```

The oracle at each step is the highest expected-reward-per-unit-cost arm whose upper-bound cost fits within the remaining budget. This introduces a second confidence interval (on cost) alongside the reward confidence, creating a two-level optimism mechanism.

### Positionally-Aware Selection (PAKH)
Users exhibit **positional bias** — they value high-quality early responses more than late ones. The Positionally-Aware Knapsack Heuristic (PAKH) incorporates positional utility into the arm-selection policy, front-loading capable (but costly) models rather than deferring them.

## Relationship to Prior Bandit Approaches in LLM Routing

Prior works (e.g., Dai 2024, Nguyen 2024, Xia 2024) apply bandits to LLM routing in single-step or stateless multi-turn settings. The contextual bandit framing in [[poon-2026-contextual-bandits]] is distinguished by:

1. **Sequential, stateful context**: the bandit operates on evolving prompts, not i.i.d. queries.
2. **Unstructured evolution**: no assumptions on how context changes between steps.
3. **Myopic regret**: a new theoretical construct enabling rigorous analysis without trajectory modeling.
4. **Budget and positional extensions**: practical deployability in cost-constrained environments.

## Comparison with Related Approaches

| Approach | Training | Stateful | Budget-Aware | Proven Sublinear Regret |
|:---|:---:|:---:|:---:|:---:|
| Offline classifier (e.g., RouteLLM) | Offline | No | Partial | No |
| RL-based (requires env model) | Online | Yes | Partial | Problem-specific |
| Prior bandit routing (single-step) | Online | No | Partial | Yes (i.i.d. contexts) |
| **Greedy LinUCB (Poon 2026)** | Online | Yes | Yes (extension) | Yes (myopic) |

## See Also

- [[poon-2026-contextual-bandits]] — Foundational paper introducing this framework.
- [[model-routing]] — The broader paradigm of dispatching queries to the best LLM.
- [[deployment-time-learning]] — Umbrella concept for online adaptation without weight updates.
- [[dynamic-routing]] — Routing when the candidate pool changes at test time.
- [[llm-cascade]] — Sequential routing that also queries models in steps.
