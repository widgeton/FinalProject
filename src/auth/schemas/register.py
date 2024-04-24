from typing import Any

from pydantic import BaseModel, Field, model_validator

from .types import Email, Pass


class UserRegister(BaseModel):
    first_name: str = Field(examples=["John"])
    last_name: str = Field(examples=["Doe"])
    password: Pass

    @model_validator(mode='before')
    @classmethod
    def check_fields_nonempty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for val in data.values():
                if isinstance(val, str) and not val.strip():
                    raise ValueError('Fields must not be empty')
        return data


class CompanyRegister(BaseModel):
    email: Email
    token: str = Field(examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJzdWIiOiJ1c2VyQGdtYWlsLmNvbSIsImV4cCI6MTcxMzg3NDAyNX0."
                                 "cCS-lLzP8kJGTifgFmAX76myjcHA7euj6i_QjdPu8Aw"])


class CompleteCompanyRegister(UserRegister):
    email: Email
    company_name: str = Field(examples=["Google"])
