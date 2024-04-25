from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SMTP_USER: str
    SMTP_PASS: str
    SMTP_HOST: str
    SMTP_PORT: str

    JWT_SECRET_KEY: str

    MODE: str

    @property
    def DB_URL(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='.env')


load_dotenv(find_dotenv('.env'))
settings = Settings()
