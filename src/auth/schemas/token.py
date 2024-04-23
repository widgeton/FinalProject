from pydantic import BaseModel


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str
