from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class SeedTestDataConfigTest(unittest.TestCase):
    def test_required_env_accepts_aliases(self):
        from scripts.seed_test_data import required_env

        with patch.dict(os.environ, {"SECRET_KEY": "secret-local"}, clear=True):
            value = required_env("SUPABASE_SERVICE_ROLE_KEY", aliases=("SECRET_KEY",))

        self.assertEqual(value, "secret-local")


if __name__ == "__main__":
    unittest.main()
