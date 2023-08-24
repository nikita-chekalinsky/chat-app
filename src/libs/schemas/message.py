from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Message(BaseModel):
    chat_id: UUID
    message_timestamp: datetime | None = None
    sender_id: UUID
    attachment_links: set[str] = set()
    message_text: str
