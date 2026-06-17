from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

from fastapi import HTTPException

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("SUPABASE_URL", "http://localhost:54321")
os.environ.setdefault("SUPABASE_ANON_KEY", "anon")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "service")


class _FakeAuthUser:
    def __init__(self, user_id: str):
        self.id = user_id


class _FakeAuthResponse:
    def __init__(self, user_id: str | None):
        self.user = _FakeAuthUser(user_id) if user_id else None


class _FakeAuth:
    def __init__(self, user_id: str | None = "user-1", error: Exception | None = None):
        self.user_id = user_id
        self.error = error
        self.tokens: list[str] = []

    def get_user(self, token: str):
        self.tokens.append(token)
        if self.error:
            raise self.error
        return _FakeAuthResponse(self.user_id)


class _FakeAnonClient:
    def __init__(self, auth: _FakeAuth):
        self.auth = auth


class _FakeResponse:
    def __init__(self, data):
        self.data = data


class _FakeProfileQuery:
    def __init__(self, rows):
        self.rows = rows
        self.filters: list[tuple[str, str]] = []

    def select(self, *_args, **_kwargs):
        return self

    def eq(self, key: str, value: str):
        self.filters.append((key, value))
        return self

    def limit(self, *_args, **_kwargs):
        return self

    def execute(self):
        return _FakeResponse(self.rows)


class _FakeAdminClient:
    def __init__(self, rows):
        self.rows = rows
        self.table_name: str | None = None
        self.query = _FakeProfileQuery(rows)

    def table(self, name: str):
        self.table_name = name
        return self.query


class AuthDependencyTest(unittest.IsolatedAsyncioTestCase):
    async def test_current_user_rejects_missing_authorization_header_with_401(self):
        from api import deps

        with self.assertRaises(HTTPException) as ctx:
            await deps.get_current_user(None)  # type: ignore[arg-type]

        self.assertEqual(ctx.exception.status_code, 401)
        self.assertEqual(ctx.exception.detail, "Token invalido")

    async def test_current_user_delegates_token_validation_to_supabase_auth(self):
        from api import deps

        auth = _FakeAuth(user_id="user-1")
        admin = _FakeAdminClient(
            [{"id": "user-1", "role": "admin", "nome": "Admin Teste"}]
        )
        original_anon = deps.get_anon_client
        original_admin = deps.get_admin_client
        deps.get_anon_client = lambda: _FakeAnonClient(auth)
        deps.get_admin_client = lambda: admin
        try:
            user = await deps.get_current_user("Bearer access-token")
        finally:
            deps.get_anon_client = original_anon
            deps.get_admin_client = original_admin

        self.assertEqual(auth.tokens, ["access-token"])
        self.assertEqual(admin.table_name, "perfis")
        self.assertIn(("id", "user-1"), admin.query.filters)
        self.assertEqual(user.id, "user-1")
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.nome, "Admin Teste")

    async def test_current_user_rejects_tokens_supabase_auth_cannot_validate(self):
        from api import deps

        original_anon = deps.get_anon_client
        deps.get_anon_client = lambda: _FakeAnonClient(_FakeAuth(error=RuntimeError("bad token")))
        try:
            with self.assertRaises(HTTPException) as ctx:
                await deps.get_current_user("Bearer invalid")
        finally:
            deps.get_anon_client = original_anon

        self.assertEqual(ctx.exception.status_code, 401)
        self.assertEqual(ctx.exception.detail, "Token invalido")

    async def test_require_role_rejects_disallowed_roles_with_403(self):
        from api import deps

        check_admin = deps.require_role("admin")

        with self.assertRaises(HTTPException) as ctx:
            await check_admin(deps.AuthenticatedUser(id="user-1", role="operador", nome="Operador"))

        self.assertEqual(ctx.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
