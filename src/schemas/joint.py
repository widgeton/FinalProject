from . import company as c
from . import user as u


class UserRelInDB(u.UserInDB):
    company: c.CompanyInDB


class CompanyRelInDB(c.CompanyInDB):
    users: list[u.UserInDB]
