from typing import Annotated
from enum import Enum

from sqlalchemy.orm import mapped_column


class Roles(Enum):
    admin = "admin"
    chief = "chief"
    worker = "worker"


pk = Annotated[int, mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)]
