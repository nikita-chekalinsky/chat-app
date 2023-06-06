from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    chat_id: str
    message_timestamp: datetime = datetime.now()
    sender_id: str
    attachment_links: list[str] = []
    message_text: str
