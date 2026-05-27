# Schema Decisions — Sprint 1

## Estrutura de migrations

| Arquivo | Conteúdo |
|---------|----------|
| `20260527000001_initial_schema.sql` | Tabelas, view `estoque_atual`, índices, trigger `atualizado_em` |
| `20260527000002_rls_base.sql` | RLS em todas as tabelas + trigger de criação de perfil no signup |
| `20260527000003_seed.sql` | 10 produtos + movimentações (5 produtos com estoque abaixo do mínimo para demo de IA) |

## Decisões

**UUID como PK:** evita colisão em ambiente distribuído e não expõe volume de registros.

**`lotes` incluído no schema inicial:** sprint 3 depende desta tabela. Criar junto evita migration de ALTER TABLE depois.

**`estoque_atual` como VIEW simples:** Stocky é PME com volume baixo — view recalcula em tempo real sem necessidade de tabela materializada. Revisar se volume crescer.

**`estoque_atual` inclui dados do produto:** a view retorna `nome`, `sku`, `estoque_minimo` e `unidade` além de `quantidade_atual` para evitar JOIN extra no código da API e do agente de IA.

**RLS: operador lê tudo, admin escreve tudo:** simplificação para POC. Multitenancy (isolamento por empresa) está fora do escopo do POC.

**Trigger `handle_new_user`:** cria linha em `perfis` automaticamente no signup via Supabase Auth. Role sempre `operador` hardcoded — nunca lido do `raw_user_meta_data` (campo controlado pelo cliente, spoofable). Promoção para `admin` somente via dashboard ou endpoint com autenticação de admin existente.

**`perfis_update_own` com restrição de role:** policy impede que usuário altere o próprio `role` via UPDATE direto. O `WITH CHECK` compara o novo valor com o valor atual no banco.

## Como aplicar

### Opção A — Supabase Studio (SQL Editor)
Colar cada arquivo em ordem no SQL Editor do Studio.

### Opção B — CLI via SSH tunnel
```bash
# Terminal 1: abrir tunnel
ssh -L 5432:127.0.0.1:5432 <user>@<ip-vps>

# Terminal 2: aplicar
supabase db push --db-url "postgresql://postgres:<senha>@127.0.0.1:5432/postgres"
```

## Seed

10 produtos de mercearia com estoque inicial via `movimentacoes` (entrada).
Saídas configuradas para deixar 5 produtos abaixo do `estoque_minimo` — necessário para demonstrar o agente de recomendação de reposição (sprint 6).
