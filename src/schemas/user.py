from pydantic import BaseModel

from database.models.user import Roles


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: Roles


class UserInDB(User):
    id: int
    hashed_pass: str
