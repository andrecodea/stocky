-- ============================================================
-- Migration 2: RLS + Auth trigger
-- ============================================================

-- Trigger: cria perfil automaticamente no signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.perfis (id, nome, role)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'nome', 'Usuário'),
    'operador'  -- sempre operador; promoção para admin somente via fluxo privilegiado
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- ============================================================
-- RLS: produtos
-- ============================================================
ALTER TABLE produtos ENABLE ROW LEVEL SECURITY;

-- Todos autenticados podem ler
CREATE POLICY "produtos_select" ON produtos
  FOR SELECT TO authenticated USING (true);

-- Somente admin pode escrever
CREATE POLICY "produtos_admin_write" ON produtos
  FOR ALL TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM perfis
      WHERE perfis.id = auth.uid() AND perfis.role = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM perfis
      WHERE perfis.id = auth.uid() AND perfis.role = 'admin'
    )
  );

-- ============================================================
-- RLS: movimentacoes
-- ============================================================
ALTER TABLE movimentacoes ENABLE ROW LEVEL SECURITY;

-- Operador vê as próprias; admin vê todas
CREATE POLICY "movimentacoes_select" ON movimentacoes
  FOR SELECT TO authenticated
  USING (
    usuario_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM perfis
      WHERE perfis.id = auth.uid() AND perfis.role = 'admin'
    )
  );

-- Autenticados podem registrar movimentação própria
CREATE POLICY "movimentacoes_insert" ON movimentacoes
  FOR INSERT TO authenticated
  WITH CHECK (usuario_id = auth.uid());

-- Somente admin pode editar/deletar
CREATE POLICY "movimentacoes_admin_write" ON movimentacoes
  FOR UPDATE TO authenticated
  USING (
    EXISTS (SELECT 1 FROM perfis WHERE perfis.id = auth.uid() AND perfis.role = 'admin')
  );

-- ============================================================
-- RLS: lotes
-- ============================================================
ALTER TABLE lotes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "lotes_select" ON lotes
  FOR SELECT TO authenticated USING (true);

CREATE POLICY "lotes_admin_write" ON lotes
  FOR ALL TO authenticated
  USING (
    EXISTS (SELECT 1 FROM perfis WHERE perfis.id = auth.uid() AND perfis.role = 'admin')
  )
  WITH CHECK (
    EXISTS (SELECT 1 FROM perfis WHERE perfis.id = auth.uid() AND perfis.role = 'admin')
  );

-- ============================================================
-- RLS: perfis
-- ============================================================
ALTER TABLE perfis ENABLE ROW LEVEL SECURITY;

-- Cada usuário vê só o próprio perfil; admin vê todos
CREATE POLICY "perfis_select" ON perfis
  FOR SELECT TO authenticated
  USING (
    id = auth.uid()
    OR EXISTS (SELECT 1 FROM perfis p WHERE p.id = auth.uid() AND p.role = 'admin')
  );

-- Usuário edita só o próprio perfil, mas não pode alterar o próprio role
CREATE POLICY "perfis_update_own" ON perfis
  FOR UPDATE TO authenticated
  USING (id = auth.uid())
  WITH CHECK (
    id = auth.uid()
    AND role = (SELECT role FROM perfis WHERE id = auth.uid())
  );
