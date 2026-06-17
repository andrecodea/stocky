# ADR 0002 - Stack e superficies do produto

Status: aceito
Data: 2026-05-28
Indice: [ADR](../ADR.md)

## Contexto

Stocky precisa de um app operacional, um painel admin, uma API backend e recursos de IA baseados em dados reais do negocio.

## Decisao

Usar:

- React Native com Expo para mobile.
- Next.js para web admin.
- FastAPI para backend.
- Supabase para Postgres, Auth, Storage, RLS, Realtime, pgvector e pg_cron.
- OpenRouter para acesso a modelos.
- Coolify/VPS para API e workers.
- Vercel para web admin.
- EAS para builds mobile.

## Consequencias

- Mobile e web evoluem de forma independente.
- Backend controla autorizacao e contratos de negocio.
- Supabase reduz carga de infraestrutura.
- Recursos de IA compartilham a mesma base de dados e auth.
