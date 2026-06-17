# ADR 0005 - Modelo de deploy

Status: aceito
Data: 2026-05-28
Indice: [ADR](../ADR.md)

## Contexto

Backend e workers de IA precisam de variaveis de ambiente, endpoints de webhook e comportamento de servico persistente. Frontend e mobile tem necessidades de deploy diferentes.

## Decisao

Deploy:

- FastAPI e workers de IA no Coolify/VPS com Docker.
- Next.js na Vercel.
- React Native pelo Expo EAS.
- Supabase como banco/auth/storage gerenciado.

## Consequencias

- Backend tem alvo HTTPS estavel para webhooks.
- Web admin pode ser publicado independentemente.
- Builds mobile nao dependem do deploy do backend.
- Secrets ficam nas configuracoes das plataformas, nao nos docs do repositorio.
