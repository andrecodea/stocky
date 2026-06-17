"""Seed local Supabase with Stocky test users and an AI insight.

This script uses Supabase HTTP APIs with the service role key from `.env`.
It is intended for local/dev setup only.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

OPERATOR_EMAIL = "operador@stocky.local"
ADMIN_EMAIL = "admin@stocky.local"
TEST_PASSWORD = "Stocky123!"


def required_env(name: str, *, aliases: tuple[str, ...] = ()) -> str:
    value = ""
    for candidate in (name, *aliases):
        value = os.getenv(candidate, "").strip()
        if value:
            break
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value.rstrip("/") if name in {"SUPABASE_URL", "API_URL"} else value


class SupabaseSeeder:
    def __init__(self) -> None:
        self.url = required_env("SUPABASE_URL", aliases=("API_URL",))
        self.service_key = required_env(
            "SUPABASE_SERVICE_ROLE_KEY", aliases=("SERVICE_ROLE_KEY", "SECRET_KEY")
        )
        self.headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
        }

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        response = httpx.request(
            method,
            f"{self.url}{path}",
            headers={**self.headers, **kwargs.pop("headers", {})},
            timeout=30,
            **kwargs,
        )
        return response

    def list_users(self) -> list[dict[str, Any]]:
        response = self.request("GET", "/auth/v1/admin/users")
        response.raise_for_status()
        payload = response.json()
        return payload.get("users", payload if isinstance(payload, list) else [])

    def find_user(self, email: str) -> dict[str, Any] | None:
        email = email.lower()
        for user in self.list_users():
            if str(user.get("email", "")).lower() == email:
                return user
        return None

    def ensure_user(self, *, email: str, nome: str, role: str) -> str:
        user = self.find_user(email)
        if user is None:
            response = self.request(
                "POST",
                "/auth/v1/admin/users",
                json={
                    "email": email,
                    "password": TEST_PASSWORD,
                    "email_confirm": True,
                    "user_metadata": {"nome": nome},
                },
            )
            response.raise_for_status()
            user = response.json()

        user_id = user["id"]

        profile_response = self.request(
            "PATCH",
            f"/rest/v1/perfis?id=eq.{user_id}",
            headers={"Prefer": "return=minimal"},
            json={"nome": nome, "role": role},
        )
        profile_response.raise_for_status()
        return user_id

    def ensure_ai_log(self) -> None:
        existing = self.request(
            "GET",
            "/rest/v1/ai_logs?titulo=eq.Reposicao%20critica%20de%20teste&select=id",
        )
        existing.raise_for_status()
        if existing.json():
            return

        response = self.request(
            "POST",
            "/rest/v1/ai_logs",
            headers={"Prefer": "return=minimal"},
            json={
                "tipo": "estoque",
                "titulo": "Reposicao critica de teste",
                "resumo": "Arroz Integral 1kg esta abaixo do minimo e precisa de reposicao.",
                "conteudo": {
                    "produto": "Arroz Integral 1kg",
                    "acao_recomendada": "Comprar 30 unidades",
                },
                "fontes": [{"tipo": "estoque", "id": "11111111-0000-0000-0000-000000000001"}],
                "severidade": "critica",
                "audiencia": "ambos",
                "agente": "seed",
            },
        )
        response.raise_for_status()


def main() -> None:
    seeder = SupabaseSeeder()
    operator_id = seeder.ensure_user(
        email=OPERATOR_EMAIL,
        nome="Operador Stocky",
        role="operador",
    )
    admin_id = seeder.ensure_user(
        email=ADMIN_EMAIL,
        nome="Admin Stocky",
        role="admin",
    )
    seeder.ensure_ai_log()

    print("Seed complete.")
    print(f"Operator: {OPERATOR_EMAIL} / {TEST_PASSWORD} ({operator_id})")
    print(f"Admin: {ADMIN_EMAIL} / {TEST_PASSWORD} ({admin_id})")


if __name__ == "__main__":
    main()
