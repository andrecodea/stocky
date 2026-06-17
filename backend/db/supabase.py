"""Supabase client singletons for backend operations."""

from supabase import create_client, Client
from config import settings

_anon_client: Client | None = None
_admin_client: Client | None = None


def get_anon_client() -> Client:
    """Return a Supabase client using the anon key.

    Used for auth operations (login/signup) that rely on the native
    Supabase Auth flow.
    """
    global _anon_client
    if _anon_client is None:
        _anon_client = create_client(settings.supabase_url, settings.supabase_anon_key)
    return _anon_client


def get_admin_client() -> Client:
    """Return a Supabase client using the service role key.

    Used for all data operations. Authorization is handled at the
    FastAPI dependency layer, so RLS is bypassed intentionally.
    """
    global _admin_client
    if _admin_client is None:
        _admin_client = create_client(
            settings.supabase_url, settings.supabase_service_role_key
        )
    return _admin_client
