---
type: concept
title: "Similarity-Based Routing"
tags: [llm-routing, pre-generation-routing, embeddings, unsupervised]
sources: [varangot-reille-2025-routing-survey, ong-2025-routellm, jitkrittum-2026-universal-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Similarity-Based Routing

**Similarity-based routing** is a family of [[model-routing]] strategies that select a target model based on semantic similarity between the incoming query and a reference set of past queries or interaction patterns. Unlike supervised routing (which requires labelled training data with explicit routing targets), similarity-based methods use **unsupervised or weakly supervised signals** — historical performance patterns, human preference data, or clustering of past interactions.

## Three Sub-Strategies

### 1. Query Similarity (kNN)
Routes a query to the model that performed best on the most similar past queries, measured by embedding cosine similarity.

- **1-Nearest-Neighbour**: simplest form; often fails on complex queries and can perform worse than random baselines.
- **k-Nearest-Neighbour** (k > 1): more robust; achieves ~90% accuracy on intent detection tasks, comparable to prompt-based classifiers (Manias et al. 2024).
- **Contrastive learning enhancements**: OrchestraLLM and RouterDC train embeddings to cluster semantically similar queries, reducing calls to large models by 50–80%.
- **LoRA adapter routing**: extends query similarity to select fine-tuned adapters rather than separate models.

See [[knn-routing]] for the dedicated concept page.

### 2. Clustering Previous Interactions
A two-stage approach: (1) identify the cluster that best represents the incoming query; (2) route to the model with the best historical performance on that cluster.

- **Pre-trained clusters** (Expert Router, Pichlmeier 2024): leverages large-scale pre-trained cluster assignments.
- **From-scratch k-means** (Srivatsa 2024, Jitkrittum 2025 / [[uniroute]]): trains clusters on routing-specific data; generalises without retraining when new models are introduced.

The key advantage of the clustering approach is **dynamic extensibility**: adding a new model only requires computing its per-cluster performance vector — no router retraining. This is what [[dynamic-routing]] and [[uniroute]] are built on.

### 3. Preference Similarity
Reframes routing as preference prediction: given query similarity to past interactions, what is the probability that a more expensive model would be preferred?

- **RouteLLM** ([[routellm]]): uses Chatbot Arena preference data + Bradley-Terry algorithm with similarity weighting. Predicts P(large model preferred | query); routes to large model only when probability exceeds a threshold.
- **Eagle** (Zhao et al. 2024): ELO-based; computes a weighted sum of global ELO ranking and local ELO from nearest-neighbour preferences.
- **Semantic entropy enhancement** (Zhang et al. 2025): replaces raw preference similarity with uncertainty-based preference simulation; needs only 27% of queries routed to the large model to achieve 50% quality boost on MT-Bench over the small model baseline.

Preference-based methods consistently outperform classification baselines (SVM, MLP, KNN, BERT classifiers) — suggesting that preference signals capture routing requirements better than hard labels.

## Strengths and Limitations

**Strengths**:
- Lightweight: no labelled data with explicit routing targets required.
- Adaptable: reference sets can be updated as new queries arrive.
- Extensible: clustering variants work without retraining when model pool changes.

**Limitations**:
- Fails on complex or rare queries where no similar historical example exists.
- Performance is sensitive to the embedding quality and domain coverage.
- Preference data (Chatbot Arena) may not generalise to production query distributions.
- Simple 1-NN implementations can perform worse than random on generative tasks.

## Where This Fits

- [[varangot-reille-2025-routing-survey]] — §4.1; primary taxonomy source.
- [[knn-routing]] — dedicated page for the query similarity sub-strategy.
- [[dynamic-routing]] — the clustering approach enables dynamic routing without retraining.
- [[uniroute]] — implements cluster-based routing for dynamic model pools.
- [[routellm]] — flagship preference similarity routing system.
- [[model-routing]] — parent concept.
- [[pre-generation-routing]] — similarity-based routing is always a pre-generation approach.
