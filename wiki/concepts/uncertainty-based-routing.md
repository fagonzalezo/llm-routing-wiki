---
type: concept
title: "Uncertainty-Based Routing"
tags: [llm-routing, uncertainty-quantification, conformal-prediction, calibration]
sources: [moslem-2026-routing-survey]
created: 2026-06-06
updated: 2026-06-06
---

# Uncertainty-Based Routing

**Uncertainty-Based Routing** is a class of [[model-routing]] methods that make routing decisions based on a model's calibrated confidence in its own output. Rather than selecting a model before generation (pre-generation), these approaches typically operate *post-generation*: a cheap model generates a candidate response, a confidence estimator evaluates it, and the query escalates to a stronger model only if confidence falls below a threshold.

## Core Idea

Different from difficulty-aware routing (which predicts complexity from query features *before* generating), uncertainty-based routing uses *response-level signals* — the model's internal probability distribution, calibrated confidence scores, or probe-based estimates — to decide whether the initial response is trustworthy. This makes it well-suited to safety-critical applications where false confidence is costly.

## Key Techniques

### Conformal Prediction (CP-Router)
Applies conformal prediction theory to obtain statistically valid coverage guarantees. For a given confidence level $1 - \alpha$, the conformal predictor constructs a prediction set such that the true answer is included with probability at least $1 - \alpha$. If the prediction set is large (high uncertainty), the query escalates. **CP-Router** is the representative system from [[moslem-2026-routing-survey]].

### Probe-Based Uncertainty Quantification
Lightweight auxiliary probes (small classification heads) are attached to intermediate transformer layers to estimate model confidence without requiring full generation. This avoids the latency of sampling multiple completions. The probes are trained to predict correctness from hidden states at inference time.

## Relationship to the Three-Dimensional Framework

Within the conceptual framework of [[moslem-2026-routing-survey]]:

| Dimension | Uncertainty-Based Placement |
|---|---|
| **When** | Post-generation (and often multi-stage in cascades) |
| **What** | Response-level signals (token probabilities, hidden states, prediction sets) |
| **How** | Heuristic thresholds on confidence, or trained probes |

Uncertainty methods naturally pair with cascading: they are the *scoring function* component of an [[llm-cascade]] that decides when to escalate.

## Trade-Offs

- **Calibration dependency**: Routing quality is only as good as the confidence estimates. LLMs are known to be poorly calibrated out-of-the-box; temperature scaling or post-hoc calibration is usually required.
- **Latency**: Post-generation routing means one model has already run; escalation adds a second forward pass. Probe-based methods mitigate this by intercepting at intermediate layers.
- **Coverage guarantees**: Conformal prediction provides formal coverage guarantees (unlike heuristic thresholds), but requires a calibration dataset and assumes exchangeability.

## See Also

- [[model-routing]] — parent concept
- [[llm-cascade]] — uncertainty estimates are commonly used as the scoring/escalation signal within cascades
- [[moslem-2026-routing-survey]] — primary source taxonomising uncertainty-based routing
