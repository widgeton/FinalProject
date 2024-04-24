import enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base, pk


class Roles(enum.Enum):
    admin = "admin"
    chief = "chief"
    worker = "worker"


class User(Base):
    __tablename__ = "user"

    id: Mapped[pk]
    email: Mapped[str] = mapped_column(String(256), unique=True)
    hashed_pass: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[Roles]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    company: Mapped["Company"] = relationship(back_populates="users", lazy="joined")
