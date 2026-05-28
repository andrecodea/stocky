# Stocky — Roadmap

> **Spec aprovado:** `docs/superpowers/specs/2026-05-28-stocky-design.md`  
> **Stack:** FastAPI · LangGraph (Deep Agents) · Next.js · React Native (Expo) · Supabase · OpenRouter · Coolify/VPS · Vercel · EAS

---

## ✅ Phase 1 — POC (Concluído)

> MVP Streamlit para validação. Substituído pela arquitetura de produção na Phase 2+.

| Sprint | Objetivo | Status |
|---|---|---|
| [[phase_1/sprint_1_supabase_schema]] | Schema inicial, Auth, RLS base (`produtos`, `movimentacoes`, `perfis`) | ✅ |
| [[phase_1/sprint_2_fastapi_foundation]] | FastAPI setup, estrutura, `/ping` `/health` | ✅ |
| [[phase_2/sprint_3_estoque_bd]] | Lotes, view `estoque_atual`, Storage, índices | ✅ |
| [[phase_2/sprint_4_estoque_api]] | CRUD produtos, movimentações (serviço Python) | ✅ |
| [[phase_2/sprint_5_financeiro]] | Schema financeiro + endpoints margem/perdas | ⏳ (pulado no POC) |
| [[phase_3/sprint_6_ai]] | LangChain single agent: recomendações + busca web | ✅ |
| [[phase_3/sprint_7_design]] | MVP Streamlit: Dashboard, Estoque, Chat IA | ✅ |
| [[phase_3/sprint_8_frontend_conn]] | Streamlit conectado ao Supabase com dados reais | ✅ |

**POC entregável:** app Streamlit com estoque real + alertas + chat IA (LangChain + OpenRouter + Tavily).

---

## 🔄 Phase 2 — Produção: Backend + DB

> Completa o backend FastAPI com RBAC real, todos os endpoints do spec, e estende o schema Supabase com tabelas AI + negócio.

| Sprint | Objetivo | Status |
|---|---|---|
| [[phase_4/sprint_9_supabase_ai]] | Novas tabelas: `logs_ia`, `embeddings_ia`, `vendas`, `financeiro`, `fornecedores`, `transferencias` + pgvector + pg_cron + RLS | ⏳ |
| [[phase_4/sprint_10_fastapi_rbac]] | FastAPI: JWT middleware, RBAC deps, todos endpoints do spec (`/products`, `/movements`, `/financials`, `/ai/insights`, `/ai/chat` SSE, `/webhooks/supabase`) | ⏳ |

**Entregável:** API completa testável via Swagger. Todos os endpoints do spec respondendo com dados reais.

---

## ⏳ Phase 3 — Produção: AI Layer

> 5 Deep Agents autônomos (LangGraph) + pipeline RAG para o Copilot.

| Sprint | Objetivo | Status |
|---|---|---|
| [[phase_5/sprint_11_deep_agents]] | EstoqueAgent · ComercialAgent · FinancialAgent · LogisticsAgent · SupplyChainAgent — cada um com subagents, output em `logs_ia` | ⏳ |
| [[phase_5/sprint_12_rag_pipeline]] | Embedder pipeline: `text-embedding-3-small` → `embeddings_ia` + função `buscar_embeddings` + re-embedding triggers | ⏳ |

**Entregável:** Agentes rodando via webhook Supabase e pg_cron. Chat RAG retornando respostas baseadas em dados reais.

---

## ⏳ Phase 4 — Produção: Next.js Web Admin

> Dashboard admin com 7 páginas + Copilot flutuante. Hosted no Vercel.

| Sprint | Objetivo | Status |
|---|---|---|
| [[phase_6/sprint_13_nextjs_setup]] | Next.js 15 + TypeScript + Tailwind + shadcn/ui + Supabase client + auth flow | ⏳ |
| [[phase_6/sprint_14_nextjs_pages]] | 7 páginas: Dashboard · Estoque · Financeiro · Comercial · Logística · Supply Chain · Configurações | ⏳ |
| [[phase_6/sprint_15_nextjs_copilot]] | Copilot FAB flutuante: chat SSE + Realtime subscription em `logs_ia` | ⏳ |

**Entregável:** Web admin completo no Vercel com dados reais e insights de agentes em tempo real.

---

## ⏳ Phase 5 — Produção: React Native Mobile

> App operador com 4 tabs + Copilot. Build via Expo EAS.

| Sprint | Objetivo | Status |
|---|---|---|
| [[phase_7/sprint_16_expo_setup]] | Expo + TypeScript + NativeWind + Supabase client + auth flow | ⏳ |
| [[phase_7/sprint_17_mobile_tabs]] | 4 tabs: Home · Estoque · Movimentações · Alertas | ⏳ |
| [[phase_7/sprint_18_movimentacoes_flow]] | Fluxo completo: tipo → identificar (barcode/foto Gemini/busca/recente) → confirmar | ⏳ |
| [[phase_7/sprint_19_mobile_copilot]] | Copilot FAB: chat full-screen + SSE streaming | ⏳ |

**Entregável:** APK via EAS Build com fluxo de movimentações completo e copilot funcional.

---

## ⏳ Phase 6 — Infra

> Deploy produção no Coolify/VPS.

| Sprint | Objetivo | Status |
|---|---|---|
| [[phase_8/sprint_20_coolify]] | Docker Compose (FastAPI + AI workers) no Coolify + Traefik + SSL + env vars + Supabase webhooks apontando para VPS | ⏳ |

---

## Legenda

| Emoji | Status |
|---|---|
| ⏳ | Pendente |
| 🔄 | Em progresso |
| ✅ | Concluído |
| 🔒 | Bloqueado |
