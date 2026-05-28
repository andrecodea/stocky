# Stocky — Roadmap POC (3 Semanas)

> **Contexto:** POC com desenvolvimento acelerado por IA. Foco em valor demonstrável ao final das 3 semanas, não em feature-completeness. Cada dev entrega a fatia vertical da sua responsabilidade.

## Divisão de Devs

| Role | Responsabilidade |
|------|-----------------|
| **Backend Dev 1** | API REST + IA (FastAPI, LangChain, OpenRouter) |
| **Backend Dev 2** | Banco de Dados (Supabase schema, Auth, RLS, Storage) |
| **Frontend Dev 1** | Conexão com endpoints (API client, Auth flow, State management) |
| **Frontend Dev 2** | Design (Design system, componentes, telas) |

---

## Semana 1 — Foundation (Backend Dev 1 + Dev 2 em paralelo)

> Frontend ainda não começa. Backend Dev 1 e Dev 2 trabalham em paralelo na mesma semana.

| Sprint | Dev | Objetivo | Status |
|--------|-----|----------|--------|
| [[phase_1/sprint_1_supabase_schema]] | BD Dev 2 | Schema inicial, Auth, RLS base | ✅ |
| [[phase_1/sprint_2_fastapi_foundation]] | API Dev 1 | FastAPI setup, estrutura, Auth middleware | 🔄 |

**Entregável semana 1:** `POST /auth/login` + `GET /me` funcionando. Schema `produtos`, `movimentacoes`, `perfis` no ar com RLS.

> ✅ Schema + RLS + seed aplicados no Supabase Cloud. FastAPI com `/ping` e `/health` — auth e endpoints de negócio pendentes.

---

## Semana 2 — Core Features (todos os 4 devs)

> Backend termina estoque + financeiro. Frontend começa design e conexão.

| Sprint | Dev | Objetivo | Status |
|--------|-----|----------|--------|
| [[phase_2/sprint_3_estoque_bd]] | BD Dev 2 | Lotes, view estoque_atual, Storage, índices | ✅ |
| [[phase_2/sprint_4_estoque_api]] | API Dev 1 | CRUD produtos, movimentações, alertas, upload foto | 🔄 |
| [[phase_2/sprint_5_financeiro]] | BD Dev 2 + API Dev 1 | Schema financeiro + endpoints de margem | ⏳ |
| [[phase_3/sprint_7_design]] | Frontend Dev 2 | Design system RN + telas de estoque | 🔄 |

**Entregável semana 2:** App mobile com telas navegáveis (sem dados reais). API com endpoints de estoque e financeiro testáveis via Swagger.

> ✅ View `estoque_atual` funcional. CRUD de produtos implementado como serviço Python (endpoints FastAPI pendentes). Design system entregue via Streamlit (MVP — React Native pós-POC). Módulo financeiro não iniciado.

---

## Semana 3 — AI + Integração Frontend

> IA entra na API. Frontend conecta telas reais. POC demo-ready.

| Sprint | Dev | Objetivo | Status |
|--------|-----|----------|--------|
| [[phase_3/sprint_6_ai]] | API Dev 1 | LangChain + OpenRouter: recomendações + busca web | ✅ |
| [[phase_3/sprint_8_frontend_conn]] | Frontend Dev 1 | Auth flow + conectar endpoints de estoque e alertas | ✅ |

**Entregável semana 3 (POC demo):**
- ~~Login funcional no app~~ *(auth adiado para pós-POC)*
- ✅ Lista de produtos com estoque real
- ✅ Alertas de esgotamento funcionando
- ✅ Recomendações de reposição geradas por IA (LangChain + OpenRouter + Tavily)
- ⏳ Cadastro de produto por foto (OCR) — pendente

---

## Escopo POC (fora do POC)

| Feature | Status |
|---------|--------|
| Módulo financeiro completo (relatórios, perdas) | Fora do POC |
| Previsão de ruptura por ML | Fora do POC |
| Leitor de código de barras | Fora do POC |
| RBAC granular por tela | Fora do POC |
| Tela de finanças no app | Fora do POC |

---

## Legenda de Status

| Emoji | Status |
|-------|--------|
| ⏳ | Pendente |
| 🔄 | Em progresso |
| ✅ | Concluído |
| 🔒 | Bloqueado |
