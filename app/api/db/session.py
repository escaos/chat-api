from supabase_py import create_client, Client
from app.api.core.config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SECRET_KEY)
