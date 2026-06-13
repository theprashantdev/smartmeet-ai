from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    database_url: str
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    whisper_model: str = "base"
    openrouter_model: str = "openai/gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = Settings()
