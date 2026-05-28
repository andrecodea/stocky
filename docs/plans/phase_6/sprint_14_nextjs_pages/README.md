# Sprint 14 — Next.js: 7 Páginas Admin

**Pré-requisito:** Sprint 13 (setup + auth) + Sprint 10 (API no ar)

## Objetivo

Implementar as 7 páginas do dashboard admin com dados reais via API FastAPI + Supabase Realtime para insights de agentes.

## Páginas

| Página | Rota | Conteúdo principal | Role |
|---|---|---|---|
| Dashboard | `/dashboard` | KPI cards · alertas ativos · feed `logs_ia` (Realtime) · charts vendas/margem | admin |
| Estoque | `/estoque` | Tabela produtos com status chips · filtros · ações em lote | admin |
| Financeiro | `/financeiro` | Receita/custo/margem · perdas · relatório FinancialAgent | admin |
| Comercial | `/comercial` | Velocidade vendas · previsão demanda · ranking produtos (ComercialAgent) | admin |
| Logística | `/logistica` | Sugestões transferência (LogisticsAgent) · histórico movimentações | admin |
| Supply Chain | `/supply-chain` | Ranking fornecedores · risco ruptura · heatmap sazonalidade (SupplyChainAgent) | admin |
| Configurações | `/configuracoes` | Gerenciar usuários + roles · toggles de agentes · info empresa | admin |

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | `lib/api.ts`: funções fetch tipadas para cada endpoint FastAPI (`getProducts`, `getMovements`, `getInsights`, `getFinancialSummary`, etc.) | ⏳ | ~30 min |
| T2 | Componentes compartilhados: `KpiCard`, `StatusChip`, `InsightCard`, `DataTable` | ⏳ | ~35 min |
| T3 | Página Dashboard: KPIs via `getFinancialSummary` + feed `logs_ia` via Supabase Realtime subscription | ⏳ | ~35 min |
| T4 | Página Estoque: tabela `getProducts` com filtros client-side | ⏳ | ~25 min |
| T5 | Página Financeiro: `getFinancialSummary` + `getDailyReport` | ⏳ | ~25 min |
| T6 | Página Comercial: `getInsights?type=sales_report` | ⏳ | ~20 min |
| T7 | Página Logística: `getInsights?type=transfer_suggestion` + `getMovements` | ⏳ | ~20 min |
| T8 | Página Supply Chain: `getInsights?type=supplier_report` com heatmap de sazonalidade | ⏳ | ~25 min |
| T9 | Página Configurações: listagem e edição de roles via Supabase `perfis` + toggles (estado local por agora) | ⏳ | ~30 min |

## Contrato de saída

- Todas as 7 páginas renderizam dados reais sem erros
- Dashboard atualiza automaticamente quando novo `logs_ia` é inserido (Realtime)
- Filtros de estoque funcionam client-side

## Referência visual

`docs/architecture/nextjs-screens.html`

## Próximo sprint
[[phase_6/sprint_15_nextjs_copilot]]
