from pydantic import BaseModel, Field

from schemas.field_types import Pass, Str


class UserRegister(BaseModel):
    first_name: Str = Field(examples=["John"])
    last_name: Str = Field(examples=["Doe"])
    password: Pass


class CompanyRegister(UserRegister):
    company_name: str = Field(examples=["Google"])
