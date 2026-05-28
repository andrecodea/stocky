# Sprint 9 — Supabase: Tabelas AI + Negócio

**Pré-requisito:** Sprints 1–3 concluídos (schema base + RLS base)

## Objetivo

Estender schema com tabelas para agentes AI, RAG, e módulos de negócio ainda ausentes. Habilitar pgvector e pg_cron. Documentar webhooks.

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | Migração: `logs_ia`, `embeddings_ia`, extension `vector`, HNSW index, função `buscar_embeddings` | ⏳ | ~30 min |
| T2 | Migração: `vendas`, `financeiro`, `fornecedores`, `transferencias`, `produto_fornecedor` | ⏳ | ~30 min |
| T3 | Migração: `ALTER produtos` (+ `categoria`), `ALTER movimentacoes` (+ `metodo`), atualizar view `estoque_atual` com `status` | ⏳ | ~20 min |
| T4 | Migração: RLS policies para todas as novas tabelas | ⏳ | ~25 min |
| T5 | Migração: pg_cron jobs (FinancialAgent diário 06h, ComercialAgent diário 08h, SupplyChainAgent semanal seg 07h) | ⏳ | ~20 min |
| T6 | `supabase/WEBHOOKS.md`: checklist manual de configuração dos webhooks no Dashboard | ⏳ | ~15 min |

## Contrato de saída

- Todas as tabelas do spec existem no Supabase
- `buscar_embeddings(vector, int)` funciona via RPC
- pg_cron jobs agendados
- Webhook setup documentado

## Referência

Ver detalhes de código em `docs/superpowers/plans/2026-05-28-01-supabase-schema.md`.

## Próximo sprint
[[phase_4/sprint_10_fastapi_rbac]]
