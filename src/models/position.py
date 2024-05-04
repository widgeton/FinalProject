from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseModel
from models.field_types import pk
from schemas import PositionInDB


class UserPositionModel(BaseModel):
    __tablename__ = 'user_position'

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("position.id", ondelete="CASCADE"), primary_key=True)


class PositionModel(BaseModel):
    __tablename__ = 'position'

    id: Mapped[pk]
    name: Mapped[str]
    department_id: Mapped[int] = mapped_column(ForeignKey("department.id", ondelete="CASCADE"))

    users: Mapped[list["UserModel"]] = relationship(secondary="user_position", back_populates="position")
    department: Mapped["DepartmentModel"] = relationship(lazy="joined")

    def to_pydantic_schema(self) -> PositionInDB:
        return PositionInDB(**self.__dict__)
