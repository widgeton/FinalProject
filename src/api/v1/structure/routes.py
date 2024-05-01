from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas import DepartmentCreate, DepartmentUpdate, UserInDB
from utils.unit_of_work import UnitOfWork
from api.v1.auth.dependencies import get_current_admin
from api.v1.structure import services as srv
from api.v1.structure import exceptions as exp
from api.v1.structure.dependencies import get_department

router = APIRouter()


@router.post("/create-department")
async def create_department(dep: DepartmentCreate,
                            admin: Annotated[UserInDB, Depends(get_current_admin)],
                            uow: Annotated[UnitOfWork, Depends()]):
    path = "0"
    if dep.parent_id is not None:
        parent = await get_department(dep.parent_id, admin, uow)
        path = parent.path

    try:
        new_dep = await srv.create_new_department(**dep.model_dump(exclude={"parent_id"}),
                                                  parent_path=path,
                                                  company_id=admin.company_id,
                                                  uow=uow)
        return new_dep
    except exp.HandleDepartmentException:
        raise HTTPException(400, detail="Error in create department")


@router.put("/update-department/{id}")
async def update_department(id: int,
                            admin: Annotated[UserInDB, Depends(get_current_admin)],
                            update: DepartmentUpdate,
                            uow: Annotated[UnitOfWork, Depends()]):
    old_dep = await get_department(id, admin, uow)
    data = update.model_dump(exclude_unset=True)
    path = old_dep.path
    if "parent_id" in data and data["parent_id"] is None:
        del data["parent_id"]
        path = str(id)
    elif "parent_id" in data:
        parent = await get_department(data.pop("parent_id"), admin, uow)
        path = f"{parent.path}.{id}"
    new_dep = old_dep.model_copy(update={"path": path, **data})

    try:
        dep = await srv.update_department(uow, old_dep, new_dep)
        return dep
    except exp.HandleDepartmentException:
        raise HTTPException(400, detail="Error in update department")


@router.delete("/delete-department/{id}")
async def delete_department(id: int,
                            admin: Annotated[UserInDB, Depends(get_current_admin)],
                            uow: Annotated[UnitOfWork, Depends()]):
    dep = await get_department(id, admin, uow)
    try:
        await srv.delete_department(id_=dep.id, uow=uow)
    except exp.HandleDepartmentException:
        raise HTTPException(400, detail="Error in delete department")