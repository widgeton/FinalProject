from sqlalchemy import Index, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel
from models.field_types import pk
from schemas import DepartmentInDB


class DepartmentModel(BaseModel):
    __tablename__ = 'department'

    id: Mapped[pk]
    name: Mapped[str]
    path: Mapped[str] = mapped_column(unique=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    #
    # __table_args__ = (
    #     Index('ix_department_path', 'path'),
    # )

    def to_pydantic_schema(self) -> DepartmentInDB:
        return DepartmentInDB(**self.__dict__)
