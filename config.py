from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ATS Resume Score API"
    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    USE_AI: bool = True

    class Config:
        env_file = ".env"

settings = Settings()