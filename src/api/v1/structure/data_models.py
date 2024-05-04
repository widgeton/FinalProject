from pydantic import BaseModel


class Assignment(BaseModel):
    position_id: int
    user_id: int
