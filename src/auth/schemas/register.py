from typing import Any

from pydantic import BaseModel, field_validator, model_validator

import auth.services.common as srv


class CompanyRegister(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    company_name: str

    @model_validator(mode='before')
    @classmethod
    def check_fields_nonempty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for val in data.values():
                if isinstance(val, str) and not val.strip():
                    raise ValueError('Fields must not be empty')
        return data

    @field_validator('email')
    @classmethod
    def check_email(cls, v: str) -> str:
        if not srv.is_email(v):
            raise ValueError('Wrong email format')
        return v

    @field_validator('password')
    @classmethod
    def password_must_contain_more_then_six_chars(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Pass must have six or more chars')
        return v
