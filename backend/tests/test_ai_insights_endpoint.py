from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("SUPABASE_URL", "http://localhost:54321")
os.environ.setdefault("SUPABASE_ANON_KEY", "anon")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "service")


class AiInsightsEndpointTest(unittest.TestCase):
    def tearDown(self):
        from api.app import app

        app.dependency_overrides.clear()

    def test_get_ai_insights_uses_authenticated_role(self):
        from fastapi.testclient import TestClient

        from api.app import app
        from api.deps import AuthenticatedUser
        from api.routers import ai
        from schemas.ai import AiLogRead

        calls = []

        async def fake_user():
            return AuthenticatedUser(id="user-1", role="operador", nome="Operador")

        def fake_listar_insights(*, role, tipo=None, limit=50):
            calls.append({"role": role, "tipo": tipo, "limit": limit})
            return [
                AiLogRead(
                    id="log-1",
                    tipo="estoque",
                    titulo="Reposicao",
                    resumo="Arroz abaixo do minimo.",
                    conteudo={},
                    fontes=[],
                    severidade="atencao",
                    audiencia="operador",
                    agente="estoque",
                )
            ]

        app.dependency_overrides[ai.require_any] = fake_user
        original = ai.ai_insight_service.listar_insights
        ai.ai_insight_service.listar_insights = fake_listar_insights
        try:
            response = TestClient(app).get("/ai/insights?tipo=estoque&limit=10")
        finally:
            ai.ai_insight_service.listar_insights = original

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["titulo"], "Reposicao")
        self.assertEqual(calls, [{"role": "operador", "tipo": "estoque", "limit": 10}])

    def test_post_ai_insights_persists_admin_payload(self):
        from fastapi.testclient import TestClient

        from api.app import app
        from api.deps import AuthenticatedUser
        from api.routers import ai
        from schemas.ai import AiLogRead

        calls = []

        async def fake_admin():
            return AuthenticatedUser(id="admin-1", role="admin", nome="Admin")

        def fake_criar_ai_log(payload):
            calls.append(payload)
            return AiLogRead(
                id="log-2",
                tipo=payload.tipo,
                titulo=payload.titulo,
                resumo=payload.resumo,
                conteudo=payload.conteudo,
                fontes=payload.fontes,
                severidade=payload.severidade,
                audiencia=payload.audiencia,
                agente=payload.agente,
            )

        app.dependency_overrides[ai.require_admin] = fake_admin
        original = ai.ai_insight_service.criar_ai_log
        ai.ai_insight_service.criar_ai_log = fake_criar_ai_log
        try:
            response = TestClient(app).post(
                "/ai/insights",
                json={
                    "tipo": "financeiro",
                    "titulo": "Margem em queda",
                    "resumo": "Margem caiu 4pp na semana.",
                    "conteudo": {"janela": "7d"},
                    "fontes": [{"tipo": "financeiro", "id": "resumo"}],
                    "severidade": "atencao",
                    "audiencia": "admin",
                    "agente": "financeiro",
                },
            )
        finally:
            ai.ai_insight_service.criar_ai_log = original

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], "log-2")
        self.assertEqual(calls[0].tipo, "financeiro")


if __name__ == "__main__":
    unittest.main()
