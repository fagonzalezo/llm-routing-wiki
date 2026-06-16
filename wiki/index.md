# Wiki Index

The catalog of all pages in this wiki. Each entry: a wikilink to the page and a one-line summary. The LLM reads this first when answering queries to identify candidate pages.

Keep summaries tight — one line each. The index is engineered to be cheap to read; a fat index defeats its purpose.

When this file exceeds ~300 lines or the wiki passes ~150 pages, shard into `wiki/indexes/<type>.md` and replace this file with a directory of shards. See the `scaling-playbook.md` reference in the `llm-wiki` skill for the migration procedure.

---

## Sources

- [[hu-2024-routerbench]] — RouterBench: foundational multi-LLM routing benchmark (11 models × 8 tasks, 405K records) introducing the c–q plane, NDCH, Zero Router baseline, and AIQ metric (Hu et al. 2024).
- [[chen-2023-frugalgpt]] — FrugalGPT: budget-aware LLM cascade pipeline optimization that cuts costs while maintaining quality by combining heterogeneous APIs.
- [[advanced-architectures-llm-routing]] — Comprehensive routing survey: unifies kNN, cascade, bandit, RecSys-isomorphism, and oracle-gap perspectives on LLM routing (Moslem & Kelleher 2026).
- [[shnitzer-2024-benchmark-routing]] — Repurposes benchmark evaluation byproducts (per-sample correctness records) to train kNN-based LLM routers; introduces three routing scores including an OOD-aware variant.
- [[chen-2025-irtnet]] — IrtNet: applies Item Response Theory to learn compact LLM + query embeddings for routing and benchmark prediction.
- [[fang-2025-device-cloud]] — RL post-training framework (GAPG) enabling a lightweight on-device LLM to dynamically collaborate with a cloud LLM for cost-efficient inference.
- [[guo-2026-cascade]] — CASCADE: case-based continual adaptation framework that lets LLM agents improve from deployment-time failures without retraining.
- [[huang-2025-routereval]] — RouterEval: comprehensive open-source benchmark evaluating LLM routing across 11 router methods, 3 difficulty levels, and 4 query types.
- [[jitkrittum-2026-universal-routing]] — UniRoute: universal LLM routing for dynamic model pools where the candidate set changes at test time.
- [[kim-2024-llm-rec]] — A-LLMRec: efficient all-round LLM-based recommender bridging frozen CF-RecSys and frozen LLM via a lightweight alignment network (cold + warm + cross-domain).
- [[li-2025-predictive-routing]] — Challenges the trend toward complex learned routers; shows simple kNN matching often outperforms sophisticated parametric approaches.
- [[li-2026-llmrouterbench]] — LLMRouterBench: large-scale benchmark and unified framework for evaluating LLM routing systems across diverse strategies.
- [[ma-2026-mmr-bench]] — MMR-Bench: budget-aware benchmark for multimodal LLM routing, showing joint text+image embeddings beat unimodal routers.
- [[moslem-2026-routing-survey]] — First systematic survey organizing dynamic model routing and cascading into six paradigms with a 3D conceptual framework (Moslem & Kelleher 2026).
- [[poon-2026-contextual-bandits]] — First contextual bandit framework for sequential multi-step LLM selection under unstructured context evolution; introduces myopic regret and Greedy LinUCB.
- [[nelson-2025-ethical-rec]] — Applies collaborative filtering to recommend ethical prompts in LLMs, steering users away from unethical inputs pre-generation.
- [[xu-2024-llm-recommender]] — Comprehensive LLM-RS framework and empirical analysis of prompting LLMs as recommenders: model selection, user interest modeling, candidate construction, and prompting strategies.
- [[okokamoto-2026-trust-routing]] — BELLA: transparent, skill-profile-based LLM routing that provides natural-language rationales for routing decisions under budget constraints.
- [[ong-2025-routellm]] — RouteLLM: open-source framework for learning binary LLM routers from human preference data, achieving >2× cost savings.
- [[owodunni-2023-koya]] — Koya: zero-finetune LLM recommender using KPPPL pseudo-perplexity for training-free model selection in low-resource African languages.
- [[varangot-reille-2025-routing-survey]] — Comprehensive survey formalizing model routing as a performance-cost optimization problem across four implementation families (Varangot-Reille et al. 2025).
- [[zhuang-2025-embedllm]] — EmbedLLM: reconstruction-based framework mapping LLMs to compact embeddings for correctness forecasting and routing.

## Entities

- [[a-llmrec]] — All-round LLM-based Recommender that aligns frozen CF-RecSys embeddings into a frozen LLM's token space for cold+warm recommendation (Kim 2024).
- [[bella]] — Budget-Efficient LLM Selection via Automated skill-profiling; transparent, interpretable routing framework (Okamoto 2026).
- [[cascade]] — CASe-based Continual Adaptation during DEployment; enables LLM agents to learn from deployment failures without retraining (Guo 2026).
- [[embedllm]] — Reconstruction-based framework that maps LLMs to compact latent embeddings for multi-task routing and prediction (Zhuang 2025).
- [[frugalgpt]] — Budget-aware LLM cascade pipeline optimizer that selects and combines heterogeneous APIs (Chen 2023).
- [[gapg]] — Group-Adaptive Policy Gradient; RL algorithm for jointly training on-device LLM collaboration behavior (Fang 2025).
- [[irtnet]] — Psychometrics-inspired framework applying Item Response Theory to learn compact LLM ability representations (Chen 2025).
- [[koya]] — Zero-finetune LLM recommender system using KPPPL for training-free model selection in low-resource languages (Owodunni 2023).
- [[llmrouterbench]] — Large-scale benchmarking suite and unified framework for LLM routing evaluation (Li 2026).
- [[mmr-bench]] — Comprehensive budget-aware benchmark for multimodal LLM routing (Ma 2026).
- [[routerbench]] — Foundational multi-LLM routing benchmark: 405K+ inference records across 11 LLMs × 8 tasks; introduced the AIQ metric and Zero Router baseline (Hu et al. 2024).
- [[routellm]] — Open-source framework for building and serving preference-trained binary LLM routers (Ong 2025).
- [[routereval]] — Comprehensive benchmark for evaluating LLM routing across difficulty levels and query types (Huang 2025).
- [[uniroute]] — Universal routing framework for dynamic model pools where candidate sets shift at test time (Jitkrittum 2026).

## Concepts

- [[benchmark-based-routing]] — Routing paradigm that recycles benchmark evaluation byproducts (per-sample correctness labels) to train input-only LLM routers without additional inference costs.
- [[contextual-bandits-routing]] — Online learning approach to LLM routing using contextual bandits (LinUCB); enables adaptive multi-step selection without offline training or model internals.
- [[collaborative-filtering]] — Recommendation technique predicting preferences from collective user behavior; applied to prompt and model selection.
- [[collaborative-inference]] — Device-cloud paradigm distributing LLM computation across edge and server to balance cost and latency.
- [[deployment-time-learning]] — Third lifecycle stage where LLMs improve from real interaction feedback during deployment without offline retraining.
- [[dynamic-routing]] — Routing paradigm where the candidate model pool changes at test time, requiring generalization beyond fixed model pairs.
- [[generative-routing]] — Routing paradigm using LLM-native generative signals (token probabilities, prompting) to determine model selection.
- [[llm-cf-alignment]] — Technique aligning CF-RecSys latent embeddings into an LLM's token space via lightweight adapter networks, enabling collaborative+textual reasoning.
- [[knn-routing]] — Non-parametric routing strategy retrieving the optimal model by nearest-neighbor similarity to a labeled reference set.
- [[llm-cascade]] — Sequential routing architecture that escalates queries to stronger, more expensive models only when cheaper ones fail.
- [[llm-embeddings]] — Low-dimensional vector representations of entire LLM models for routing, prediction, and multi-task transfer.
- [[model-routing]] — Core paradigm of dynamically dispatching queries to the most appropriate LLM from a heterogeneous pool.
- [[multimodal-llm-routing]] — Extension of model routing to multimodal queries (text+image), requiring joint embeddings for accurate selection.
- [[llm-recommendation-prompting]] — Four-component prompt framework (task description, user interest, candidate construction, prompting strategies) for using LLMs as recommenders.
- [[llm-rs-framework]] — LLM-RS: unified framework for leveraging LLMs as recommender systems, decomposing design choices into LLM selection and prompt engineering axes.
- [[oracle-gap]] — Structural divergence between real router performance and theoretical oracle maximum; root cause is model-recall failure and pool-size diminishing returns.
- [[perplexity-based-routing]] — Training-free LLM selection using intrinsic perplexity or KPPPL as a proxy for model-task compatibility.
- [[post-generation-routing]] — Evaluative routing paradigm (cascade) where response quality is assessed post-generation to decide on model escalation.
- [[pre-generation-routing]] — Predictive routing paradigm where a model is selected before generation to minimize latency overhead.
- [[prompt-recommendation]] — Dynamic suggestion of prompts to users, either for quality improvement or ethical alignment, before generation.
- [[query-complexity-routing]] — Pre-generation strategy estimating query difficulty to route queries to the cheapest model with sufficient capability.
- [[rl-based-routing]] — Class of routing methods learning or adapting model selection policies online from reinforcement learning signals.
- [[similarity-based-routing]] — Unsupervised routing family selecting models using semantic similarity to past query performance patterns.
- [[skill-based-routing]] — Approach matching granular task requirements to model capability profiles rather than aggregate performance scores.
- [[uncertainty-based-routing]] — Post-generation routing strategy selecting models based on calibrated output confidence or conformal prediction.
- [[user-interest-modeling]] — Encoding user preferences (short-term, long-term, retrieval-based, generation-based) into LLM recommendation prompts.

## Synthesis

- [[knowledge-mindmap]] — Wiki Knowledge Mindmap: taxonomy and organization of timing paradigms, implementation families, recommender integrations, evaluation benchmarks, and research gaps in LLM routing.

