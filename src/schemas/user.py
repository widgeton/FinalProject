from pydantic import BaseModel, Field

from models.field_types import Roles
from schemas.field_types import Email, Str, Pass


class User(BaseModel):
    email: Email
    first_name: Str
    last_name: Str
    role: Roles


class UserCreate(User):
    password: Pass | None = None
    company_id: int | None = None


class UserUpdate(BaseModel):
    email: Email | None = None
    first_name: Str | None = Field(examples=["John"], default=None)
    last_name: Str | None = Field(examples=["Doe"], default=None)
    role: Roles | None = None


class UserInDB(User):
    id: int
    hashed_pass: str
    company_id: int
