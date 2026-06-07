---
type: concept
title: "Perplexity-Based Routing"
tags: [llm-routing, model-selection, pseudo-perplexity, zero-shot, low-resource-nlp]
sources: [owodunni-2023-koya]
created: 2026-06-06
updated: 2026-06-06
---

# Perplexity-Based Routing

**Perplexity-Based Routing** is a family of LLM selection/routing methods that use a model's **intrinsic language familiarity** — measured by perplexity or pseudo-perplexity on a sample from the target domain — as the routing signal. Unlike learned routers that require labeled preference data or finetuning logs, perplexity-based methods are **zero-shot and training-free**, relying only on the pretrained model's internal probability distributions.

## Core Intuition

A language model with lower perplexity on a text sample has higher probability of that text under its learned distribution — it is "more familiar" with the language and domain. Because downstream task performance depends on how well a model has internalized the surface statistics and semantics of a language, perplexity serves as a cheap proxy for expected finetuned performance:

> *The more sense an LLM is able to make of a sentence in a given language, the easier and faster it will be for the model to learn the downstream task in that language.* — Owodunni & Emezue (2022)

## Variants

### Standard Perplexity (Autoregressive Models)
For causal/autoregressive LLMs, perplexity is well-defined as the inverse geometric mean of the token probabilities under the model:

PPL(S) = exp(−(1/N) Σ log P(wᵢ | w₁,...,wᵢ₋₁))

### Pseudo-Perplexity (PPPL) for MLMs
For bidirectional masked language models (BERT variants), the joint sequence probability cannot be factorized autoregressively. Salazar et al. (2019) introduced **pseudo-perplexity**, masking each token in turn and summing the log-likelihoods from each masked prediction:

PPPL(S) = exp(−(1/N) Σ log P(wᵢ | w₁,...,wᵢ₋₁, wᵢ₊₁,...,wN))

This requires *N* forward passes (one per token), making it O(N) in sequence length.

### Koya Pseudo-Perplexity (KPPPL)
Introduced by [[owodunni-2023-koya]], KPPPL approximates PPPL by masking only a **random subset of *k* tokens** rather than all *N*:

KPPPL(S) ≈ exp(−(1/k) Σᵢ∈R log P(wᵢ | S \ wᵢ))

This reduces inference cost from O(N) to O(k) forward passes while maintaining high rank correlation with actual finetuned performance (~95% recommender accuracy across three African languages).

## Use Cases

1. **Pre-inference Model Selection (Static Routing)**: Before deploying on a new language/domain, score all candidate models on a few representative samples and select the top-ranked one. This is the primary use case of [[koya]].
2. **Domain Shift Detection**: Monitor perplexity drift over time; a sudden spike may indicate the query distribution has shifted beyond the model's training distribution.
3. **Model Pool Pruning**: In ensemble or cascade systems, prune low-compatibility models before deploying, reducing the candidate pool cheaply.

## Advantages

- **Zero labels required** — no annotated finetuning data needed.
- **No model training** — the signal comes from the pretrained weights directly.
- **Language-agnostic** — works for any language, including those not well-covered by external knowledge bases (URIRL, LITMUS).
- **Single-sentence sufficient** — in practice, scoring a single representative sentence produces reliable rankings.

## Limitations

- Measures **language familiarity**, not task-specific aptitude. Two models may have similar KPPPL but very different instruction-following or reasoning ability.
- Requires access to the **model's logits** — not applicable to black-box API-only models without token probability outputs.
- Not designed for **per-query routing**: KPPPL is computed offline and provides a static ranking across the whole target language/domain, not a dynamic per-input decision.
- Less applicable for instruction-tuned or RLHF-aligned models where perplexity correlates poorly with helpfulness.

## Relationship to Other Routing Signals

| Signal | Training-free? | Per-query? | Requires logits? | Primary reference |
|--------|---------------|-----------|-----------------|-------------------|
| KPPPL | ✓ | ✗ (static) | ✓ (MLM) | [[owodunni-2023-koya]] |
| IRT ability (IrtNet) | ✗ | ✓ | ✗ | [[irtnet]] |
| Embedding similarity (EmbedLLM) | ✗ | ✓ | ✗ | [[embedllm]] |
| Preference classifier (RouteLLM) | ✗ | ✓ | ✗ | [[routellm]] |
| kNN from labeled set | ✗ | ✓ | ✗ | [[li-2025-predictive-routing]] |

## See Also

- [[koya]] — The recommender system that implements KPPPL-based model selection.
- [[owodunni-2023-koya]] — Primary source paper defining KPPPL.
- [[model-routing]] — The general paradigm of dynamically selecting LLMs for queries.
- [[irtnet]] — Complementary approach using learned latent ability representations.
