from schemas import DepartmentInDB
from utils.unit_of_work import AbstractUnitOfWork
from api.v1.structure.exceptions import HandleDepartmentException


async def create_new_department(name: str,
                                parent_path: str,
                                company_id: int,
                                uow: AbstractUnitOfWork) -> DepartmentInDB:
    try:
        async with uow:
            new_dep = await uow.departments.add(name=name, path="0", company_id=company_id)
            new_dep.path = str(new_dep.id) if parent_path == "0" else f"{parent_path}.{new_dep.id}"
            await uow.commit()
            return new_dep.to_pydantic_schema()
    except Exception:
        raise HandleDepartmentException


async def update_department(uow: AbstractUnitOfWork,
                            old_dep: DepartmentInDB,
                            new_dep: DepartmentInDB) -> DepartmentInDB:
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
