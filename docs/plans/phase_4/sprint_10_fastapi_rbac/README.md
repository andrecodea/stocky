# Sprint 10 — FastAPI: RBAC + Todos os Endpoints

**Pré-requisito:** Sprint 9 (schema completo) + Sprint 2 (FastAPI base)

## Objetivo

Refatorar FastAPI com JWT middleware real (Supabase Auth), RBAC (operador/admin), e implementar todos os endpoints do spec incluindo SSE e webhook receiver.

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | `backend/api/deps.py`: `get_supabase_user`, `require_admin`, `require_operator` — validação JWT via Supabase + leitura de role de `perfis` | ⏳ | ~30 min |
| T2 | `backend/api/routers/auth.py`: `POST /v1/auth/login`, `GET /v1/me` | ⏳ | ~20 min |
| T3 | `backend/api/routers/products.py` + `backend/services/product_service.py`: `GET /v1/products`, `POST /v1/products`, `GET /v1/products/{id}`, `GET /v1/products/lookup` (barcode + Gemini Vision) | ⏳ | ~50 min |
| T4 | `backend/api/routers/movements.py` + `backend/services/movement_service.py`: `GET /v1/movements`, `POST /v1/movements` | ⏳ | ~30 min |
| T5 | `backend/api/routers/financials.py` + `backend/services/financial_service.py`: `GET /v1/financials/summary`, `GET /v1/reports/daily` | ⏳ | ~30 min |
| T6 | `backend/api/routers/ai.py`: `GET /v1/ai/insights`, `POST /v1/ai/chat` (SSE streaming via LangChain + pgvector) | ⏳ | ~40 min |
| T7 | `backend/api/routers/webhooks.py` + `backend/services/webhook_service.py`: `POST /v1/webhooks/supabase` com secret validation + async dispatch stubs | ⏳ | ~25 min |
| T8 | `backend/Dockerfile` + `docker-compose.yml` | ⏳ | ~15 min |

## Contrato de saída

- Todos endpoints do spec respondem via Swagger em `http://localhost:8000/docs`
- `401` sem JWT, `403` role errado, `201`/`200` com JWT válido
- `POST /v1/ai/chat` retorna `text/event-stream` com deltas SSE
- `POST /v1/webhooks/supabase` retorna `202` com secret correto

## Referência

Ver código detalhado em `docs/superpowers/plans/2026-05-28-02-fastapi-backend.md`.

## Próximo sprint
[[phase_5/sprint_11_deep_agents]]
