from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI RAG 客服 API"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/rag"

    model_config = {"env_file": ".env"}


settings = Settings()
