---
type: concept
title: "Pre-Generation Routing"
tags: [llm-routing, cost-optimization, query-routing]
sources: [varangot-reille-2025-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Pre-Generation Routing

**Pre-generation routing** is a routing paradigm where a routing decision is made *before* any candidate model generates a response. The router inspects the query (and optionally the system context) and selects the most appropriate model or pipeline component, then that model is invoked exactly once. Because no generation needs to happen first, pre-generation routing **minimises latency overhead** from routing itself.

## Contrast with Post-Generation / Cascade Routing

| Aspect | Pre-Generation | Post-Generation (Cascade) |
|---|---|---|
| When decided | Before any generation | After one or more models generate |
| Input to router | Query features only | Query + generated response(s) |
| Latency overhead | Low — one model invoked | High — multiple models may generate |
| Cost overhead | Low | Variable (potentially high) |
| Accuracy | Predictive; can be wrong | Evaluative; directly observes output quality |

## Two Main Sub-Strategies

### Domain Routing
Classify the query's knowledge domain and route to a domain-specialist model. Examples: routing medical questions to Med-PaLM, math questions to Mathstral-7B. Implemented via BERT-based classifiers (e.g., DeBERTa-v3-large).

- MoDEM (Simonds 2024) achieves MMLU 87.7% using a pool of 70B expert models at 4× lower cost than a single 405B generalist.

### Complexity Routing
Estimate the *difficulty* of a query for a given LLM, then route to the cheapest model that can handle it. [[query-complexity-routing]] is the dedicated concept page.

**Complexity taxonomy** (defined by Varangot-Reille et al.):
- *Low*: simple greetings or chitchat; no retrieval needed.
- *Intermediate*: explicit information extraction from a single document.
- *High*: implicit reasoning across multiple documents.

## Implementation Strategies

Pre-generation routing is implemented across multiple method families:

- **Similarity-based**: [[knn-routing]], clustering, preference similarity — route based on past query-performance patterns.
- **Supervised**: domain classifiers, complexity estimators, recommendation systems.
- **Reinforcement learning**: bandit algorithms that learn routing policies from deployment feedback.
- **Generative**: prompt the LLM to self-assess and choose a routing target.

## Key Limitation

The router operates on query features alone, meaning it must *predict* model performance without seeing the output. If the routing signal is weak (e.g., embeddings are ambiguous), it may route incorrectly — a risk that [[post-generation-routing]] avoids by evaluating actual outputs.

## Where This Fits

- [[varangot-reille-2025-routing-survey]] — primary definition source; §3.1 defines the concept.
- [[model-routing]] — parent concept; pre-generation routing is the dominant paradigm in the literature.
- [[post-generation-routing]] — the complementary timing paradigm.
- [[query-complexity-routing]] — the most common implementation signal for pre-generation routing.
- [[knn-routing]] — frequently used as a pre-generation routing mechanism.
- [[dynamic-routing]] — a variant where the model pool changes at test time, requiring pre-generation routing without retraining.
