from schemas import CompanyInDB, UserInDB


class UserRelInDB(UserInDB):
    company: CompanyInDB


class CompanyRelInDB(CompanyInDB):
    users: list[UserInDB]
