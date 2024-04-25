from utils.repository import SQLAlchemyRepository
from models import UserModel


class UserRepository(SQLAlchemyRepository):
    model = UserModel
