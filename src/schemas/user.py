from typing import Any

from pydantic import BaseModel, Field, model_validator

from database.models.user import Roles


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: Roles
    company_id: int | None = None


class UserUpdate(BaseModel):
    email: str | None = Field(validation_alias="new_email", default=None)
    first_name: str | None = Field(validation_alias="new_first_name", default=None)
    last_name: str | None = Field(validation_alias="new_last_name", default=None)
    role: Roles | None = Field(validation_alias="new_role", default=None)

    @model_validator(mode='before')
    @classmethod
    def check_fields_nonempty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for val in data.values():
                if isinstance(val, str) and not val.strip():
                    raise ValueError('Fields must not be empty')
        return data


class UserInDB(User):
    id: int
    hashed_pass: str
