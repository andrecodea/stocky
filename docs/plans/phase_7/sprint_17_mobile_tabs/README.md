# Sprint 17 — React Native: 4 Tabs

**Pré-requisito:** Sprint 16 (setup + auth) + Sprint 10 (API no ar)

## Objetivo

Implementar as 4 tabs do app operador com dados reais.

## Tabs

| Tab | Conteúdo |
|---|---|
| Home | KPI grid (produtos totais, alertas críticos, movimentações hoje) · feed `logs_ia` via Realtime |
| Estoque | Lista produtos com `StatusChip` (ok/baixo/crítico) · busca por nome/SKU |
| Movimentações | Botões Entrada/Saída/Ajuste → abre fluxo (Sprint 18) · lista últimas movimentações |
| Alertas | Lista `restock_alert` e `transfer_suggestion` de `logs_ia` por urgência |

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | `lib/api.ts`: funções fetch para `getProducts`, `getMovements`, `getInsights`, `getKpis` | ⏳ | ~25 min |
| T2 | Componentes: `KpiCard`, `StatusChip`, `ProductListItem`, `AlertCard` | ⏳ | ~35 min |
| T3 | Tab Home: KPIs + feed Realtime de `logs_ia` (Supabase channel) | ⏳ | ~30 min |
| T4 | Tab Estoque: FlatList de produtos com busca + StatusChip | ⏳ | ~25 min |
| T5 | Tab Movimentações: 3 botões de ação + FlatList de últimas movimentações | ⏳ | ~20 min |
| T6 | Tab Alertas: lista de insights com urgência colorida | ⏳ | ~20 min |

## Contrato de saída

- Todas as 4 tabs renderizam dados reais
- Home atualiza ao receber novo `logs_ia` (Realtime)
- Busca no Estoque filtra localmente

## Referência visual

`docs/architecture/rn-screens.html`

## Próximo sprint
[[phase_7/sprint_18_movimentacoes_flow]]
