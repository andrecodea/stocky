# Stocky PRD

Status: ativo
Owner: WedgeDynamics
Atualizado: 2026-05-28

## Resumo

Stocky ajuda pequenos e medios negocios a controlar estoque, entender impacto financeiro e receber recomendacoes de IA sobre reposicao, risco de ruptura e decisoes operacionais.

O produto tem duas superficies principais:

- App mobile para operacao diaria de estoque, resumo financeiro permitido por papel e insights de IA.
- Web admin para financeiro, relatorios, equipe e tomada de decisao.

## Usuarios

### Operador

Usa o app mobile para:

- Consultar estoque de produtos.
- Registrar movimentacoes.
- Revisar alertas e recomendacoes operacionais de IA.

### Admin

Usa o web admin para:

- Monitorar saude do estoque.
- Revisar KPIs financeiros.
- Gerenciar acessos da equipe.
- Inspecionar insights e relatorios de IA.
- Decidir reposicao, fornecedores e acoes contra perdas.

## Problema

Pequenos negocios frequentemente gerenciam estoque de forma reativa. Eles descobrem faltas tarde, nao conectam movimentacoes ao impacto de margem e nao tem uma forma simples de transformar dados operacionais em decisoes.

## Objetivos

- Manter estoque atual visivel e confiavel.
- Tornar movimentacoes rapidas no mobile.
- Expor alertas de estoque minimo e risco de ruptura.
- Conectar estoque a financeiro e margem.
- Registrar insights de IA como dados estruturados e auditaveis.
- Oferecer Copilot com respostas baseadas em dados reais.

## Fora de escopo

- Substituir um ERP completo.
- Billing multi-tenant complexo.
- Modulo avancado de RH.
- Acoplamento direto entre agentes em runtime.
- Execucao longa de IA dentro de requests sincronas do usuario.

## Requisitos funcionais

### Estoque

- Criar e editar produtos.
- Controlar estoque por produto e local.
- Registrar movimentacoes `in`, `out` e `adjustment`.
- Mostrar estoque atual e status de estoque minimo.
- Preservar historico com usuario, timestamp, quantidade e observacao.

### Mobile

- Autenticar operador.
- Exibir tabs Home, Estoque, Financeiro, IA, Movimentacoes e Alertas.
- Suportar busca textual de produtos.
- Exibir resumo financeiro quando o usuario autenticado for admin.
- Exibir insights de IA armazenados quando o backend estiver disponivel.
- Exibir fallback local explicito baseado no estoque quando o backend de IA ainda nao estiver disponivel.
- Nao incluir scanner, camera ou upload de foto no MVP mobile atual.

### Web admin

- Autenticar admin.
- Exibir KPIs de dashboard.
- Exibir tabela de estoque e filtros de status.
- Exibir resumo financeiro.
- Exibir feed de insights de IA.
- Gerenciar papeis basicos de usuarios.
- Expor Copilot flutuante.

### Financeiro

- Armazenar custo, receita, margem e perdas por produto/periodo.
- Mostrar resumo financeiro somente para admin.
- Conectar vendas e estoque aos relatorios de IA.

### IA

- Gerar logs estruturados de insights.
- Rodar agentes por webhooks ou agendamentos.
- Manter chat RAG separado dos agentes longos.
- Retornar respostas com fontes quando houver contexto.
- Evitar inventar valores quando nao houver contexto relevante.

### Backend API

Contrato produtivo que conecta todas as superficies (mobile, web, IA) ao banco.

#### Autenticacao

- Aceitar JWTs emitidos pelo Supabase Auth no header `Authorization: Bearer <token>`.
- Retornar 401 para requests sem token ou com token invalido/expirado.
- Expor endpoints de login (`POST /auth/login`) e signup (`POST /auth/signup`) como proxy ao Supabase Auth.
- Login retorna `access_token`, `refresh_token` e dados do perfil.
- Signup cria usuario e perfil `operador` automaticamente (via trigger no banco).

#### RBAC

- Dois papeis: `operador` e `admin` (armazenados na tabela `perfis`).
- Operador acessa: produtos (leitura), estoque, movimentacoes (leitura + criacao propria), lotes (leitura), perfil proprio.
- Admin acessa: tudo do operador mais escrita em produtos, lotes, perfis de outros, e resumo financeiro.
- Retornar 403 quando o papel nao tem permissao para o endpoint.

#### Endpoints de dados

- Produtos: `GET /produtos`, `GET /produtos/{id}`, `POST /produtos` (admin), `PATCH /produtos/{id}` (admin), `DELETE /produtos/{id}` (admin).
- Estoque: `GET /estoque` (posicao atual), `GET /estoque/alertas` (produtos abaixo do minimo).
- Movimentacoes: `GET /movimentacoes`, `GET /movimentacoes/{id}`, `POST /movimentacoes` (vincula usuario autenticado).
- Lotes: `GET /lotes`, `GET /lotes/{id}`, `POST /lotes` (admin), `PATCH /lotes/{id}` (admin), `DELETE /lotes/{id}` (admin).
- Perfis: `GET /perfis/me`, `GET /perfis` (admin), `PATCH /perfis/me`, `PATCH /perfis/{id}` (admin).
- Financeiro: `GET /financeiro/resumo` (admin).
- IA: `GET /ai/insights` (admin ve todos; operador ve apenas insights operacionais ou compartilhados), `POST /ai/insights` (admin/internal para persistir logs estruturados).

#### Respostas

- Erros de validacao retornam 422 com detalhes do campo.
- Recurso nao encontrado retorna 404.
- Conflito (ex: SKU duplicado) retorna 409.
- Todas as respostas seguem formato JSON consistente.
- Swagger UI acessivel em `/docs`.


## Papeis e acesso

- `operator`: estoque, movimentacoes, busca de produtos e alertas operacionais.
- `admin`: tudo do operador mais financeiro, relatorios, configuracoes de equipe e insights administrativos.

## Criterios de aceite

- Chamadas sem autenticacao retornam 401.
- Usuarios autenticados recebem respostas coerentes com seu papel.
- Operador nao acessa endpoints financeiros de admin.
- Movimentacao de estoque atualiza o estoque atual de forma consistente.
- Insights de IA sao armazenados antes de aparecerem na UI.
- Chat RAG retorna resposta fundamentada ou fallback explicito.

## Referencias visuais

- [System overview](architecture/system-overview.html)
- [AI modules](architecture/ai-modules.html)
- [API endpoints](architecture/api-endpoints.html)
- [Next.js screens](architecture/nextjs-screens.html)
- [React Native screens](architecture/rn-screens.html)

## Decisoes relacionadas

- [ADR](ADR.md)
