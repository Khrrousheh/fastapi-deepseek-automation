from pydantic_settings import BaseSettings
from pydantic import SecretStr, ValidationError

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: SecretStr      # Marks the key as sensitive
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra env vars

try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError("Missing or invalid .env file!") from e