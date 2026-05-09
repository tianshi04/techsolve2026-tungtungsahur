from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    LLM_API_KEY: str
    LLM_MODEL: str = "gemini-3-flash-preview"
    MAX_DIFFICULTY: int = 5
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
