from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class ConfigDict:
        env_file = '.env'

    DATABASE_URL: str = 'sqlite+aiosqlite:///./test.db'
    BASE_URL: str = 'http://localhost:8000/api/v1'


@lru_cache()
def get_settings():
    return Settings()
