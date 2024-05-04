from typing import Annotated

from fastapi import HTTPException, Depends

from schemas import UserInDB, DepartmentInDB
from utils.unit_of_work import UnitOfWork
from api.v1.auth.dependencies import get_current_admin
from api.v1.structure.data_models import Assignment


async def get_department(id_: int, admin: UserInDB, uow: UnitOfWork) -> DepartmentInDB:
    async with uow:
        dep = await uow.departments.get({"id": id_})
        if not dep:
            raise HTTPException(400, f"There is no department with ID {id_}.")
        if dep.company_id != admin.company_id:
            raise HTTPException(400, "Could not change another company departments.")
        return dep.to_pydantic_schema()


async def check_position(id: int,
                         admin: Annotated[UserInDB, Depends(get_current_admin)],
                         uow: Annotated[UnitOfWork, Depends()]) -> int:
    async with uow:
        pos = await uow.positions.get({"id": id})
        if not pos:
            raise HTTPException(400, f"There is no position with ID {id}.")
        if pos.department.company_id != admin.company_id:
            raise HTTPException(400, "Could not change another company departments.")
        return id


async def check_assignment_data(
        data: Assignment,
        admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
) -> Assignment:
    async with uow:
        user = await uow.users.get({"id": data.user_id})
        if not user or user.company_id != admin.company_id:
            raise HTTPException(400, "Inappropriate user ID.")
        position = await uow.positions.get({"id": data.position_id})
        if not position or position.departent.company_id != admin.company_id:
            raise HTTPException(400, "Inappropriate position ID.")
        return data
