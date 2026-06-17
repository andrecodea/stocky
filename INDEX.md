# Stocky Index

Este e o ponto de partida da documentacao do Stocky.

Use este arquivo para navegar. Os documentos abaixo tem responsabilidades diferentes e nao devem duplicar conteudo entre si.

## Hierarquia

```text
INDEX.md
  -> README.md
  -> docs/SETUP.md
  -> docs/PRD.md
  -> docs/ROADMAP.md
  -> docs/ADR.md
       -> docs/adr/*.md
  -> docs/architecture/*.html
  -> AGENTS.md / CLAUDE.md
```

## Produto

- [README](README.md) - visao curta, stack, comandos e links principais.
- [PRD](docs/PRD.md) - usuarios, problema, escopo, requisitos e criterios de aceite.

## Setup

- [Setup](docs/SETUP.md) - ambiente local, variaveis, comandos, validacao e troubleshooting.
- [Mobile test runbook](docs/MOBILE_TEST_RUNBOOK.md) - logins, senha e comandos para testar o app no celular.

## Execucao

- [Roadmap](docs/ROADMAP.md) - marcos implementaveis, entregaveis e validacoes.

## Decisoes

- [ADR](docs/ADR.md) - indice de decisoes arquiteturais.
- [ADR 0001 - Modelo enxuto de documentacao](docs/adr/0001-lean-documentation.md)
- [ADR 0002 - Stack e superficies do produto](docs/adr/0002-stack-and-surfaces.md)
- [ADR 0003 - Auth, RBAC e dados](docs/adr/0003-auth-rbac-and-data.md)
- [ADR 0004 - Arquitetura de IA](docs/adr/0004-ai-architecture.md)
- [ADR 0005 - Modelo de deploy](docs/adr/0005-deploy-model.md)
- [ADR 0006 - Arquitetura do backend API](docs/adr/0006-backend-api-architecture.md)
- [ADR template](docs/adr/TEMPLATE.md)

## Visual

- [System overview](docs/architecture/system-overview.html)
- [DB schema](docs/architecture/db-schema.html)
- [AI modules](docs/architecture/ai-modules.html)
- [API endpoints](docs/architecture/api-endpoints.html)
- [Next.js screens](docs/architecture/nextjs-screens.html)
- [React Native screens](docs/architecture/rn-screens.html)

## Agentes

- [AGENTS.md](AGENTS.md) - orientacao para Codex e outros agentes.
- [CLAUDE.md](CLAUDE.md) - orientacao para Claude Code.

## Regra de manutencao

- Produto muda: atualize `docs/PRD.md`.
- Setup muda: atualize `docs/SETUP.md`.
- Ordem de construcao muda: atualize `docs/ROADMAP.md`.
- Decisao arquitetural muda: crie ou atualize um ADR.
- Diagrama muda: atualize o HTML em `docs/architecture/`.
- Instrucao para codegen muda: atualize `AGENTS.md` e, se aplicavel, `CLAUDE.md`.
