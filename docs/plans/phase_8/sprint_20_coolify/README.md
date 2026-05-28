# Sprint 20 — Infra: Deploy no Coolify

**Pré-requisito:** Sprints 10–12 (FastAPI + Agents funcionando localmente)

## Objetivo

Deploy do backend FastAPI + AI workers no Coolify (VPS), com Traefik, SSL automático, e Supabase webhooks apontando para a VPS.

## Tasks

| Task | Descrição | Tag | Status | Estimativa |
|---|---|---|---|---|
| T1 | Configurar `docker-compose.yml` com serviços `api` e `workers` (FastAPI + asyncio event loop para agentes) | `backend` | ⏳ | ~25 min |
| T2 | Adicionar projeto no Coolify: conectar repositório, configurar env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `OPENROUTER_API_KEY`, `WEBHOOK_SECRET`, `TAVILY_API_KEY`) | `backend` | ⏳ | ~20 min |
| T3 | Configurar domínio no Coolify (`api.stocky.app`) + Traefik SSL via Let's Encrypt | `backend` | ⏳ | ~15 min |
| T4 | Atualizar webhooks Supabase (Dashboard → Database → Webhooks) para apontar para `https://api.stocky.app/v1/webhooks/supabase` | `database` | ⏳ | ~10 min |
| T5 | Atualizar pg_cron: `app.fastapi_url` → `https://api.stocky.app/v1` no Supabase Dashboard | `database` | ⏳ | ~10 min |
| T6 | Smoke test pós-deploy: `GET /health` → 200, `POST /webhooks/supabase` com secret correto → 202 | `backend` | ⏳ | ~15 min |

## Contrato de saída

- `https://api.stocky.app/v1/health` retorna `{"status":"ok"}`
- Webhook de movimentação dispara EstoqueAgent e grava em `logs_ia` na Supabase Cloud
- Next.js no Vercel e app Expo conseguem conectar na API de produção

## Referência

`supabase/WEBHOOKS.md` — checklist de configuração manual
