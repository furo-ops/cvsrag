from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    anthropic_api_key: str
    chroma_db_path: str = "./data/chroma_db"
    cv_directory: str = "./data/cvs"
    availability_file: str = "./data/availability.csv"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "claude-sonnet-4-20250514"
    top_k_results: int = 20
    rerank_top_n: int = 10
    admin_username: Optional[str] = None
    admin_password: Optional[str] = None
    max_upload_mb: int = 25

    class Config:
        env_file = ".env"


settings = Settings()
