---
type: concept
title: "Post-Generation Routing"
tags: [llm-routing, cost-optimization, llm-cascade]
sources: [varangot-reille-2025-routing-survey, chen-2023-frugalgpt]
created: 2026-06-06
updated: 2026-06-06
---

# Post-Generation Routing

**Post-generation routing** (also called **cascade routing**) is a routing paradigm where a model generates a response *first*, and then a stop judger evaluates that response to decide whether to accept it or escalate to a more capable (and more expensive) model. The process can iterate over a sequence of models of increasing capability.

This is the timing axis complement to [[pre-generation-routing]]. While pre-generation routing is *predictive*, post-generation routing is *evaluative* — it directly assesses actual model output rather than predicting performance from query features alone.

## Core Mechanism

```
Query → Model₁ → Response₁ → Stop Judger
                                 ↓ (score < τ)
                              Model₂ → Response₂ → Stop Judger
                                                       ↓ (score ≥ τ)
                                                     Return Response₂
```

The **stop judger** compares an output quality score against a threshold τ:
- If `score ≥ τ`: accept response; cascade terminates.
- If `score < τ`: escalate to the next model in the sequence.

## Relationship to LLM Cascade

Post-generation routing is the timing paradigm; [[llm-cascade]] is the specific architectural pattern that implements it. All LLM cascades are post-generation routers, but the broader concept of post-generation routing also encompasses non-sequential variants:

### Standard Cascade (Fixed Sequence)
Models are ordered by cost/capability (cheapest first). The stop judger applies a fixed threshold at each step. Championed by [[frugalgpt]].

### Multi-Choice Cascading
Proposed by deKoninck et al. (2024). A hybrid variant where the *next* model is selected dynamically (not from a fixed sequence) based on an evaluation of the current response. Incorporates elements of pre-generation routing into each escalation step. Generally outperforms simple cascading but at higher cost due to multiple generations.

## Scoring / Stop Criteria

Common stop judger implementations:
- **Confidence/calibration scores**: log-probability of the generated tokens (when API exposes logprobs).
- **Auxiliary classifier**: a small model trained to predict whether a given response is correct.
- **LLM self-evaluation**: prompt the model to score its own answer.
- **Code execution**: execute generated code; pass/fail as binary stop criterion.

## Cost-Latency Trade-off

Post-generation routing incurs **higher latency and cost** than pre-generation routing because at least one model must generate a response before routing proceeds. In the worst case (query escalates to the final model), *all* models in the cascade have generated outputs. This makes stop judger calibration critical: a poorly calibrated threshold causes either over-acceptance (low quality) or over-escalation (high cost).

## Key Limitation

Requires multiple generations per query in escalation scenarios, which can negate cost savings. Also requires that at least one model generates output before a routing decision is finalized — makes it unsuitable for latency-critical applications.

## Where This Fits

- [[varangot-reille-2025-routing-survey]] — §3.2 defines the concept and the multi-choice cascade variant.
- [[llm-cascade]] — the primary architectural instantiation of post-generation routing.
- [[frugalgpt]] — the landmark system implementing learned cascade thresholds.
- [[pre-generation-routing]] — the complementary timing paradigm; lower latency, predictive not evaluative.
- [[model-routing]] — parent concept.
