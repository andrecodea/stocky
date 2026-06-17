-- ============================================================
-- Migration: AI logs
-- Structured persisted insights consumed by mobile/web clients.
-- ============================================================

CREATE TABLE IF NOT EXISTS ai_logs (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tipo        text NOT NULL CHECK (
    tipo IN ('estoque', 'financeiro', 'comercial', 'logistica', 'supply_chain', 'geral')
  ),
  titulo      text NOT NULL,
  resumo      text NOT NULL,
  conteudo    jsonb NOT NULL DEFAULT '{}'::jsonb,
  fontes      jsonb NOT NULL DEFAULT '[]'::jsonb,
  severidade  text NOT NULL DEFAULT 'info' CHECK (
    severidade IN ('info', 'atencao', 'critica')
  ),
  audiencia   text NOT NULL DEFAULT 'ambos' CHECK (
    audiencia IN ('operador', 'admin', 'ambos')
  ),
  agente      text,
  criado_em   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ai_logs_criado_em ON ai_logs(criado_em DESC);
CREATE INDEX IF NOT EXISTS idx_ai_logs_tipo ON ai_logs(tipo);
CREATE INDEX IF NOT EXISTS idx_ai_logs_audiencia ON ai_logs(audiencia);

ALTER TABLE ai_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "ai_logs_operator_select" ON ai_logs
  FOR SELECT TO authenticated
  USING (
    audiencia IN ('operador', 'ambos')
    OR EXISTS (
      SELECT 1 FROM perfis
      WHERE perfis.id = auth.uid() AND perfis.role = 'admin'
    )
  );
