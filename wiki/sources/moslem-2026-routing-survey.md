---
type: source
title: "Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey"
authors: ["Yasmin Moslem", "John D. Kelleher"]
url: "https://arxiv.org/abs/2603.04445"
raw: "raw/Moslem 2026 - Dynamic Model Routing and Cascading for Efficient LLM Inference A Survey.pdf"
ingested: 2026-06-06
tags: [llm-routing, survey, llm-cascade, rl-routing, uncertainty-routing, multimodal-routing, benchmark]
entities: [frugalgpt, routellm, embedllm, irtnet, uniroute]
concepts: [model-routing, llm-cascade, dynamic-routing, multimodal-llm-routing, rl-based-routing, uncertainty-based-routing, skill-based-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey

**Moslem & Kelleher, ADAPT Centre / Trinity College Dublin, arXiv 2603.04445v2 (April 2026)**

## Summary

This survey provides the first systematic, taxonomy-driven analysis of *multi-LLM* routing and cascading — the practice of intelligently dispatching queries at inference time across a pool of independently trained LLMs rather than within a single model (cf. Mixture-of-Experts). The authors at Trinity College Dublin's ADAPT Centre cover the full design space from simple heuristic difficulty estimation to learned RL policies, and from pre-generation to post-generation decisions.

## Core Claim

Well-designed multi-LLM routing systems can *outperform* even the most powerful individual models by strategically leveraging specialised capabilities across models, while simultaneously reducing costs. Choosing the optimal routing strategy depends critically on deployment and computational constraints; no single paradigm dominates across all settings.

## Taxonomy: Six Routing Paradigms

The survey organises the literature into six paradigms (plus a multimodal extension):

| Paradigm | Mechanism | Representative Methods |
|---|---|---|
| **Difficulty-aware** | Estimate query complexity; route simple queries to small models | BEST-Route, vLLM Router, RouteLMT, EmbedLLM, ICL-Router, GraphRouter, IRT-Router |
| **Human preference-aligned** | Learn from human pairwise preference data | RouteLLM, Hybrid LLM, Arch-Router, P2L, Eagle, Zooter |
| **Clustering-based** | Unsupervised grouping of queries to matched specialist models | UniRoute, Avengers-Pro |
| **Reinforcement learning** | Learn routing policies via PPO/GRPO/bandit methods | Router-R1, R2-Reasoner, SCOPE, MetaLLM, MixLLM, PILOT, GreenServ, Dueling Feedback, TI-UCB |
| **Uncertainty-based** | Route based on model confidence/conformal prediction | CP-Router, Probe-based UQ |
| **Cascading** | Sequential escalation through cheaper → stronger models | FrugalGPT, Cascade Routing, AutoMix, Self-REF, LM-Blender |

## Three-Dimensional Conceptual Framework

Beyond taxonomy, the paper introduces a unifying three-axis framework for characterising any routing system:

1. **When** — *pre-generation* (query features only), *post-generation* (response quality signals), or *multi-stage* (sequential escalation combining both).
2. **What** — signals used: query features alone, query + model metadata (cost, latency, domain), response-level signals (confidence, token probabilities, verifier outputs), or accumulated external feedback.
3. **How** — computation mechanism: heuristic/threshold rules, supervised classifiers, bandit algorithms, or full RL policy optimisation (PPO, GRPO).

Key insight: real-world systems are *compositional* — they combine multiple paradigms under operational constraints. For example, a system may use a supervised classifier for initial routing and a threshold rule for cascade escalation.

## Key Methodological Findings

- **Difficulty-aware routing** is almost always pre-generation and operates on query-level signals. LLM-as-a-judge (asking a model to estimate own complexity) is an emerging sub-technique.
- **Preference-aligned routing** (e.g., [[routellm]]) leverages human ranking signals from platforms like Chatbot Arena to train binary classifiers — strong results but requires large preference datasets.
- **RL-based routing** (PPO, GRPO, bandit methods) is uniquely suited to online/adaptive settings where the routing policy must improve from deployment-time feedback. Bandit methods (e.g., TI-UCB, MetaLLM) are particularly relevant when the model pool changes or ground truth is delayed.
- **Uncertainty-based routing** (conformal prediction, probe-based UQ) routes post-generation based on calibrated confidence; best for safety-critical applications.
- **Cascading** (e.g., [[frugalgpt]], AutoMix) typically employs layers of individual routing techniques: a small model attempts first, a scoring function evaluates quality, and escalation follows only on failure. Cascades can also embed safety checks on inputs and outputs.
- **Multimodal routing** is an emerging area; joint text+image embeddings beat unimodal baselines (see [[mmr-bench]]).

## Open Challenges Identified

- **Cross-architecture generalisation**: routers trained on one set of model pairs do not transfer cleanly to new ones.
- **Latency in cascades**: each escalation step adds latency; practical deployment must bound total cascade depth.
- **Evaluation gaps**: most benchmarks focus on accuracy/cost trade-off; calibration, fairness, and distributional shift are underexplored.
- **Multimodal gaps**: few routing approaches handle video, audio, or mixed modalities beyond text+image.
- **RL training stability**: policy-gradient methods are sensitive to reward design and can overfit to specific benchmarks.

## Where This Fits

This survey is the most comprehensive taxonomy of multi-LLM routing as of 2026. It contextualises and cross-references many papers already in this wiki:

- [[model-routing]] — the central concept this survey taxonomises
- [[llm-cascade]] — covered in depth as a multi-stage routing paradigm; [[frugalgpt]] is the primary case study
- [[dynamic-routing]] — the survey covers this under clustering and RL paradigms
- [[routellm]] — canonical example of preference-aligned routing
- [[embedllm]] — cited under difficulty-aware routing for compact model embedding-based routing
- [[irtnet]] — IRT-Router listed as a difficulty-aware method
- [[uniroute]] — listed under clustering-based routing
- [[multimodal-llm-routing]] — Section 8 of the survey; [[mmr-bench]] is the evaluation vehicle
- [[skill-based-routing]] — subsumed conceptually under preference-aligned and clustering paradigms
- [[deployment-time-learning]] — RL-based routing (bandit methods) is the routing-specific instantiation
- [[rl-based-routing]] — new concept page created from this survey's RL paradigm section
- [[uncertainty-based-routing]] — new concept page created from the survey's uncertainty paradigm section
