from pydantic import BaseSettings, Field
from uuid import uuid4


class Settings(BaseSettings):
    http_host: str = Field(..., env='HTTP_HOST')
    http_port: int = Field(..., env='HTTP_PORT')
    rmq_host: str = Field(..., env='RMQ_HOST')
    rmq_port: int = Field(..., env='RMQ_PORT')
    rmq_queue_name: str = Field(env='RMQ_QUEUE_NAME',
                                default=str(uuid4()))


settings = Settings()
