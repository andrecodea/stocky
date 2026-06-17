from __future__ import annotations

import os
import sys
import unittest
import importlib
from pathlib import Path
from unittest.mock import patch

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


class SettingsTest(unittest.TestCase):
    def test_accepts_supabase_cli_env_names(self):
        cli_env = {
            "API_URL": "http://127.0.0.1:54321",
            "ANON_KEY": "anon-local",
            "SERVICE_ROLE_KEY": "service-local",
        }

        with patch.dict(os.environ, cli_env, clear=True):
            sys.modules.pop("config", None)
            from config import Settings

            settings = Settings(_env_file=None)

        self.assertEqual(settings.supabase_url, "http://127.0.0.1:54321")
        self.assertEqual(settings.supabase_anon_key, "anon-local")
        self.assertEqual(settings.supabase_service_role_key, "service-local")

    def test_accepts_supabase_publishable_and_secret_key_env_names(self):
        cli_env = {
            "API_URL": "http://127.0.0.1:54321",
            "PUBLISHABLE_KEY": "publishable-local",
            "SECRET_KEY": "secret-local",
        }

        with patch.dict(os.environ, cli_env, clear=True):
            sys.modules.pop("config", None)
            config = importlib.import_module("config")
            settings = config.Settings(_env_file=None)

        self.assertEqual(settings.supabase_anon_key, "publishable-local")
        self.assertEqual(settings.supabase_service_role_key, "secret-local")


if __name__ == "__main__":
    unittest.main()
