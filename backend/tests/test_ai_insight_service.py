from __future__ import annotations

import sys
import unittest
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("SUPABASE_URL", "http://localhost:54321")
os.environ.setdefault("SUPABASE_ANON_KEY", "anon")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "service")


class _FakeResponse:
    def __init__(self, data):
        self.data = data


class _FakeQuery:
    def __init__(self, data):
        self.data = data
        self.filters: list[tuple[str, object]] = []
        self.inserted = None

    def select(self, *_args, **_kwargs):
        return self

    def insert(self, payload):
        self.inserted = payload
        self.data = [{**payload, "id": "log-1", "criado_em": "2026-06-17T12:00:00Z"}]
        return self

    def eq(self, key, value):
        self.filters.append((key, value))
        return self

    def in_(self, key, value):
        self.filters.append((key, tuple(value)))
        return self

    def order(self, *_args, **_kwargs):
        return self

    def limit(self, *_args, **_kwargs):
        return self

    def execute(self):
        return _FakeResponse(self.data)


class _FakeClient:
    def __init__(self, data):
        self.query = _FakeQuery(data)

    def table(self, name):
        self.table_name = name
        return self.query


class AiInsightServiceTest(unittest.TestCase):
    def test_operator_only_reads_operator_or_shared_insights(self):
        from services import ai_insight_service

        client = _FakeClient(
            [
                {
                    "id": "log-1",
                    "tipo": "estoque",
                    "titulo": "Reposição",
                    "resumo": "Arroz abaixo do mínimo.",
                    "conteudo": {},
                    "fontes": [],
                    "severidade": "atencao",
                    "audiencia": "operador",
                    "agente": "estoque",
                    "criado_em": "2026-06-17T12:00:00Z",
                }
            ]
        )

        result = ai_insight_service.listar_insights(role="operador", client=client)

        self.assertEqual(client.table_name, "ai_logs")
        self.assertIn(("audiencia", ("operador", "ambos")), client.query.filters)
        self.assertEqual(result[0].titulo, "Reposição")

    def test_admin_can_filter_by_insight_type_without_audience_filter(self):
        from services import ai_insight_service

        client = _FakeClient([])

        ai_insight_service.listar_insights(role="admin", tipo="financeiro", client=client)

        self.assertIn(("tipo", "financeiro"), client.query.filters)
        self.assertNotIn(("audiencia", ("operador", "ambos")), client.query.filters)

    def test_create_ai_log_persists_structured_payload(self):
        from schemas.ai import AiLogCreate
        from services import ai_insight_service

        client = _FakeClient([])

        created = ai_insight_service.criar_ai_log(
            AiLogCreate(
                tipo="estoque",
                titulo="Reposição crítica",
                resumo="Arroz precisa de reposição.",
                conteudo={"produto_id": "p1"},
                fontes=[{"tipo": "estoque", "id": "p1"}],
                severidade="critica",
                audiencia="ambos",
                agente="estoque",
            ),
            client=client,
        )

        self.assertEqual(client.table_name, "ai_logs")
        self.assertEqual(client.query.inserted["tipo"], "estoque")
        self.assertEqual(client.query.inserted["conteudo"], {"produto_id": "p1"})
        self.assertEqual(created.id, "log-1")


if __name__ == "__main__":
    unittest.main()
