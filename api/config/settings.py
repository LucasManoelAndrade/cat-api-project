# api/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cat_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
