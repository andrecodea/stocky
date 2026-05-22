# Task 3a: Índices de performance

**Estimativa:** ~30 min  
**Dev:** Backend Dev 2  
**O que é e por que existe:**  
Queries frequentes (movimentações por produto, produtos por SKU) precisam de índices para não fazer full table scan em volumes maiores.

**Arquivos:**
- Criar: `supabase/migrations/<timestamp>_indices.sql`

---

### O que você precisa fazer

> **Passo 1 — Criar índices nas colunas de FK e filtros frequentes:**

```sql
-- TODO: índice em movimentacoes.produto_id (filtro mais frequente)
-- TODO: índice em movimentacoes.criado_em DESC (queries de histórico)
-- TODO: índice em produtos.sku (busca por código)
-- TODO: índice em lotes.produto_id
-- TODO: índice em lotes.data_validade (alertas de vencimento)
```

<details>
<summary>💡 Solução — Passo 1</summary>

```sql
CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto_id ON movimentacoes(produto_id);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_criado_em ON movimentacoes(criado_em DESC);
CREATE INDEX IF NOT EXISTS idx_produtos_sku ON produtos(sku) WHERE sku IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_lotes_produto_id ON lotes(produto_id);
CREATE INDEX IF NOT EXISTS idx_lotes_data_validade ON lotes(data_validade) WHERE data_validade IS NOT NULL;
```

</details>

---

### Checkboxes

- [ ] **T3a.1:** `supabase db push` aplica sem erro
- [ ] **T3a.2:** Índices visíveis no Supabase Dashboard → Database → Indexes

---

### Resumo
> *Preencher após concluir a task.*
