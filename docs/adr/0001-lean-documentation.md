# ADR 0001 - Modelo enxuto de documentacao

Status: aceito
Data: 2026-05-28
Indice: [ADR](../ADR.md)

## Contexto

O projeto tinha uma cascata Obsidian com indice, MOCs, sprints e arquivos individuais de task. Essa estrutura ajudou no planejamento, mas criou manutencao demais e aumentou o risco de links quebrados e escopo duplicado.

## Decisao

Usar um modelo enxuto:

- `README.md` para orientacao e comandos.
- `docs/PRD.md` para escopo de produto.
- `docs/ROADMAP.md` para ordem de implementacao e criterios de aceite.
- `docs/adr/*.md` para decisoes duraveis.
- `docs/architecture/*.html` para diagramas visuais.
- `AGENTS.md` e `CLAUDE.md` para orientacao de codegen.

## Consequencias

- Menos drift documental.
- Onboarding mais direto para humanos e agentes.
- Tasks deixam de existir como arquivos locais e passam a viver em marcos do roadmap ou em issues externas.
- Quebras detalhadas de task so devem voltar quando o usuario pedir explicitamente.
