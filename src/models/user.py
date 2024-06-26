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
    position: Mapped["PositionModel"] = relationship(secondary="user_position", back_populates="users")
    authored_tasks: Mapped[list["TaskModel"]] = relationship(primaryjoin="UserModel.id == TaskModel.author_id",
                                                             back_populates="author")
    charged_tasks: Mapped[list["TaskModel"]] = relationship(primaryjoin="UserModel.id == TaskModel.charged_id",
                                                            back_populates="charged")
    observed_tasks: Mapped[list["TaskModel"]] = relationship(secondary="task_observer", back_populates="observers")
    running_tasks: Mapped[list["TaskModel"]] = relationship(secondary="task_executor", back_populates="executors")

    async def to_pydantic_schema(self) -> UserWithCompany:
        company = await self.awaitable_attrs.company
        attrs = self.__dict__.copy()
        del attrs['company']
        return UserWithCompany(**attrs, company=company.to_pydantic_schema())
