from pydantic import BaseModel, Field


class Department(BaseModel):
    name: str = Field(max_length=64, examples=["Development"])


class DepartmentInDB(Department):
    id: int | None = None
    company_id: int
    path: str = Field(pattern=r"^(?:0|([1-9]\d{0,8}(\.[1-9]\d{0,8})*))$")


class DepartmentCreate(Department):
    parent_id: int | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = Field(max_length=64, examples=["Development"], default=None)
    parent_id: int | None = Field(examples=[1], default=None)
