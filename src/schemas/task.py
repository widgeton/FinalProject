from datetime import datetime, timedelta

from pydantic import BaseModel, Field, field_validator
from models.field_types import Statuses


class Task(BaseModel):
    title: str = Field(examples=["Implement authentication"])
    description: str
    author_id: int | None
    charged_id: int | None
    deadline: datetime = Field(examples=["2024-05-06 00:00"])
    status: Statuses
    estimate: timedelta = Field(examples=["48"], description="hours to complete")

    @field_validator('estimate', mode='before')
    @classmethod
    def validate_estimate(cls, v) -> timedelta:
        if isinstance(v, timedelta):
            return v
        if isinstance(v, str) and v.isdecimal():
            return timedelta(hours=int(v))
        raise ValueError


class TaskInDB(Task):
    id: int


class TaskUpdate(Task):
    title: str | None = Field(examples=["Implement authentication"], default=None)
    description: str | None = None
    author_id: int | None = None
    charged_id: int | None = None
    deadline: datetime | None = Field(examples=["2024-05-06 00:00"], default=None)
    status: Statuses | None = None
    estimate: timedelta | None = Field(examples=["48"], description="hours to complete", default=None)
