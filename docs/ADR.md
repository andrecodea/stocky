# Stocky ADR

Status: ativo
Atualizado: 2026-05-28

Este arquivo e o indice das decisoes arquiteturais do Stocky.

Use este documento para navegar pelas decisoes. Use os arquivos em `docs/adr/` para registrar o contexto, a decisao e as consequencias de cada decisao duravel.

## Hierarquia de referencias

```text
INDEX.md
  -> README.md
  -> docs/PRD.md
  -> docs/ROADMAP.md
  -> docs/ADR.md
       -> docs/adr/0001-lean-documentation.md
       -> docs/adr/0002-stack-and-surfaces.md
       -> docs/adr/0003-auth-rbac-and-data.md
       -> docs/adr/0004-ai-architecture.md
       -> docs/adr/0005-deploy-model.md
       -> docs/adr/TEMPLATE.md
  -> docs/architecture/*.html
```

## Indice

- [ADR 0001 - Modelo enxuto de documentacao](adr/0001-lean-documentation.md)
  - Decide que Stocky usa PRD, roadmap, ADRs e diagramas em vez de uma arvore de tasks.
- [ADR 0002 - Stack e superficies do produto](adr/0002-stack-and-surfaces.md)
  - Define React Native, Next.js, FastAPI, Supabase, OpenRouter, Coolify, Vercel e EAS.
- [ADR 0003 - Auth, RBAC e dados](adr/0003-auth-rbac-and-data.md)
  - Define Supabase Auth, roles `operator` e `admin`, RBAC no FastAPI e RLS no Supabase.
- [ADR 0004 - Arquitetura de IA](adr/0004-ai-architecture.md)
  - Separa agentes ambientes de chat RAG.
- [ADR 0005 - Modelo de deploy](adr/0005-deploy-model.md)
  - Define Coolify/VPS para backend/workers, Vercel para web, EAS para mobile e Supabase gerenciado.
- [ADR 0006 - Arquitetura do backend API](adr/0006-backend-api-architecture.md)
  - Define validacao de bearer token via Supabase Auth, RBAC com dependency injection, dual Supabase clients, e estrutura modular de routers/services/schemas.
- [ADR template](adr/TEMPLATE.md)
  - Modelo para registrar novas decisoes arquiteturais.

## Quando criar um novo ADR

Crie um novo ADR quando a mudanca:

- troca stack, provider, framework ou arquitetura;
- altera limites de responsabilidade entre mobile, web, backend, banco ou IA;
- muda auth, RBAC, RLS, dados sensiveis ou deploy;
- cria uma regra que futuros agentes nao devem rediscutir sem motivo forte.

Nao crie ADR para tarefas pequenas, bugs simples ou detalhes temporarios de implementacao.
