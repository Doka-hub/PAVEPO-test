from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class ConfigDict:
        env_file = '.env'

    DATABASE_URL: str
    BASE_URL: str = 'http://localhost:8000/api/v1'

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # YANDEX
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str


@lru_cache()
def get_settings(env_file: str = '.env'):
    return Settings(_env_file=env_file)
