# Stocky Setup

Status: ativo
Atualizado: 2026-05-28

Guia para rodar e desenvolver o Stocky localmente.

## Pre-requisitos

- Python 3.13
- `uv`
- Supabase CLI, quando for trabalhar em migrations ou banco local/remoto
- Node.js, quando os apps Next.js ou React Native existirem no workspace
- Docker, quando for validar deploy local ou containers

## Primeiro setup

```bash
uv sync
```

Crie o `.env` a partir de `.env.example` e preencha os valores necessarios.

```bash
cp .env.example .env
```

Variaveis esperadas:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `OPENROUTER_API_KEY`
- `TAVILY_API_KEY`
- `WEBHOOK_SECRET`
- `EXPO_PUBLIC_STOCKY_API_URL`

`SUPABASE_JWT_SECRET` e opcional e fica apenas para compatibilidade local; o backend valida o bearer token com Supabase Auth.

Se estiver usando `supabase status -o env`, o backend tambem aceita os nomes emitidos pelo CLI:

- `API_URL` como alternativa a `SUPABASE_URL`
- `ANON_KEY` ou `PUBLISHABLE_KEY` como alternativa a `SUPABASE_ANON_KEY`
- `SERVICE_ROLE_KEY` ou `SECRET_KEY` como alternativa a `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET` como alternativa opcional a `SUPABASE_JWT_SECRET`

Nao commite valores reais de secrets.

## Rodar localmente

Backend:

```bash
uv run python backend/api/app.py
```

Mobile:

```bash
cd mobile
npm install
npm run start
```

No celular fisico, `EXPO_PUBLIC_STOCKY_API_URL` deve apontar para uma URL acessivel pelo aparelho. `127.0.0.1` funciona apenas para simulador/emulador ou para execucao local no mesmo host.

## Banco e migrations

Use Supabase para aplicar ou validar migrations.

Exemplo remoto:

```bash
supabase db push --db-url "postgresql://postgres:<senha>@db.<ref>.supabase.co:5432/postgres"
```

Antes de alterar schema:

- Confira o marco atual em `docs/ROADMAP.md`.
- Confira decisoes relacionadas em `docs/ADR.md`.
- Garanta que RLS e RBAC continuam alinhados aos papeis `operator` e `admin`.

## Validacao minima

Antes de encerrar uma mudanca, rode o comando mais especifico disponivel.

Base atual:

```bash
uv run python backend/api/app.py
```

Quando houver testes:

```bash
uv run pytest
cd mobile
npm test
```

Quando houver backend HTTP:

```bash
curl http://localhost:8000/health
```

## Troubleshooting

### `.env` incompleto

Sintoma: falha ao inicializar cliente Supabase, OpenRouter ou Tavily.

Correcao: compare `.env` com `.env.example` e preencha apenas valores locais.

### Supabase Auth/RLS falha

Sintoma: chamadas autenticadas retornam 401 ou 403 inesperado.

Correcao: valide se o token e aceito pelo Supabase Auth, se o perfil existe em `perfis` e se a role esperada esta correta.

### Webhook nao chega ao backend

Sintoma: evento Supabase nao cria log ou trabalho de IA.

Correcao: valide `WEBHOOK_SECRET`, URL publica, logs do backend e configuracao de webhook no Supabase.

### IA responde sem contexto

Sintoma: Copilot inventa valores ou responde de forma generica.

Correcao: verifique se embeddings existem, se a RPC de busca retorna chunks e se o prompt exige fallback quando nao houver contexto.

## Links relacionados

- [Index](../INDEX.md)
- [PRD](PRD.md)
- [Roadmap](ROADMAP.md)
- [ADR](ADR.md)
