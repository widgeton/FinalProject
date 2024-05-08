from utils.repository import SQLAlchemyDelRepository
from models import TaskModel


class TaskRepository(SQLAlchemyDelRepository):
    model = TaskModel
