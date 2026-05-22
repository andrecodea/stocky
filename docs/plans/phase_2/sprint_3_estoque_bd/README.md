# Sprint 3 — Schema de Estoque Completo

**Dev:** Backend Dev 2 (BD)  
**Duração estimada:** ~1 semana  
**Pré-requisito:** Sprint 1 concluído

## Objetivo

Expandir o schema para suportar lotes, inventário, Storage para fotos e RLS granular por role.

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | BD Dev 2 | ⏳ | ~35 min |
| T2 | [T2.md](T2.md) | BD Dev 2 | ⏳ | ~40 min |
| T3a | [T3a.md](T3a.md) | BD Dev 2 | ⏳ | ~30 min |
| T3b | [T3b.md](T3b.md) | BD Dev 2 | ⏳ | ~25 min |

## Contrato de saída

- Tabelas `lotes`, `estoque_atual` (view ou tabela materializada), `alertas` criadas
- RLS diferencia operador de admin em `movimentacoes` e `produtos`
- Bucket `product-images` configurado com políticas de acesso
- View `estoque_atual` retorna quantidade real por produto

## Próximo sprint
[[phase_2/sprint_4_estoque_api]] — Endpoints de estoque consumindo este schema.
