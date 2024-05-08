from .company import CompanyInDB
from .user import User
from .position import Position
from .task import Task


class UserWithCompany(User):
    id: int
    company: CompanyInDB


class UserWithPosition(User):
    position: Position


class TaskRel(Task):
    author: User
    charged: User
    observers: list[User]
    executors: list[User]
