# ADR 0003 - Auth, RBAC e dados

Status: aceito
Data: 2026-05-28
Indice: [ADR](../ADR.md)

## Contexto

A primeira versao produtiva precisa de apenas dois papeis: operador de estoque e admin. Mais papeis adicionariam complexidade de politica antes de haver evidencia de produto.

## Decisao

Usar Supabase Auth como provedor de identidade e aplicar dois papeis:

- `operator`: operacao de estoque, busca de produto, movimentacoes e alertas.
- `admin`: tudo do operador mais financeiro, relatorios, equipe e insights administrativos.

FastAPI valida JWTs e aplica RBAC por rota. Supabase RLS protege acesso direto aos dados.

## Consequencias

- Autorizacao permanece compreensivel.
- Testes podem verificar claramente 401, 403 e 200.
- Novos papeis exigem novo ADR ou atualizacao explicita deste ADR.
