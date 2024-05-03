from schemas import DepartmentInDB
from utils.unit_of_work import AbstractUnitOfWork
from api.v1.structure.exceptions import HandleDepartmentException


async def create_new_department(new_dep: DepartmentInDB,
                                uow: AbstractUnitOfWork) -> DepartmentInDB:
    try:
        async with uow:
            dep = await uow.departments.add(**new_dep.model_dump(exclude={"id"}))
            dep.path = str(dep.id) if new_dep.path == "0" else f"{new_dep.path}.{dep.id}"
            await uow.commit()
            return dep.to_pydantic_schema()
    except Exception:
        raise HandleDepartmentException


async def update_department(old_dep: DepartmentInDB,
                            new_dep: DepartmentInDB,
                            uow: AbstractUnitOfWork) -> DepartmentInDB:
    if old_dep == new_dep:
        return old_dep

    try:
        async with uow:
            fields = dict(new_dep.model_dump().items() - old_dep.model_dump().items())
            if old_dep.path != new_dep.path:
                fields["old_path"] = old_dep.path
            dep = await uow.departments.update(id_=new_dep.id, **fields)
            await uow.commit()
            return dep.to_pydantic_schema()
    except Exception:
        raise HandleDepartmentException


async def delete_department(id_: int, uow: AbstractUnitOfWork):
    try:
        async with uow:
            await uow.departments.delete(id_=id_)
            await uow.commit()
    except Exception:
        raise HandleDepartmentException
