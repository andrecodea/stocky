-- ============================================================
-- Seed: dados falsos para desenvolvimento
-- Aplicar APÓS as migrations 1 e 2
-- ============================================================

-- Produtos
INSERT INTO produtos (id, nome, sku, descricao, preco_custo, preco_venda, unidade, estoque_minimo) VALUES
  ('11111111-0000-0000-0000-000000000001', 'Arroz Integral 1kg',    'ARR-INT-1KG', 'Arroz integral tipo 1',          3.50,  7.90, 'un', 20),
  ('11111111-0000-0000-0000-000000000002', 'Feijão Carioca 1kg',    'FEJ-CAR-1KG', 'Feijão carioca tipo 1',           4.20,  8.50, 'un', 15),
  ('11111111-0000-0000-0000-000000000003', 'Óleo de Soja 900ml',    'OLE-SOJ-900', 'Óleo de soja refinado',           4.80,  9.90, 'un', 10),
  ('11111111-0000-0000-0000-000000000004', 'Açúcar Cristal 1kg',    'ACU-CRI-1KG', 'Açúcar cristal standard',         2.90,  5.50, 'un', 25),
  ('11111111-0000-0000-0000-000000000005', 'Café Moído 500g',       'CAF-MOI-500', 'Café torrado e moído',            8.90, 18.90, 'un', 12),
  ('11111111-0000-0000-0000-000000000006', 'Leite Integral 1L',     'LEI-INT-001', 'Leite integral UHT',              3.20,  5.90, 'un', 30),
  ('11111111-0000-0000-0000-000000000007', 'Macarrão Espaguete 500g','MAC-ESP-500', 'Macarrão de sêmola',             2.10,  4.50, 'un', 20),
  ('11111111-0000-0000-0000-000000000008', 'Sal Refinado 1kg',      'SAL-REF-1KG', 'Sal refinado iodado',             1.20,  2.80, 'un', 15),
  ('11111111-0000-0000-0000-000000000009', 'Farinha de Trigo 1kg',  'FAR-TRI-1KG', 'Farinha de trigo tipo 1',         2.80,  5.90, 'un', 18),
  ('11111111-0000-0000-0000-000000000010', 'Molho de Tomate 340g',  'MOL-TOM-340', 'Molho de tomate tradicional',     1.80,  3.90, 'un',  8);

-- Movimentações de entrada (estoque inicial)
INSERT INTO movimentacoes (produto_id, tipo, quantidade, custo_unitario, observacao) VALUES
  ('11111111-0000-0000-0000-000000000001', 'entrada', 50,  3.50, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000002', 'entrada', 40,  4.20, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000003', 'entrada', 30,  4.80, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000004', 'entrada', 60,  2.90, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000005', 'entrada', 25,  8.90, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000006', 'entrada', 80,  3.20, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000007', 'entrada', 45,  2.10, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000008', 'entrada', 35,  1.20, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000009', 'entrada', 40,  2.80, 'Estoque inicial'),
  ('11111111-0000-0000-0000-000000000010', 'entrada', 20,  1.80, 'Estoque inicial');

-- Saídas para simular estoque baixo em alguns produtos
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao) VALUES
  ('11111111-0000-0000-0000-000000000001', 'saida', 44, 'Vendas período'),   -- restam 6  (mín 20) ⚠️
  ('11111111-0000-0000-0000-000000000002', 'saida', 37, 'Vendas período'),   -- restam 3  (mín 15) ⚠️
  ('11111111-0000-0000-0000-000000000003', 'saida', 22, 'Vendas período'),   -- restam 8  (mín 10) ⚠️
  ('11111111-0000-0000-0000-000000000005', 'saida',  8, 'Vendas período'),   -- restam 17 (mín 12) OK
  ('11111111-0000-0000-0000-000000000006', 'saida', 50, 'Vendas período'),   -- restam 30 (mín 30) ⚠️
  ('11111111-0000-0000-0000-000000000010', 'saida', 16, 'Vendas período');   -- restam 4  (mín  8) ⚠️
