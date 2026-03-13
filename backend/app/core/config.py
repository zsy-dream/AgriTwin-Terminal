from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "智汇大棚"
    env: str = "dev"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
