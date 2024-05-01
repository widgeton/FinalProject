from fastapi import HTTPException

from schemas import UserInDB, DepartmentInDB
from utils.unit_of_work import UnitOfWork


async def get_department(id_: int, admin: UserInDB, uow: UnitOfWork) -> DepartmentInDB:
    async with uow:
        dep = await uow.departments.get({"id": id_})
        if not dep:
            raise HTTPException(400, f"There is no department with ID {id_}.")
        if dep.company_id != admin.company_id:
            raise HTTPException(400, "Could not change another company departments.")
        return dep.to_pydantic_schema()
