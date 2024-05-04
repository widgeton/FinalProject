from pydantic import BaseModel, Field


class Position(BaseModel):
    name: str = Field(max_length=64, examples=["Head of department"])
    department_id: int


class PositionInDB(Position):
    id: int


class PositionUpdate(Position):
    name: str | None = Field(max_length=64, examples=["Head of department"], default=None)
    department_id: int | None = None
