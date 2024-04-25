from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.field_types import Roles, pk
from models.base import BaseModel
from schemas import UserWithCompany


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[pk]
    email: Mapped[str] = mapped_column(String(256), unique=True)
    hashed_pass: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[Roles]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    company: Mapped["CompanyModel"] = relationship(back_populates="users", lazy="joined")

    async def to_pydantic_schema(self) -> UserWithCompany:
        company = await self.awaitable_attrs.company
        return UserWithCompany(id=self.id, email=self.email,
                               first_name=self.first_name,
                               last_name=self.last_name,
                               role=self.role,
                               company=company.to_pydantic_schema())
