# Sprint 2 — FastAPI Foundation

**Dev:** Backend Dev 1 (API)  
**Duração estimada:** ~1 semana  
**Pré-requisito:** Sprint 1 concluído (banco com schema + RLS ativo)

## Objetivo

Criar a estrutura base do projeto FastAPI, conectar ao Supabase e implementar os endpoints de autenticação. Ao final deste sprint, qualquer endpoint futuro pode ser adicionado seguindo o padrão estabelecido aqui.

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | API Dev 1 | ✅ | ~25 min |
| T2 | [T2.md](T2.md) | API Dev 1 | ✅ | ~35 min |
| T3 | [T3.md](T3.md) | API Dev 1 | 🔄 | ~40 min |

## Contrato de saída

Ao concluir este sprint:
- `POST /auth/login` retorna JWT válido
- `GET /health` responde `200 OK`
- `GET /produtos` retorna lista (autenticado) ou `401` (não autenticado)
- Estrutura de pastas definida para os próximos sprints

## Próximo sprint
[[phase_2/sprint_3_estoque_bd]] — Schema de estoque completo e RLS por role.  
[[phase_2/sprint_4_estoque_api]] — Endpoints de estoque e produtos.
