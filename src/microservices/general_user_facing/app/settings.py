from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_keyspace: str = Field(default='chat_app', env="DB_KEYSPACE")


settings = Settings()
