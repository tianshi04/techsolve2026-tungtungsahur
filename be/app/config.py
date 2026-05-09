from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    LLM_API_KEY: str
    LLM_MODEL: str = "gemini-2.0-flash"
    MAX_DIFFICULTY: int = 5

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
