from pydantic import BaseModel


class Company(BaseModel):
    name: str


class CompanyInDB(Company):
    id: int
