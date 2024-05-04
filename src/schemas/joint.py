from schemas import CompanyInDB, User, Position


class UserWithCompany(User):
    id: int
    company: CompanyInDB


class UserWithPosition(User):
    position: Position
