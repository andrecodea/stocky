# Task 3b: Configurar Supabase Storage para fotos de produtos

**Estimativa:** ~25 min  
**Dev:** Backend Dev 2  
**O que é e por que existe:**  
Fotos de produtos ficam no Supabase Storage (não no banco). O bucket precisa de políticas de acesso para que o backend faça upload e o app mobile leia as URLs.

**Arquivos:**
- Executar via Supabase CLI ou Dashboard (Storage não tem migration SQL padrão)

---

### Documentação
- [Supabase Storage](https://supabase.com/docs/guides/storage) — buckets e políticas
- [Storage Policies](https://supabase.com/docs/guides/storage/security/access-control)

---

### O que você precisa fazer

> **Passo 1 — Criar bucket `product-images`:**

```sql
-- TODO: via SQL Editor do Supabase:
-- INSERT INTO storage.buckets (id, name, public) VALUES ('product-images', 'product-images', false);
-- Bucket privado: acesso só por URLs assinadas
```

<details>
<summary>💡 Solução — Passo 1</summary>

```sql
INSERT INTO storage.buckets (id, name, public)
VALUES ('product-images', 'product-images', false)
ON CONFLICT (id) DO NOTHING;
```

</details>

---

> **Passo 2 — Criar políticas de Storage:**

```sql
-- TODO: SELECT (leitura): authenticated pode ler qualquer arquivo do bucket
-- TODO: INSERT: authenticated pode fazer upload
-- TODO: DELETE: somente admin (usar is_admin())
```

<details>
<summary>💡 Solução — Passo 2</summary>

```sql
CREATE POLICY "storage_select" ON storage.objects
  FOR SELECT TO authenticated
  USING (bucket_id = 'product-images');

CREATE POLICY "storage_insert" ON storage.objects
  FOR INSERT TO authenticated
  WITH CHECK (bucket_id = 'product-images');

CREATE POLICY "storage_delete" ON storage.objects
  FOR DELETE TO authenticated
  USING (bucket_id = 'product-images' AND is_admin());
```

</details>

---

### Checkboxes

- [ ] **T3b.1:** Bucket `product-images` aparece no Supabase Dashboard → Storage
- [ ] **T3b.2:** Upload de imagem de teste via Dashboard funciona sem erro
- [ ] **T3b.3:** URL assinada gerada via Dashboard abre a imagem no browser

---

### Resumo
> *Preencher após concluir a task.*
