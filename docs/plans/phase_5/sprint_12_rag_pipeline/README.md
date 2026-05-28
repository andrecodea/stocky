# Sprint 12 — AI: RAG Pipeline (Embeddings)

**Pré-requisito:** Sprint 9 (`embeddings_ia` + `buscar_embeddings`) + Sprint 11 (`write_log` funcionando)

## Objetivo

Implementar o pipeline de embeddings para o RAG Copilot: embeda produtos, movimentações e outputs de agentes em `embeddings_ia`. O endpoint `POST /v1/ai/chat` (já implementado no Sprint 10) consome este store via `buscar_embeddings`.

## Tasks

| Task | Descrição | Tag | Status | Estimativa |
|---|---|---|---|---|
| T1 | `agents/rag/embedder.py`: `build_product_document`, `build_log_document`, `embed_and_store`, `re_embed_products`, `re_embed_log` | `ai` | ⏳ | ~30 min |
| T2 | Integrar `re_embed_log` no `agents/base.py::write_log` (fire-and-forget após gravar em `logs_ia`) | `ai` | ⏳ | ~15 min |
| T3 | Script `scripts/seed_embeddings.py`: embeda todos produtos e últimos 50 logs existentes (warm-up inicial) | `ai` | ⏳ | ~20 min |
| T4 | Testar chat RAG end-to-end: `POST /v1/ai/chat` → embed query → `buscar_embeddings` → LLM stream | `ai` | ⏳ | ~20 min |

## Contrato de saída

- `buscar_embeddings` retorna chunks relevantes para query de estoque
- `POST /v1/ai/chat` responde com contexto real (não hallucination)
- Novo output de agente automaticamente re-embedado

## Próximo sprint
[[phase_6/sprint_13_nextjs_setup]]
