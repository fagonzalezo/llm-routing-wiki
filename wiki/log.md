# Wiki Log

Append-only chronological record of operations on the wiki. Each entry begins with `## [YYYY-MM-DD] <op> | <description>` so it's parseable with `grep "^## \[" log.md | tail -N`.

Operations:
- `ingest` — a source was processed into the wiki.
- `query` — a question was answered against the wiki (typically only logged when the answer was filed back as synthesis)
- `lint` — a health check was run.
- `schema` — the schema was modified.
- `shard` — an index was sharded.

---

## [2026-06-06] schema | Initialized wiki structure: SCHEMA.md, index.md, log.md, .page-template.md
## [2026-06-06] ingest | chen-2023-frugalgpt — FrugalGPT: budget-aware LLM cascade pipeline (Chen 2023)
## [2026-06-06] ingest | ong-2025-routellm — RouteLLM: preference-trained binary LLM router framework (Ong 2025)
## [2026-06-06] ingest | jitkrittum-2026-universal-routing — UniRoute: universal routing for dynamic model pools (Jitkrittum 2026)
## [2026-06-06] ingest | zhuang-2025-embedllm — EmbedLLM: compact LLM embedding via reconstruction (Zhuang 2025)
## [2026-06-06] ingest | chen-2025-irtnet — IrtNet: IRT-based compact LLM ability representations (Chen 2025)
## [2026-06-06] ingest | guo-2026-cascade — CASCADE: case-based continual adaptation during deployment (Guo 2026)
## [2026-06-06] ingest | huang-2025-routereval — RouterEval: comprehensive LLM routing benchmark (Huang 2025)
## [2026-06-06] ingest | li-2026-llmrouterbench — LLMRouterBench: large-scale routing benchmark and framework (Li 2026)
## [2026-06-06] ingest | li-2025-predictive-routing — kNN beats complex learned routers for LLM routing (Li 2025)
## [2026-06-06] ingest | fang-2025-device-cloud — GAPG: RL-based device-cloud collaborative inference (Fang 2025)
## [2026-06-06] ingest | ma-2026-mmr-bench — MMR-Bench: multimodal LLM routing benchmark (Ma 2026)
## [2026-06-06] ingest | okokamoto-2026-trust-routing — BELLA: skill-profile transparent cost-aware routing (Okamoto 2026)
## [2026-06-06] ingest | nelson-2025-ethical-rec — Ethical prompt recommendation via collaborative filtering (Nelson 2025)
## [2026-06-06] ingest | xu-2024-llm-recommender — LLM-RS: comprehensive framework and empirical analysis of LLMs as recommender systems (Xu et al. 2024); created concepts: llm-rs-framework, user-interest-modeling, llm-recommendation-prompting
## [2026-06-06] ingest | shnitzer-2024-benchmark-routing — Benchmark-based LLM routing via kNN correctness predictors and OOD-aware scoring (Shnitzer et al. 2024)
## [2026-06-06] ingest | poon-2026-contextual-bandits — Contextual bandit framework for online multi-step LLM selection; Greedy LinUCB + myopic regret (Poon 2026)
## [2026-06-06] ingest | kim-2024-llm-rec — A-LLMRec: all-round LLM+CF recommender via frozen alignment network; created entity a-llmrec, concept llm-cf-alignment (Kim et al. KDD 2024)
## [2026-06-06] ingest | moslem-2026-routing-survey — Dynamic Model Routing and Cascading Survey (Moslem & Kelleher 2026); created concepts: rl-based-routing, uncertainty-based-routing
## [2026-06-06] ingest | varangot-reille-2025-routing-survey — Comprehensive Survey on Routing Strategies for Resource Optimisation (Varangot-Reille et al. 2025); created concepts: pre-generation-routing, post-generation-routing, similarity-based-routing, query-complexity-routing
## [2026-06-06] ingest | owodunni-2023-koya — Koya: zero-finetune LLM recommender via KPPPL (Owodunni & Emezue 2023); created entity: koya, concept: perplexity-based-routing
## [2026-06-06] ingest | advanced-architectures-llm-routing — Survey on LLM Routing and Performance Prediction (Moslem & Kelleher 2026); created concept: oracle-gap

