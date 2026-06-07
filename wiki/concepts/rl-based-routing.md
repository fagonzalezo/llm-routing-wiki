---
type: concept
title: "RL-Based Routing"
tags: [llm-routing, reinforcement-learning, online-learning, bandit]
sources: [moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# RL-Based Routing

**RL-Based Routing** is a class of [[model-routing]] methods that learn or adapt routing policies through reinforcement learning (RL) signals, rather than relying on fixed supervised classifiers or heuristics. The defining property is that the routing policy improves over time through interaction with the environment — either during training (offline RL) or continuously during deployment (online bandit/RL).

## Motivation

Static classifiers trained on historical preference data cannot adapt when the deployment distribution shifts, when new models are added, or when ground-truth feedback is only available after significant delay. RL framing allows routing to improve continuously from whatever reward signal is available (binary correctness, user satisfaction, task completion).

## Sub-Paradigms

### Policy-Gradient Methods (Offline/Online RL)
Methods such as PPO and GRPO optimise a routing policy end-to-end with a reward signal measuring downstream task quality. Examples from [[moslem-2026-routing-survey]]:

- **Router-R1** and **R2-Reasoner**: Train routing policies using GRPO-style policy optimisation, rewarding correct model selection.
- **SCOPE**, **MixLLM**, **PILOT**: Policy-gradient approaches targeting cost-quality Pareto efficiency.
- **GreenServ**: RL-based routing optimised for energy efficiency in multi-model inference.

### Bandit Methods (Online Adaptive)
Contextual and multi-armed bandit algorithms update routing online without full RL overhead. They are especially suited to settings where:
- The model pool changes at test time.
- Ground-truth labels arrive with delay.
- Exploration vs. exploitation of model capabilities must be balanced.

Examples:
- **MetaLLM**: Treats model selection as a contextual bandit problem.
- **Dueling Feedback**: Uses pairwise preference feedback (rather than scalar reward) in a dueling bandit framework.
- **TI-UCB**: UCB-style bandit maintaining per-model confidence bounds updated after each query.

## Relationship to the Three-Dimensional Framework

Within the conceptual framework of [[moslem-2026-routing-survey]]:

| Dimension | Typical RL/Bandit Routing Placement |
|---|---|
| **When** | Pre-generation (policy selects model before generation) or Online/adaptive |
| **What** | Query features + accumulated feedback over time |
| **How** | Bandit algorithm (UCB, dueling) or RL policy (PPO, GRPO) |

Bandit methods are the most deployment-friendly: they require no offline training and update from sparse, delayed feedback. Full policy-gradient methods require a differentiable reward and a training loop, but can learn more complex routing behaviours.

## Relationship to Deployment-Time Learning

RL-based routing — especially bandit variants — is the primary routing-specific instantiation of [[deployment-time-learning]]. The bandit policy sits between the user query and the model pool, continuously improving without modifying the underlying LLM weights.

## See Also

- [[model-routing]] — parent concept
- [[deployment-time-learning]] — broader paradigm of online adaptation during deployment
- [[dynamic-routing]] — RL/bandit routing is naturally suited to dynamic model pools
- [[llm-cascade]] — cascading and RL can be combined (RL learns cascade thresholds)
- [[moslem-2026-routing-survey]] — primary source taxonomising RL-based routing paradigms
