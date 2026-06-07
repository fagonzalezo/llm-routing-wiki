---
type: source
title: "Koya: A Recommender System for Large Language Model Selection"
authors: ["Abraham Toluwase Owodunni", "Chris Chinenye Emezue"]
url: "https://huggingface.co/spaces/koya-recommender/system"
raw: "raw/Owodunni 2023 - Koya A Recommender System for Large Language Model Selection.pdf"
ingested: 2026-06-06
tags: [llm-routing, model-selection, low-resource-nlp, pseudo-perplexity, african-languages, recommender-system]
entities: [koya]
concepts: [model-routing, perplexity-based-routing]
created: 2026-06-06
updated: 2026-06-06
---

# Koya: A Recommender System for Large Language Model Selection

**Owodunni & Emezue (AfricaNLP workshop at ICLR 2022)**

## Summary

This paper presents **Koya**, a recommender system designed to help researchers and practitioners — particularly those in low-compute, low-resource communities — select the most compatible pretrained LLM for a given downstream NLP task and language, **without ever finetuning the models**. The core insight is that perplexity (a model's intrinsic familiarity with a language) is a reliable proxy for downstream task performance: the more sense an LLM can make of a sentence in a language, the faster and easier it will be to adapt to a downstream task in that language.

## Key Contributions

1. **Koya Pseudo-Perplexity (KPPPL)**: A novel adaptation of the standard pseudo-perplexity for masked language models (MLMs). Rather than masking all tokens to compute the full pseudo-perplexity, KPPPL randomly selects a subset of *k* tokens to mask, which accelerates inference while preserving ranking accuracy. This makes Koya faster than full PPPL scoring.

2. **Zero-Finetune Recommender**: Koya ranks a pool of pretrained LLMs by their KPPPL score on a single user-provided sentence from the target dataset. Lower KPPPL indicates better language familiarity and a higher recommendation rank. No finetuning, no training data labels required.

3. **High Recommender Accuracy on African Languages**: Evaluated across five encoder-only MLMs — AfriBERTa, Afro-XLMR, mBERT, InfoXLM, and XLM-RoBERTa — and three African languages (Yoruba, Kinyarwanda, Amharic), Koya achieves an **average recommender accuracy of 95%** on two downstream tasks (news classification and NER).

4. **Web Interface**: Koya is deployed as an accessible web interface (hosted on HuggingFace Spaces), making it practical for researchers without sophisticated infrastructure.

## Methodology

- **KPPPL computation**: Given a sentence *S* of *N* tokens, randomly select *k* tokens to mask. For each masked token *w_ri*, pass the masked sequence through the MLM and read off the probability the model assigns to the original token from the masked-position logits. KPPPL is the geometric mean of these per-token inverse probabilities, i.e., the *k*-th root of the product of inverse token probabilities.
- **Ranking**: All candidate LLMs are scored with KPPPL on the same sample sentence from the user's dataset. Models are ranked ascending by KPPPL (lower = better fit).
- **Comparison baseline**: The KPPPL ranking is compared against rankings derived from actual finetuning performance (ground truth) to compute recommender accuracy.

## Experimental Setup

- **Languages**: Amharic (Afro-Asiatic, ~50k news articles), Kinyarwanda (Niger-Congo, 21k articles + MasakhaNER), Yoruba (Niger-Congo, 1.9k BBC news articles + MasakhaNER)
- **Downstream tasks**: News classification and Named Entity Recognition (NER)
- **Models evaluated**: AfriBERTa, Afro-XLMR, mBERT, InfoXLM, XLM-RoBERTa
- **Result**: 95% average recommender accuracy; Koya's ranking closely tracks finetuned performance without any training.

## Key Claims

- A single representative sentence is sufficient for Koya to produce a reliable ranking — full corpus perplexity is not required.
- KPPPL is faster than full PPPL because only a random subset of tokens is masked per forward pass.
- The approach is fully agnostic to downstream task type and does not require access to training infrastructure or language-specific metadata.
- The method is especially valuable for low-resource, low-compute communities where finetuning 500+ HuggingFace models is not feasible.
- Unlike Xia et al. (2020) which requires language distance features from URIRL, or Ahuja et al. (2022) which depends on Microsoft's LITMUS project, Koya is self-contained and works for understudied languages without external databases.

## Relationship to Routing

While framed as a "recommender system," Koya is functionally an early instance of **static LLM routing** (model selection before inference). The selection signal (KPPPL) is intrinsic, zero-shot, and training-free — distinguishing it from learned routers (e.g., [[routellm]], [[irtnet]]) that require labeled preference data or finetuning logs. Koya's focus on **low-resource language compatibility** also fills a gap in the routing literature, which predominantly targets English-centric benchmarks.

## Where This Fits

- [[koya]] — the entity page for the system described in this paper.
- [[model-routing]] — Koya is a zero-shot, perplexity-driven instance of pre-inference model selection.
- [[perplexity-based-routing]] — The KPPPL metric is the conceptual anchor; this paper is the primary source for that concept.
- [[irtnet]] — Both use intrinsic model properties (IRT ability vs. KPPPL) to predict downstream task performance without finetuning.
- [[embedllm]] — Complementary: EmbedLLM learns compact embeddings from finetuning data; Koya requires no labeled data at all.
- [[routereval]] — Routing evaluation frameworks; Koya's recommender accuracy metric is a simpler but related evaluation paradigm.
