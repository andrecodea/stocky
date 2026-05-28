# Stocky — System Design Spec

**Date:** 2026-05-28  
**Status:** Approved  
**Stack:** FastAPI · Deep Agents (LangGraph) · Next.js · React Native (Expo) · Supabase · OpenRouter · Coolify/VPS · Vercel · Expo EAS

---

## 1. Overview

Stocky is an AI-powered inventory management system targeting small-to-medium retail businesses. It consists of:

- A **React Native mobile app** for stock operators (inventory tracking, movements, alerts)
- A **Next.js web dashboard** for admins (financials, reports, AI insights, team management)
- A **FastAPI backend** handling REST, auth, RBAC, and agent orchestration
- A **Deep Agents AI layer** with one ambient root agent per business module, spawning managed subagents autonomously
- A **RAG chat copilot** for reactive Q&A on inventory and financial data

---

## 2. Architecture

### 2.1 Layers

| Layer | Technology | Hosting |
|---|---|---|
| Mobile | React Native (Expo) | EAS Build → Play Store / TestFlight |
| Web Admin | Next.js | Vercel |
| Backend API | FastAPI + Uvicorn | Docker container — Coolify/VPS |
| AI Workers | Deep Agents (LangChain/LangGraph) | Docker container — Coolify/VPS |
| Database / Auth | Supabase (Postgres + Auth + RLS + Realtime + Storage + pgvector + Webhooks + pg_cron) | Supabase Cloud |
| LLM Routing | OpenRouter | External API |

### 2.2 Data Flow

```
Supabase Event / pg_cron
  → HTTP Webhook → FastAPI
    → spawns Deep Agent (root)
      → managed subagents execute in parallel
        → output JSON written to Supabase ai_logs
          → Realtime subscription → frontend renders insight/alert
```

Chat Q&A (RAG):
```
User query → embed (text-embedding-3-small via OpenRouter)
  → pgvector cosine similarity → top-K chunks retrieved
    → augmented prompt → LLM via OpenRouter → response streamed to client
```

### 2.3 Key Design Decisions

- **Ambient agents, not user-triggered.** Deep Agents run autonomously on DB events or schedules. Frontend only consumes results via Realtime — no HTTP polling, no agent waiting inside a request.
- **RAG is separate from Deep Agents.** Chat requires low latency; pgvector retrieval + LLM is faster and simpler than spawning an agent for each question.
- **Agent decoupling via Supabase.** ComercialAgent writes to `ai_logs`; EstoqueAgent and SupplyChainAgent read from it. No direct inter-agent calls.
- **All agent outputs are structured JSON** in `ai_logs`. Frontend has no agent-specific endpoints — it queries and subscribes to this single table.
- **RBAC: two roles only.** Operator = mobile app (inventory ops). Admin = web dashboard (financials + team + all modules). No HR agent — team management is a Settings page.

---

## 3. AI Layer

### 3.1 Deep Agents (Ambient)

One root agent per module. Each root agent spawns managed subagents as needed.

#### EstoqueAgent
- **Trigger:** Supabase DB Webhook (on stock movement insert / update)
- **Subagents:** AnomalyDetector · RestockAdvisor · AlertDispatcher
- **Output:** `{ type: "restock_alert", product_id, recommended_qty, urgency }`

#### ComercialAgent *(feeds EstoqueAgent + SupplyChainAgent)*
- **Trigger:** DB Webhook (on sale insert) + pg_cron daily
- **Subagents:** SalesVelocityTracker · DemandForecaster · TopProductsAnalyzer
- **Output:** `{ type: "sales_report", top_products, demand_forecast, avg_turnover }`

#### FinancialAgent
- **Trigger:** pg_cron daily
- **Subagents:** MarginAnalyzer · LossDetector · ReportWriter
- **Output:** `{ type: "daily_report", avg_margin, top_losses, recommendations }`

#### LogisticsAgent
- **Trigger:** DB Webhook (on stock transfer insert)
- **Subagents:** MovementTracker · TransferOptimizer
- **Output:** `{ type: "transfer_suggestion", from, to, items }`

#### SupplyChainAgent *(reads ComercialAgent output)*
- **Trigger:** pg_cron weekly
- **Subagents:** SupplierRanker · SeasonalityAnalyzer · WebResearcher (Tavily)
- **Output:** `{ type: "supplier_report", rupture_risk, seasonality }`

### 3.2 RAG Chat Copilot

- **Embedding model:** text-embedding-3-small via OpenRouter
- **Vector store:** Supabase pgvector (`ai_embeddings` table, cosine similarity)
- **Retriever:** LangChain `SupabaseVectorStore`, top-K = 5
- **Indexed data:** products + stock · agent reports · financial movements · sales history
- **Re-embedding trigger:** on agent report save + on significant stock change

---

## 4. Backend (FastAPI)

### 4.1 Responsibilities
- JWT validation (Supabase Auth tokens)
- RBAC enforcement (Operator / Admin) per route
- Business logic endpoints (products, movements, financials)
- Supabase webhook receiver → agent trigger
- RAG chat endpoint (streaming)

### 4.2 Key Endpoints

| Method | Path | Role | Description |
|---|---|---|---|
| POST | `/auth/login` | public | Supabase auth passthrough |
| GET | `/me` | any | Current user profile + role |
| GET | `/products` | any | List products with stock status |
| POST | `/products` | operator / admin | Create product |
| POST | `/movements` | operator / admin | Register stock movement |
| GET | `/movements` | any | List movements with filters |
| GET | `/financials/summary` | admin | Financial KPIs |
| GET | `/reports/daily` | admin | Latest FinancialAgent report |
| GET | `/ai/insights` | any | Latest agent outputs from ai_logs |
| POST | `/ai/chat` | any | RAG chat (streaming SSE) |
| POST | `/webhooks/supabase` | internal | Supabase DB webhook receiver |

---

## 5. Frontend

### 5.1 Next.js Web (Admin)

**Navigation:** sidebar with 7 pages + floating Copilot widget (bottom-right FAB)

| Page | Key Content |
|---|---|
| Dashboard | KPIs · active alerts · agent insights feed · sales/margin charts |
| Estoque | Product table with stock status · filters · bulk actions |
| Financeiro | Revenue · margins · losses · daily FinancialAgent report |
| Comercial | Sales velocity · demand forecast · top products ranking |
| Logística | Transfer suggestions (LogisticsAgent) · movement history |
| Supply Chain | Supplier ranking · rupture risk · seasonality heatmap |
| Configurações | Team management (users + roles) · notifications · agent toggles · company info |

**Copilot:** floating chat widget (not a page), accessible from any screen. Connects to `/ai/chat` SSE endpoint.

### 5.2 React Native Mobile (Operator)

**Navigation:** bottom nav with 4 tabs + floating Copilot FAB

| Tab | Key Content |
|---|---|
| Home | KPI grid · urgent alerts · agent insights |
| Estoque | Product list with status chips · search bar |
| Movimentações | Entrada / Saída / Ajuste buttons → Scan sub-flow → Confirm |
| Alertas | Critical / warning alerts + agent insights |

**Movimentações flow:**
1. Choose type (Entrada / Saída / Ajuste)
2. Identify product via:
   - **Barcode / QR scan** → DB lookup
   - **Camera photo** → Gemini Vision → DB match
   - **Text search** by name or SKU
   - **Recent movements list** (one-tap repeat)
3. Set quantity + optional note → confirm

**Copilot:** full-screen chat (Stocky Copilot), triggered by green FAB on all tabs.

---

## 6. Data Model (Key Tables)

| Table | Purpose |
|---|---|
| `products` | SKU, name, category, min stock, unit, photo URL |
| `stock_levels` | Current qty per product per location |
| `movements` | Stock in/out/adjust entries with operator, timestamp, method (barcode/photo/manual) |
| `financials` | Revenue, cost, margin entries per product/period |
| `sales` | Sales records feeding ComercialAgent |
| `suppliers` | Supplier info + lead times |
| `ai_logs` | All agent outputs (structured JSON, type-tagged) |
| `ai_embeddings` | pgvector embeddings for RAG |
| `profiles` | User profiles linked to Supabase Auth (role: operator/admin) |

---

## 7. Infrastructure

| Service | Provider | Notes |
|---|---|---|
| FastAPI + AI workers | Coolify on own VPS | Docker compose, Traefik reverse proxy, auto SSL |
| Next.js | Vercel | Zero-config, CDN global |
| React Native | Expo EAS | APK/IPA builds, OTA updates |
| Database | Supabase Cloud | Includes Auth, RLS, Realtime, Storage, pgvector, pg_cron |
| LLMs | OpenRouter | Model selection per agent (cost vs capability) |

---

## 8. Visual References

- `docs/architecture/system-overview.html` — full system architecture diagram
- `docs/architecture/ai-modules.html` — AI agents detail (subagents, triggers, outputs)
- `docs/architecture/nextjs-screens.html` — Next.js admin dashboard mockup (interactive)
- `docs/architecture/rn-screens.html` — React Native mobile app mockup (interactive)
