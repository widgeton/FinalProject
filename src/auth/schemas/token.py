from pydantic import BaseModel


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []
