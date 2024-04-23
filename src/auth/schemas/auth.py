from pydantic import BaseModel

from .types import Email, Pass


class OAuth2Body(BaseModel):
    email: Email
    password: Pass
