from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_TTL_MIN: int

    class Config:
        env_file = ".env"


settings = Settings()
