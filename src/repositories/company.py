from utils.repository import SQLAlchemyRepository
from models import CompanyModel


class CompanyRepository(SQLAlchemyRepository):
    model = CompanyModel
