from pydantic import BaseModel


class ChatBase(BaseModel):
    chat_id: str
    messages: dict
