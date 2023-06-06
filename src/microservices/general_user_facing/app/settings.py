from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    region: str = Field(..., env='AWS_REGION')
    dynamodb_user_key: str = Field(..., env='DYNAMODB_USER_KEY')
    dynamodb_user_secret: str = Field(..., env='DYNAMODB_USER_SECRET')


settings = Settings()
