from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from utils.unit_of_work import UnitOfWork
from api.v1.auth.dependencies import get_current_admin
from api.v1.structure import services as srv
from api.v1.structure import exceptions as exp
import api.v1.structure.dependencies as dep
from api.v1.structure.data_models import Assignment
from schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentInDB,
    UserInDB,
    Position,
    PositionUpdate
)

router = APIRouter()


@router.post("/create-department")
async def create_department(new_dep: DepartmentCreate,
                            admin: Annotated[UserInDB, Depends(get_current_admin)],
                            uow: Annotated[UnitOfWork, Depends()]):
    path = "0"
    if new_dep.parent_id is not None:
        parent = await dep.get_department(new_dep.parent_id, admin, uow)
        path = parent.path

    try:
        new_dep = DepartmentInDB(**new_dep.model_dump(exclude={"parent_id"}),
                                 path=path, company_id=admin.company_id)
        new_dep = await srv.create_new_department(new_dep, uow)
        return new_dep
    except exp.HandleDepartmentException:
        raise HTTPException(400, detail="Error in create department")


@router.put("/update-department/{id}")
async def update_department(id: int,
                            admin: Annotated[UserInDB, Depends(get_current_admin)],
                            update: DepartmentUpdate,
                            uow: Annotated[UnitOfWork, Depends()]):
    old_dep = await dep.get_department(id, admin, uow)
    data = update.model_dump(exclude_unset=True)
    path = old_dep.path
    if "parent_id" in data and data["parent_id"] is None:
        del data["parent_id"]
        path = str(id)
    elif "parent_id" in data:
        parent = await dep.get_department(data.pop("parent_id"), admin, uow)
        if parent.path.startswith(f"{old_dep.path}."):
            raise HTTPException(400, "There cannot be cyclical paths.")
        path = f"{parent.path}.{id}"
    new_dep = old_dep.model_copy(update={"path": path, **data})

    try:
        up_dep = await srv.update_department(old_dep, new_dep, uow)
        return up_dep
    except exp.HandleDepartmentException:
        raise HTTPException(400, detail="Error in update department")


@router.delete("/delete-department/{id}")
async def delete_department(id: int,
                            admin: Annotated[UserInDB, Depends(get_current_admin)],
                            uow: Annotated[UnitOfWork, Depends()]):
    del_dep = await dep.get_department(id, admin, uow)
    try:
        await srv.delete_department(id_=del_dep.id, uow=uow)
    except exp.HandleDepartmentException:
        raise HTTPException(400, detail="Error in delete department")


@router.post("/create-position", dependencies=[Depends(get_current_admin)])
async def create_position(data: Position,
                          admin: Annotated[UserInDB, Depends(get_current_admin)],
                          uow: Annotated[UnitOfWork, Depends()]):
    try:
        await dep.get_department(data.department_id, admin, uow)
        pos = await srv.create_position(data, uow)
        return pos
    except exp.HandlePositionException:
        raise HTTPException(400, detail="Error in create position")


@router.put("/update-position/{id}")
async def update_position(id: Annotated[int, Depends(dep.check_position)],
                          data: PositionUpdate,
                          admin: Annotated[UserInDB, Depends(get_current_admin)],
                          uow: Annotated[UnitOfWork, Depends()]):
    try:
        if data.department_id:
            await dep.get_department(data.department_id, admin, uow)
        pos = await srv.update_position(id, data, uow)
        return pos
    except exp.HandlePositionException:
        raise HTTPException(400, detail="Error in update position")


@router.delete("/delete-position/{id}", dependencies=[Depends(get_current_admin)])
async def delete_position(id: Annotated[int, Depends(dep.check_position)],
                          uow: Annotated[UnitOfWork, Depends()]):
    try:
        await srv.delete_position(id, uow)
    except exp.HandlePositionException:
        raise HTTPException(400, detail="Error in delete position")


@router.post("/assign-user", dependencies=[Depends(get_current_admin)])
async def assign_user(data: Annotated[Assignment, Depends(dep.check_assignment_data)],
                      uow: Annotated[UnitOfWork, Depends()]):
    try:
        user = await srv.assign_user_to_position(data, uow)
        return user
    except exp.HandlePositionException:
        raise HTTPException(400, detail="Error in assign user to position")
