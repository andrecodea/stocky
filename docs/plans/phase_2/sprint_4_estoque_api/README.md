# Sprint 4 — Endpoints de Estoque

**Dev:** Backend Dev 1 (API)  
**Duração estimada:** ~1 semana  
**Pré-requisito:** Sprint 2 (FastAPI) + Sprint 3 (schema estoque) concluídos

## Objetivo

Implementar todos os endpoints CRUD de produtos e movimentações, com lógica de alertas de esgotamento.

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | API Dev 1 | ⏳ | ~30 min |
| T2 | [T2.md](T2.md) | API Dev 1 | ⏳ | ~40 min |
| T3 | [T3.md](T3.md) | API Dev 1 | ⏳ | ~35 min |

## Contrato de saída

- `GET /produtos` — lista com estoque atual
- `POST /produtos` — criar produto (admin)
- `POST /movimentacoes` — registrar entrada/saída
- `GET /estoque/alertas` — produtos abaixo do mínimo
- `POST /produtos/{id}/foto` — upload de imagem

## Próximo sprint
[[phase_2/sprint_5_financeiro]] — Schema e endpoints financeiros.
