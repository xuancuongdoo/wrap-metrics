from pydantic_settings import BaseSettings
from pydantic import (
    Field,
    PostgresDsn,
)


class Settings(BaseSettings):
    postgres_user: str = Field(..., env='POSTGRES_USER')
    postgres_password: str = Field(..., env='POSTGRES_PASSWORD')
    postgres_db: str = Field(..., env='POSTGRES_DB')
    postgres_port: int = Field(..., env='POSTGRES_PORT')
    postgres_host: str = Field(..., env='POSTGRES_HOST')
    log_level: str = Field('INFO', env='LOG_LEVEL')


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'




settings = Settings()
