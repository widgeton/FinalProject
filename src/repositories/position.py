from utils.repository import SQLAlchemyDelRepository
from models import PositionModel


class PositionRepository(SQLAlchemyDelRepository):
    model = PositionModel
