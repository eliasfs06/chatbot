from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str
    ollama_api_chat_url: str
    model: str
    stream: bool

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
