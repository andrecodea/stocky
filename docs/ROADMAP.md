# Stocky — Roadmap

> Atualizado: 2026-05-28 · Cada marco é executável por humano ou codegen sem arquivos de task separados.

---

## Visão geral

| # | Marco | Status |
|---|-------|--------|
| 1 | Contrato de banco | ✅ Done |
| 2 | Backend API | 🔄 In Progress |
| 3 | Camada de IA | 🔄 In Progress |
| 4 | Web admin | ⬜ Not Started |
| 5 | App mobile | 🔄 In Progress |
| 6 | Deploy | ⬜ Not Started |

> **Foco agora:** Marcos 2, 3 e 5. O mobile avanca em estoque, financeiro admin e IA com fallback local explicito; scanner/camera ficam fora do MVP atual.

---

## Marco 1 — Contrato de banco ✅

**Objetivo:** Definir o schema Supabase necessário para produção.

**Entregáveis:**
- [x] Tabelas de negócio — produtos, estoque, movimentações, financeiro, vendas, fornecedores, perfis
- [x] Tabelas de IA — logs estruturados e embeddings
- [x] Políticas RLS para `operator` e `admin`
- [x] RPC pgvector para busca por similaridade
- [x] Plano de webhooks e pg_cron documentado

**Critérios de aceite:**
- [x] Migrations aplicam sem erro
- [x] Caminhos de acesso de `operator` e `admin` são testáveis
- [x] `buscar_embeddings` ou RPC equivalente retorna chunks ranqueados

---

## Marco 2 — Backend API 🔄

**Objetivo:** Expor o contrato produtivo em FastAPI.

**Entregáveis:**
- [x] Validação de token do Supabase Auth
- [x] Dependências de RBAC
- [ ] Endpoints de produtos e movimentações
- [ ] Endpoint de resumo financeiro
- [x] Endpoint de insights de IA
- [ ] Receiver de webhook Supabase
- [ ] Endpoint de chat RAG com SSE

**Critérios de aceite:**
- [x] 401 sem token
- [x] 403 quando o papel não tem permissão
- [ ] Swagger mostra todos os endpoints produtivos
- [ ] Criação de movimentação atualiza estoque e retorna quantidade resultante

---

## Marco 3 — Camada de IA 🔄

**Objetivo:** Armazenar saídas úteis de IA e suportar chat fundamentado.

**Entregáveis:**
- [ ] Agentes ambientes — estoque, comercial, financeiro, logística, supply chain
- [ ] Saídas estruturadas gravadas em logs de IA
- [ ] Pipeline de embeddings — produtos, estoque, financeiro, relatórios de IA
- [ ] Chat RAG com contexto recuperado e comportamento de fallback

**Critérios de aceite:**
- [ ] Trigger manual grava pelo menos um log válido por tipo de agente
- [ ] Chat retorna resposta em streaming com fontes quando retrieval encontra contexto
- [ ] Chat recusa ou qualifica respostas quando falta contexto

---

## Marco 4 — Web admin ⬜

**Objetivo:** Entregar dashboard admin em Next.js.

**Entregáveis:**
- [ ] Login e sessão
- [ ] Telas — Dashboard, Estoque, Financeiro, Comercial, Logística, Supply Chain, Configurações
- [ ] Cliente de API com estados loading, vazio e erro
- [ ] Copilot flutuante usando SSE

**Critérios de aceite:**
- [ ] Admin navega por todas as telas
- [ ] Operador recebe negativa amigável em telas admin-only
- [ ] Copilot transmite resposta e renderiza fontes

---

## Marco 5 — App mobile 🔄

**Objetivo:** Entregar fluxo mobile de estoque, financeiro admin e IA operacional em React Native.

**Entregáveis:**
- [x] Shell Expo
- [x] Tabs — Home, Estoque, Financeiro, IA, Movimentações, Alertas
- [x] Fluxo de movimentação com busca de produto e confirmação de quantidade
- [x] Resumo financeiro admin via `/financeiro/resumo`
- [x] Tela de IA preparada para `/ai/insights` com fallback local de estoque
- [ ] Entrada para Copilot/chat RAG

**Comandos:**

```bash
cd mobile
npm install
npm run start
npm test
```

**Critérios de aceite:**
- [ ] Operador cria uma movimentação pelo mobile
- [ ] Tela de estoque reflete a quantidade atualizada
- [ ] Admin visualiza resumo financeiro no mobile
- [x] Tela de IA mostra logs armazenados quando `/ai/insights` existir
- [x] Tela de IA mostra fallback local explicito enquanto `/ai/insights` nao existir

---

## Marco 6 — Deploy ⬜

**Objetivo:** Deixar o sistema acessível e observável em infraestrutura próxima de produção.

**Entregáveis:**
- [ ] Serviço FastAPI em Docker
- [ ] Deploy no Coolify
- [ ] Documentação de variáveis de ambiente
- [ ] Health check HTTPS
- [ ] Webhook Supabase configurado

**Critérios de aceite:**
- [ ] `/health` público retorna OK por HTTPS
- [ ] Endpoint protegido rejeita request sem token
- [ ] Webhook Supabase chega ao backend e cria ou enfileira trabalho de IA

---

## Referências

- [PRD](PRD.md)
- [ADR](ADR.md)
