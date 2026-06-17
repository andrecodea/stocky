# ADR 0006 - Arquitetura do backend API

Status: aceito
Data: 2026-06-09
Indice: [ADR](../ADR.md)

## Contexto

O Marco 2 do roadmap exige um backend FastAPI produtivo com autenticacao JWT, RBAC por rota e CRUD completo sobre todas as entidades do schema Supabase. Ate agora, o backend tem apenas endpoints `/ping` e `/health`, um service layer de produtos sem rotas, e nenhum middleware de auth.

Decisoes necessarias:

- como validar JWTs do Supabase Auth no FastAPI;
- como aplicar RBAC (`operador`/`admin`) sem acoplar logica a cada handler;
- como organizar routers, services e schemas de forma que novos dominios (IA, webhooks) se encaixem sem refatoracao;
- como o backend acessa o banco sem depender de RLS para autorizacao primaria.

## Decisao

### Autenticacao

Validar tokens emitidos pelo Supabase Auth chamando `get_anon_client().auth.get_user(token)` no backend. Isso delega a verificacao de assinatura, expiracao e algoritmo ao Supabase Auth, evitando acoplamento do FastAPI ao algoritmo local do JWT.

O fluxo:

1. Cliente envia `Authorization: Bearer <token>`.
2. Dependency `get_current_user()` chama Supabase Auth com o token recebido e extrai o `user.id` validado.
3. Consulta a tabela `perfis` via admin client para obter `role` e `nome`.
4. Retorna `AuthenticatedUser(id, role, nome)` injetado no handler.
5. Token invalido, expirado ou sem usuario retorna 401. Perfil nao encontrado retorna 401.

### RBAC

Usar dependency factory `require_role(*roles)` que recebe os papeis permitidos e retorna 403 se o usuario autenticado nao pertence a nenhum deles.

Atalhos:

- `require_admin` = `require_role("admin")`
- `require_any` = `require_role("operador", "admin")`

Esses atalhos sao usados via `Depends()` nos parametros dos handlers.

### Clientes Supabase

Expor dois clientes singleton:

- `get_anon_client()`: usa `supabase_anon_key`. Usado para operacoes de auth (login/signup) que dependem do fluxo nativo do Supabase Auth.
- `get_admin_client()`: usa `supabase_service_role_key`. Usado para todas as operacoes de dados no backend. A autorizacao ja foi validada nas dependencies do FastAPI, entao o RLS e uma camada secundaria de defesa, nao primaria.

### Camadas

```
Router (HTTP) -> Dependency (Auth/RBAC) -> Service (logica) -> Supabase client (dados)
```

- **Routers** (`api/routers/*.py`): recebem requests, validam schemas Pydantic, delegam para services.
- **Dependencies** (`api/deps.py`): autenticacao e autorizacao injetaveis.
- **Services** (`services/*.py`): logica de negocio, queries ao Supabase, transformacoes.
- **Schemas** (`schemas/*.py`): modelos Pydantic separados por dominio.

### Estrutura de routers

Cada dominio tem seu router em `api/routers/`:

- `auth.py` — login e signup (proxy Supabase Auth)
- `produtos.py` — CRUD de produtos
- `estoque.py` — view de estoque atual e alertas
- `movimentacoes.py` — CRUD de movimentacoes
- `lotes.py` — CRUD de lotes
- `perfis.py` — leitura e edicao de perfis
- `financeiro.py` — resumo financeiro (admin-only)

### Endpoints de auth

O backend faz proxy das chamadas de login e signup ao Supabase Auth. Isso evita que o frontend precise conhecer a URL direta do Supabase e permite adicionar logica futura (rate limiting, audit log) no backend.

### Tratamento de erros

Excecoes de negocio (`NotFoundError`, `ForbiddenError`, `ConflictError`) sao definidas em `api/exceptions.py` e mapeadas a HTTP status codes via exception handlers globais no FastAPI.

## Consequencias

- Todo endpoint protegido depende de `get_current_user` ou `require_role`, tornando impossivel esquecer auth ao criar nova rota.
- O backend usa `service_role_key` para dados, o que exige cuidado: qualquer bug de autorizacao nas dependencies expoe dados sem protecao de RLS. O RLS do Supabase ainda protege acessos diretos ao banco fora do backend.
- Adicionar novos dominios (webhooks, chat RAG) significa criar novos routers e services sem tocar na infraestrutura de auth.
- `SUPABASE_JWT_SECRET` nao e necessario para a validacao de usuario no FastAPI; o backend depende de `SUPABASE_URL`, `SUPABASE_ANON_KEY` e `SUPABASE_SERVICE_ROLE_KEY`.

## Revisao

Revisar esta decisao quando:

- o projeto precisar de refresh token rotation gerenciado pelo backend;
- o numero de papeis crescer alem de `operador` e `admin`;
- o backend precisar de auth machine-to-machine (API keys) para integracao externa;
- o fluxo de auth migrar para fora do Supabase.
