from sqlalchemy.orm import Mapped, relationship

from models.base import BaseModel
from models.field_types import pk
from schemas import CompanyInDB


class CompanyModel(BaseModel):
    __tablename__ = "company"

    id: Mapped[pk]
    name: Mapped[str]

    users: Mapped[list["UserModel"]] = relationship(back_populates="company")

    def to_pydantic_schema(self) -> CompanyInDB:
        return CompanyInDB(id=self.id, name=self.name)
