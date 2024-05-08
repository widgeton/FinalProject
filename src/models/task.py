from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel
from models.field_types import pk, Statuses
from schemas import TaskInDB


class TaskModel(BaseModel):
    __tablename__ = "task"

    id: Mapped[pk]
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    charged_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    deadline: Mapped[datetime]
    status: Mapped[Statuses]
    estimate: Mapped[timedelta]

    author: Mapped["UserModel"] = relationship(foreign_keys=author_id,
                                               back_populates="authored_tasks",
                                               lazy="joined")
    charged: Mapped["UserModel"] = relationship(foreign_keys=charged_id,
                                                back_populates="charged_tasks",
                                                lazy="joined")
    observers: Mapped[set["UserModel"]] = relationship(secondary="task_observer",
                                                        back_populates="observed_tasks",
                                                        lazy="selectin")
    executors: Mapped[set["UserModel"]] = relationship(secondary="task_executor",
                                                        back_populates="running_tasks",
                                                        lazy="selectin")

    def to_pydantic_schema(self) -> TaskInDB:
        return TaskInDB(**self.__dict__)


class TaskObserverModel(BaseModel):
    __tablename__ = 'task_observer'

    observer_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"), primary_key=True)


class TaskExecutorModel(BaseModel):
    __tablename__ = 'task_executor'

    executor_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"), primary_key=True)
