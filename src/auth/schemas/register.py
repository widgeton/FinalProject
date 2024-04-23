from typing import Any

from pydantic import BaseModel, Field, model_validator


class CompanyRegister(BaseModel):
    email: str = Field(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                       examples=["user@gmail.com"])
    token: str = Field(examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                 "eyJzdWIiOiJ1c2VyQGdtYWlsLmNvbSIsImV4cCI6MTcxMzg3NDAyNX0."
                                 "cCS-lLzP8kJGTifgFmAX76myjcHA7euj6i_QjdPu8Aw"])


class CompleteCompanyRegister(BaseModel):
    email: str = Field(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                       examples=["user@gmail.com"])
    password: str = Field(min_length=6, examples=["NjuyT56Yu/U%g"])
    first_name: str = Field(examples=["John"])
    last_name: str = Field(examples=["Doe"])
    company_name: str = Field(examples=["Google"])

    @model_validator(mode='before')
    @classmethod
    def check_fields_nonempty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for val in data.values():
                if isinstance(val, str) and not val.strip():
                    raise ValueError('Fields must not be empty')
        return data
