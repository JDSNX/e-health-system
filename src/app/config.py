import logging

from pydantic_settings import BaseSettings, SettingsConfigDict
from requests.structures import CaseInsensitiveDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


headers = CaseInsensitiveDict
headers = {"Content-Type": "application/json"}


class Settings(BaseSettings):
    URL: str
    SMS_API_KEY: str
    SMS_URL: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()