---
type: entity
title: "A-LLMRec"
tags: [recommender-systems, collaborative-filtering, llm-alignment, cold-start, kdd-2024]
sources: [kim-2024-llm-rec]
created: 2026-06-06
updated: 2026-06-06
---

# A-LLMRec

**A-LLMRec** (All-round LLM-based Recommender system) is a recommender framework proposed by Kim et al. at KDD 2024 (KAIST & NAVER). It bridges a frozen pretrained collaborative filtering recommender system (CF-RecSys) and a frozen LLM using a lightweight trainable alignment network, achieving strong performance across cold-start, warm-start, few-shot, cold-user, and cross-domain recommendation scenarios.

Code: https://github.com/ghdtjr/A-LLMRec

## Core Idea

Prior LLM-based recommenders (e.g., TALLRec) excel in cold scenarios due to their rich textual knowledge, but fail to match simple CF models in warm scenarios because they lack collaborative knowledge from user-item interaction history. A-LLMRec addresses this by injecting CF embeddings directly into the LLM's input space, enabling the LLM to reason over both collaborative and textual signals simultaneously.

## Architecture

**Two training stages, both the CF-RecSys and LLM remain frozen:**

### Stage 1: CF–Text Alignment
- A frozen CF-RecSys (e.g., SASRec) produces item embeddings.
- A fine-tuned Sentence-BERT extracts text embeddings from item titles/descriptions.
- Two 1-layer MLP encoders align both into a shared latent space.
- Three losses: latent space matching (MSE), item reconstruction, text reconstruction (the latter two prevent embedding collapse).
- A recommendation loss (BPR-style) teaches the alignment about the recommendation objective.

### Stage 2: LLM Recommendation
- Aligned item embeddings are inserted as soft tokens alongside item text into the LLM prompt.
- A user representation from the CF-RecSys is also prepended as a soft token.
- The frozen LLM (OPT-6.7B in experiments) selects the next item from a candidate set.

## Key Properties

| Property | A-LLMRec | TALLRec (comparison) |
|---|---|---|
| CF-RecSys fine-tuning | None (frozen) | N/A |
| LLM fine-tuning | None (frozen) | LoRA (PEFT) |
| Trainable parameters | Alignment network only | LLM LoRA adapters |
| Training speed | ~2.53x faster | Baseline |
| Inference speed | ~1.71x faster | Baseline |
| Cold scenario | Strong | Strong |
| Warm scenario | Strong | Weak |
| Language generation | Preserved | Lost (garbled output) |
| Model-agnostic | Yes (any CF backbone) | N/A |

## Results

On Amazon Movies/TV and Video Games datasets, A-LLMRec outperforms:
- Traditional CF models (NCF, GRU4Rec, SASRec) in cold scenarios
- LLM-based models (TALLRec, LLM-Only) in warm scenarios
- All baselines in cross-domain and few-shot settings

The reconstruction losses preventing embedding collapse are empirically shown to be critical.

## See Also

- [[kim-2024-llm-rec]] — Source paper
- [[collaborative-filtering]] — The foundational technique A-LLMRec integrates with LLMs
- [[llm-cf-alignment]] — The core technical concept: aligning CF embeddings to LLM token space
- [[model-routing]] — Related paradigm of selecting/adapting LLM behavior via lightweight bridges
