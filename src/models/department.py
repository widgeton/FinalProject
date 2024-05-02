from sqlalchemy import Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel
from models.field_types import pk
from schemas import DepartmentInDB


class DepartmentModel(BaseModel):
    __tablename__ = 'department'

    id: Mapped[pk]
    name: Mapped[str]
    path: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))

    __table_args__ = (
        Index('ix_department_path',
              'path', postgresql_using="gist",
              postgresql_ops={'path': 'gist_trgm_ops'}),
    )

    def to_pydantic_schema(self) -> DepartmentInDB:
        return DepartmentInDB(**self.__dict__)
