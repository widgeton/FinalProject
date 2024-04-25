from schemas import CompanyInDB, User


class UserWithCompany(User):
    id: int
    company: CompanyInDB
