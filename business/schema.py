from typing import Optional

from ninja import Schema


class Token(Schema):
    token_type: str
    access_token: str
    refresh_token: str


class Message(Schema):
    detail: str


class CreateResourceMessage(Schema):
    detail: str
    id: Optional[str] = None
