-- ============================================================
-- Migration 1: Schema inicial
-- Tabelas: produtos, movimentacoes, perfis
-- ============================================================

-- Tipos ENUM
CREATE TYPE tipo_movimentacao AS ENUM ('entrada', 'saida', 'ajuste');
CREATE TYPE role_usuario AS ENUM ('operador', 'admin');

-- Produtos
CREATE TABLE IF NOT EXISTS produtos (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nome           text NOT NULL,
  sku            text UNIQUE,
  descricao      text,
  preco_custo    numeric(10,2) NOT NULL DEFAULT 0,
  preco_venda    numeric(10,2) NOT NULL DEFAULT 0,
  unidade        text NOT NULL DEFAULT 'un',
  estoque_minimo integer NOT NULL DEFAULT 0,
  foto_url       text,
  criado_em      timestamptz NOT NULL DEFAULT now(),
  atualizado_em  timestamptz NOT NULL DEFAULT now()
);

-- Lotes
CREATE TABLE IF NOT EXISTS lotes (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  produto_id     uuid NOT NULL REFERENCES produtos(id) ON DELETE RESTRICT,
  numero_lote    text,
  data_validade  date,
  fornecedor     text,
  custo_unitario numeric(10,2),
  criado_em      timestamptz NOT NULL DEFAULT now()
);

-- Movimentações
CREATE TABLE IF NOT EXISTS movimentacoes (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  produto_id     uuid NOT NULL REFERENCES produtos(id) ON DELETE RESTRICT,
  lote_id        uuid REFERENCES lotes(id),
  tipo           tipo_movimentacao NOT NULL,
  quantidade     integer NOT NULL,
  custo_unitario numeric(10,2),
  observacao     text,
  usuario_id     uuid REFERENCES auth.users(id),
  criado_em      timestamptz NOT NULL DEFAULT now()
);

-- Perfis (extensão do Supabase Auth)
CREATE TABLE IF NOT EXISTS perfis (
  id        uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nome      text NOT NULL,
  role      role_usuario NOT NULL DEFAULT 'operador',
  criado_em timestamptz NOT NULL DEFAULT now()
);

-- View: estoque atual agregado por produto
CREATE OR REPLACE VIEW estoque_atual AS
SELECT
  p.id AS produto_id,
  p.nome,
  p.sku,
  p.estoque_minimo,
  p.unidade,
  COALESCE(SUM(
    CASE
      WHEN m.tipo = 'entrada' THEN m.quantidade
      WHEN m.tipo = 'saida'   THEN -m.quantidade
      ELSE 0
    END
  ), 0) AS quantidade_atual
FROM produtos p
LEFT JOIN movimentacoes m ON m.produto_id = p.id
GROUP BY p.id, p.nome, p.sku, p.estoque_minimo, p.unidade;

-- Índices de performance
CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto_id ON movimentacoes(produto_id);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_criado_em  ON movimentacoes(criado_em DESC);
CREATE INDEX IF NOT EXISTS idx_produtos_sku             ON produtos(sku) WHERE sku IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_lotes_produto_id         ON lotes(produto_id);
CREATE INDEX IF NOT EXISTS idx_lotes_data_validade      ON lotes(data_validade) WHERE data_validade IS NOT NULL;

-- Trigger: atualiza atualizado_em em produtos automaticamente
CREATE OR REPLACE FUNCTION set_atualizado_em()
RETURNS trigger AS $$
BEGIN
  NEW.atualizado_em = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_produtos_atualizado_em
  BEFORE UPDATE ON produtos
  FOR EACH ROW EXECUTE FUNCTION set_atualizado_em();
