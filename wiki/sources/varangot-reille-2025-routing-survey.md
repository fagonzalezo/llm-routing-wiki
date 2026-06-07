---
type: source
title: "Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems"
authors: ["Clovis Varangot-Reille", "Christophe Bouvard", "Antoine Gourru", "Mathieu Ciancone", "Marion Schaeffer", "François Jacquenet"]
url: "https://arxiv.org/abs/2502.00409"
raw: "raw/Varangot-Reille 2025 - Doing More with Less A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems.pdf"
ingested: 2026-06-06
tags: [llm-routing, survey, cost-optimization, pre-generation-routing, post-generation-routing, similarity-routing, rl-routing, generative-routing]
entities: [routellm, frugalgpt, embedllm, uniroute, llmrouterbench, routereval]
concepts: [model-routing, llm-cascade, pre-generation-routing, post-generation-routing, similarity-based-routing, query-complexity-routing, rl-based-routing, generative-routing, knn-routing, dynamic-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems

## Summary

Varangot-Reille et al. (2025) provide the most comprehensive survey of LLM routing strategies to date (37 pages, arXiv:2502.00409v3). The paper formalises routing as a **performance–cost optimisation problem**: given a set of candidate models *M = {M₁, ..., Mₙ}*, a router *R* selects the model maximising a scoring function *s(q, M)* subject to a budget constraint *C_M(q) ≤ B*. Critically, this definition distinguishes routing from Mixture-of-Experts (MoE): routers operate externally and independently from the LLM's forward pass, operate under budget constraints, and can route to non-neural candidates (workflows, data sources).

The survey is structured around three core questions: **Q1: What to optimise?**, **Q2: When to route?**, and **Q3: How to implement routing?** It reviews ~100 routing studies and introduces a taxonomy distinguishing pre-generation routing from post-generation (cascade) routing, then further classifying routing strategies into four implementation families.

## Key Contributions

1. **Formal taxonomy**: First survey to clearly separate the pre-/post-generation routing axis from the implementation strategy axis (similarity, supervised, RL, generative).
2. **Formal definition of routing**: Distinguishes routing from MoE and from ensemble methods (which aggregate outputs from multiple models — explicitly excluded because they sacrifice cost efficiency for performance).
3. **Coverage of non-financial costs**: Argues that the field over-focuses on API token costs; latency, compute, and especially **environmental costs** (kWh, kgCO2eq) must be minimised too.
4. **Identifies key open challenges**: Poor generalisation to new LLM candidates, lack of standardised evaluation benchmarks, limited task diversity in experiments, and the absence of adaptive/autonomous routing strategies.

## Q1: What Should Routing Optimise?

### Performance metrics
- Ground-truth comparison: exact match, partial match, ROUGE, semantic similarity.
- Human evaluation (expensive, subjective, not scalable).
- LLM-as-judge: embedding rating criteria + response into a prompt; uncertain human alignment.
- Frameworks like RAGAS automate RAG-specific evaluation.
- **Preference learning**: pairwise human preference data (A ≺ₓ B); used in RouteLLM, Eagle.

### Cost metrics
- Primary: **price per token** (API cost for proprietary models); must account for all models called in a pipeline (LLMs + embedding models in RAG).
- **Latency**: time from user request to first token / full response.
- **Computational cost**: GPU/CPU resources for inference.
- **Environmental cost**: kWh energy consumption, kgCO2eq global warming potential — tools: Ecologits, CodeCarbon, MLCO2, Boavizta.

## Q2: When Should Routing Take Place?

### Pre-generation routing
Routing decisions made **before** any model generates a response. Two sub-strategies:
- **Domain routing**: classify the query's knowledge domain; route to a domain-specialist model.
- **Complexity routing**: estimate how difficult the query is for a given LLM; route to the cheapest model with sufficient ability.

Query complexity taxonomy (for RAG agents):
- *Low*: simple greetings, no retrieval needed.
- *Intermediate*: explicit info extraction from a single document.
- *High*: implicit reasoning across multiple documents.

Advantage: minimises latency (no model must generate before routing).

### Post-generation routing (cascade routing)
Each candidate model generates a response; a **stop judger** (confidence score vs. threshold τ) decides whether to accept or escalate to a more capable model. Higher latency and cost (multiple generations per query), but evaluates actual output.

Variant: **multi-choice cascading** (deKoninck et al. 2024) — a hybrid where the next model is chosen dynamically rather than following a fixed sequence.

## Q3: How Should Routing Be Implemented?

### 4.1 Similarity-Based Routing

Routes queries using semantic similarity to a reference set of past queries.

- **Query similarity (kNN)**: cosine similarity between query embeddings; 1-NN often worse than random; multi-NN (e.g., kNN, k=5) achieves ~90% accuracy comparable to intent detection.
  - **Contrastive learning** (OrchestraLLM, RouterDC): trains embeddings so similar queries cluster together; reduces calls to large models by 50–80% with comparable accuracy.
  - **LoRA adapter routing**: extends similarity routing to select the optimal LoRA adapter rather than a separate model.
- **Clustering previous interactions**: k-means clusters from historical queries; assign the best LLM per cluster; generalises without retraining when new LLMs are added (UniRoute approach).
- **Preference similarity**: uses human preference data (Chatbot Arena) to estimate P(large model preferred | query); RouteLLM Bradley-Terry + similarity weighting; Eagle ELO-based global + local ranking.

### 4.2 Supervised Routing

Trains an explicit routing classifier/predictor on labelled data.

- **Recommendation systems**: matrix factorisation (latent embeddings for queries × models); RouteLLM MF achieves 80% quality with only 30% GPT-4 calls; EmbedLLM scales to 100+ models.
- **Domain classification**: BERT-based (DeBERTa-v3-large) domain classifiers; MoDEM achieves MMLU 87.7% using pools of 70B domain expert models at 4× lower cost than a single 405B model.
- **Query complexity inference**: predicts query difficulty; routes simple queries to cheap models, complex to powerful ones; majority of routing literature focuses here.
- **Knowledge graphs**: routes based on structured knowledge relationships in the query.
- **Answer confidence inference**: FrugalGPT-style cascade uses predicted confidence scores as the stop criterion.

### 4.3 Reinforcement Learning-Based Routing

Frames routing as an RL decision problem.

- **Stateless algorithms**: bandit-style; no memory of past queries.
- **State-based algorithms**: maintain state across interactions (e.g., LLMBandit).
- **Reward-based inference**: use reward signals derived from LLM outputs (log-probs, self-evaluation) to make routing decisions.

### 4.4 Generative-Based Routing

Uses the generative capabilities of LLMs themselves to make routing decisions.

- **Token probability**: route based on the probability of the first generated token; used for binary routing (small vs. large model).
- **Sequence probability**: score entire generated sequences.
- **Prompt-based routing**: instruct an LLM to choose the appropriate model via prompt; low overhead but sensitive to prompt formulation.
- **LLM fine-tuning**: fine-tune a small LLM to output routing decisions.
- **Repeated calls**: generate multiple responses; select via consistency or scoring.
- **Code execution**: verify answer correctness by executing generated code (for tool-use tasks like ToolBench).

## Discussion and Challenges

### Industrial considerations
Most production routing systems rely on simple rule-based or classifier-based approaches rather than RL or generative methods, prioritising reliability and interpretability.

### Key open challenges
1. **Going beyond financial costs**: latency and environmental costs are under-optimised; most benchmarks only measure API cost.
2. **Standardisation**: experiments vary in model pools, benchmarks, and cost metrics — reproducibility is poor. [[routereval]] and [[llmrouterbench]] make progress here.
3. **Complementary routing options**: routing to caches, RAG pipelines, agentic tools, or rejection (no-response) as candidates, not just different LLMs.
4. **All pipeline steps as routing candidates**: retrieval, chunking strategy, prompt template, response length — all could be routed; few works treat this holistically.
5. **Adaptive/autonomous routing**: current strategies have static model pools; next frontier is routing that adapts as new models become available and learns from deployment feedback (related to [[deployment-time-learning]]).

## Where This Fits

This survey is the field-level reference for [[model-routing]]. It provides the formal framework that underpins all entity and concept pages in this wiki. Specifically:

- [[llm-cascade]] / [[frugalgpt]] — covered under post-generation/cascade routing (§3.2, §4.2.5).
- [[routellm]] — covered under preference similarity (§4.1.3) and supervised recommendation systems (§4.2.1).
- [[embedllm]] / [[irtnet]] — covered under supervised recommendation systems (§4.2.1).
- [[uniroute]] — covered under clustering-based routing (§4.1.2); the approach that generalises without retraining when LLM candidates change.
- [[knn-routing]] — foundational strategy under §4.1.1.
- [[dynamic-routing]] — the survey's clustering approach (§4.1.2) directly enables dynamic routing.
- [[llmrouterbench]] / [[routereval]] — cited as efforts toward standardisation (§5.2.2).
- [[collaborative-inference]] — partly covered under the "complementary routing options" challenge (§5.2.3); device-cloud split is one instance of broader routing to heterogeneous resource pools.
- [[deployment-time-learning]] — directly relevant to the "autonomous adaptive routing" challenge (§5.2.5).

New concepts introduced or formalised in this survey:
- [[pre-generation-routing]] — the timing axis: routing before any generation.
- [[post-generation-routing]] — the timing axis: cascade routing after generation.
- [[similarity-based-routing]] — the implementation family using query similarity/preference similarity.
- [[query-complexity-routing]] — estimating query difficulty for routing decisions.
- [[rl-based-routing]] — bandit and MDP-style routing frameworks.
- [[generative-routing]] — using LLM-native signals (token probs, prompting) for routing.
