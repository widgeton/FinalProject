from sqlalchemy.orm import Mapped, relationship

from database.db import Base, pk


class Company(Base):
    __tablename__ = "company"

    id: Mapped[pk]
    name: Mapped[str]

    users: Mapped[list["User"]] = relationship(back_populates="company")
