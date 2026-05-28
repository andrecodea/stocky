# Sprint 11 — AI: Deep Agents (LangGraph)

**Pré-requisito:** Sprint 9 (`logs_ia` no DB) + Sprint 10 (webhook stubs no `webhook_service.py`)

## Objetivo

Implementar os 5 agentes ambientes com LangGraph. Cada agente tem estado tipado, subagentes como nós do grafo, e escreve output estruturado em `logs_ia`.

## Agentes

| Agente | Trigger | Subagentes | Output tipo |
|---|---|---|---|
| EstoqueAgent | Webhook `movimentacoes` INSERT/UPDATE | AnomalyDetector · RestockAdvisor · AlertDispatcher | `restock_alert` |
| ComercialAgent | Webhook `vendas` INSERT + pg_cron diário 08h | SalesVelocityTracker · DemandForecaster · TopProductsAnalyzer | `sales_report` |
| FinancialAgent | pg_cron diário 06h | MarginAnalyzer · LossDetector · ReportWriter | `daily_report` |
| LogisticsAgent | Webhook `transferencias` INSERT | MovementTracker · TransferOptimizer | `transfer_suggestion` |
| SupplyChainAgent | pg_cron semanal seg 07h | SupplierRanker · SeasonalityAnalyzer · WebResearcher (Tavily) | `supplier_report` |

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | `agents/base.py`: `write_log`, `get_llm`, fetchers de dados (stock, movements, sales, financials) | ⏳ | ~20 min |
| T2 | `agents/estoque/`: subagents + LangGraph graph + wire em `webhook_service` | ⏳ | ~40 min |
| T3 | `agents/comercial/`: subagents + LangGraph graph + wire | ⏳ | ~35 min |
| T4 | `agents/financial/`: subagents + LangGraph graph (inclui LLM call no ReportWriter) + wire | ⏳ | ~35 min |
| T5 | `agents/logistics/`: subagents + LangGraph graph + wire | ⏳ | ~25 min |
| T6 | `agents/supply_chain/`: subagents (inclui Tavily WebResearcher) + LangGraph graph + wire | ⏳ | ~40 min |

## Contrato de saída

- Trigger manual de cada agente via `pytest` com mock de dados grava entrada em `logs_ia`
- `GET /v1/ai/insights` retorna outputs de todos os agentes
- `POST /v1/webhooks/supabase` com payload de `movimentacoes` dispara EstoqueAgent de forma assíncrona

## Referência

Ver código detalhado em `docs/superpowers/plans/2026-05-28-03-ai-agents.md`.

## Próximo sprint
[[phase_5/sprint_12_rag_pipeline]]
