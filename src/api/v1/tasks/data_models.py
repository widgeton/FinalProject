from pydantic import BaseModel


class UserTaskID(BaseModel):
    task_id: int
    user_id: int
