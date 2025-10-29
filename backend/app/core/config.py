from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database (using SQLite for development)
    DATABASE_URL: str = "sqlite:///./ai_search.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # AI Services
    OPENAI_API_KEY: str = ""
    
    # Redis (for caching and task queue)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Scraping
    USER_AGENT: str = "AI-Product-Search-Engine/1.0"
    SCRAPING_DELAY: int = 1  # seconds between requests
    
    class Config:
        env_file = ".env"

settings = Settings()