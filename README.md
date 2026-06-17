# Stocky

Stocky e um sistema de gerenciamento inteligente de estoque para pequenos e medios negocios.

O produto combina um app operacional, um painel administrativo, um backend FastAPI, Supabase e uma camada de IA para alertas, recomendacoes e consultas sobre estoque, vendas e financeiro.

## Fonte de verdade

- [Index](INDEX.md) - ponto central de navegacao da documentacao.
- [Setup](docs/SETUP.md) - ambiente local, variaveis e validacao.
- [PRD](docs/PRD.md) - produto, usuarios, escopo e criterios de aceite.
- [Roadmap](docs/ROADMAP.md) - milestones implementaveis e validacoes.
- [ADR](docs/ADR.md) - indice de decisoes arquiteturais.
- [Diagramas HTML](docs/architecture/system-overview.html) - arquitetura e telas navegaveis.
- [AGENTS.md](AGENTS.md) - instrucoes para agentes/codegen.

## Stack alvo

- Backend: Python 3.13, FastAPI, Supabase client.
- Banco/Auth: Supabase PostgreSQL, Auth, RLS, Storage, Realtime, pgvector, pg_cron.
- IA: LangGraph/Deep Agents, RAG com pgvector, OpenRouter.
- Web admin: Next.js.
- Mobile: React Native com Expo.
- Deploy: Coolify/VPS para API e workers, Vercel para web, EAS para mobile.

## Escopo principal

- Cadastro e consulta de produtos.
- Movimentacoes de entrada, saida e ajuste.
- Alertas de estoque minimo e risco de ruptura.
- Financeiro basico: custos, receitas, margem e perdas.
- IA para insights, recomendacoes e chat com contexto real.
- RBAC com dois papeis: `operator` e `admin`.

## Como rodar

Backend:

```bash
uv sync
uv run python backend/api/app.py
```

Mobile:

```bash
cd mobile
npm install
npm run start
```

O app mobile atual cobre login, estoque, resumo financeiro para admin, IA com fallback local de estoque, alertas e registro de movimentacoes por busca textual. Scanner, camera e upload de fotos ficam fora do MVP atual.

Enquanto o backend produtivo nao estiver completo, comece pelo [Index](INDEX.md) e consulte o [Roadmap](docs/ROADMAP.md) para o proximo contrato implementavel.

## Diagramas

- [System overview](docs/architecture/system-overview.html)
- [DB schema](docs/architecture/db-schema.html)
- [AI modules](docs/architecture/ai-modules.html)
- [API endpoints](docs/architecture/api-endpoints.html)
- [Next.js screens](docs/architecture/nextjs-screens.html)
- [React Native screens](docs/architecture/rn-screens.html)
