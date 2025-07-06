from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    DATABASE_URL: str
    CSV_PATH: str
    SCRAPING_TARGET_URL: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
