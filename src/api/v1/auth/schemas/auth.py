from pydantic import BaseModel

from schemas.field_types import Email, Pass


class OAuth2Body(BaseModel):
    email: Email
    password: Pass
