# app/api/core/config.py
from fastapi import Depends
from pydantic import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SECRET_KEY: str
    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    ALGORITHMS: str = "RS256"
    API_AUDIENCE: str

    class Config:
        env_file = ".env"


settings = Settings()
