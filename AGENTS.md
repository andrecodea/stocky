# AGENTS.md

Orientacao para Codex, Claude Code e outros agentes de codegen neste repositorio.

## Leia primeiro

1. `INDEX.md`
2. `README.md`
3. `docs/SETUP.md`
4. `docs/PRD.md`
5. `docs/ROADMAP.md`
6. `docs/ADR.md`
7. `docs/adr/*.md` quando a decisao especifica for relevante
8. Diagrama relevante em `docs/architecture/`

Nao recrie documentacao por task a menos que o usuario peca explicitamente. O projeto agora usa documentacao enxuta: PRD, roadmap, ADRs e diagramas.

## Projeto

Stocky e um produto de gerenciamento inteligente de estoque para pequenos e medios negocios.

Superficies principais:

- App React Native para operadores.
- Dashboard Next.js para admins.
- Backend FastAPI para regras de negocio, auth, RBAC, webhooks e chat.
- Supabase para Postgres, Auth, Storage, Realtime, RLS, pgvector e pg_cron.
- OpenRouter para acesso a LLMs e modelos multimodais.

## Comandos

```bash
uv sync
uv run main.py
```

Se adicionar comandos especificos de app, atualize `README.md` e `docs/ROADMAP.md` no mesmo change.

## Regras de implementacao

- Amarre a mudanca a um marco do roadmap.
- Prefira fatias verticais pequenas com validacao clara.
- Nao adicione framework novo sem registrar ADR.
- Nao coloque secrets em docs ou commits.
- Preserve RBAC: `operator` opera estoque; `admin` acessa estoque, financeiro, equipe e relatorios.
- Para IA, persista saidas estruturadas antes de ligar UI. A UI deve consumir insights armazenados, nao esperar agentes longos.

## Regras de documentacao

- `docs/PRD.md` governa escopo de produto.
- `docs/SETUP.md` governa ambiente local e validacao.
- `docs/ROADMAP.md` governa ordem de execucao e criterios de aceite.
- `docs/ADR.md` e o indice de decisoes duraveis.
- `docs/adr/` contem os registros individuais de decisao.
- `docs/architecture/*.html` governa referencias visuais.
- `INDEX.md` centraliza a navegacao entre todos esses documentos.
- Evite tabelas Markdown com aliases wiki do Obsidian, porque `|` quebra a renderizacao da tabela.
