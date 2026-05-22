# Sprint 5 — Módulo Financeiro

**Devs:** Backend Dev 2 (BD) + Backend Dev 1 (API)  
**Duração estimada:** ~1 semana  
**Pré-requisito:** Sprint 3 concluído (schema estoque)

## Objetivo

Criar schema financeiro (custos, receitas, vendas) e endpoints de relatórios de margem e perdas.

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | BD Dev 2 | ⏳ | ~35 min |
| T2 | [T2.md](T2.md) | BD Dev 2 | ⏳ | ~30 min |
| T3 | [T3.md](T3.md) | API Dev 1 | ⏳ | ~40 min |
| T4 | [T4.md](T4.md) | API Dev 1 | ⏳ | ~35 min |

## Contrato de saída

- Tabelas `vendas`, `itens_venda` e view `margem_produto` criadas
- `GET /financeiro/resumo` retorna receita, custo e margem do período
- `GET /financeiro/margem` retorna margem por produto
- `GET /financeiro/perdas` retorna valor de movimentações do tipo `ajuste` negativo

## Próximo sprint
[[phase_3/sprint_6_ai]] — LangChain + OpenRouter para recomendações e previsão de ruptura.
