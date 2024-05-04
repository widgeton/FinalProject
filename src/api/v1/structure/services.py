from schemas import DepartmentInDB, Position, PositionUpdate, UserWithPosition
from utils.unit_of_work import AbstractUnitOfWork
import api.v1.structure.exceptions as exp
from api.v1.structure.data_models import Assignment


async def create_new_department(new_dep: DepartmentInDB,
                                uow: AbstractUnitOfWork) -> DepartmentInDB:
    try:
        async with uow:
            dep = await uow.departments.add(**new_dep.model_dump(exclude={"id"}))
            dep.path = str(dep.id) if new_dep.path == "0" else f"{new_dep.path}.{dep.id}"
            await uow.commit()
            return dep.to_pydantic_schema()
    except Exception:
        raise exp.HandleDepartmentException


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
        raise exp.HandleDepartmentException


async def delete_department(id_: int, uow: AbstractUnitOfWork):
    try:
        async with uow:
            await uow.departments.delete(id_=id_)
            await uow.commit()
    except Exception:
        raise exp.HandleDepartmentException


async def create_position(data: Position, uow: AbstractUnitOfWork):
    try:
        async with uow:
            pos = await uow.positions.add(**data.model_dump())
            await uow.commit()
            return pos.to_pydantic_schema()
    except Exception:
        raise exp.HandlePositionException


async def update_position(id_: int, data: PositionUpdate, uow: AbstractUnitOfWork):
    try:
        async with uow:
            pos = await uow.positions.update(id_=id_, **data.model_dump(exclude_none=True))
            await uow.commit()
            return pos.to_pydantic_schema()
    except Exception:
        raise exp.HandlePositionException


async def delete_position(id_: int, uow: AbstractUnitOfWork):
    try:
        async with uow:
            await uow.positions.delete(id_=id_)
            await uow.commit()
    except Exception:
        raise exp.HandleDepartmentException


async def assign_user_to_position(data: Assignment, uow: AbstractUnitOfWork):
    try:
        async with uow:
            user = await uow.users.get({"id": data.user_id})
            position = await uow.positions.get({"id": data.position_id})
            user.position = position
            await uow.commit()
            position = Position(**position.__dict__)
            return UserWithPosition(last_name=user.last_name,
                                    first_name=user.first_name,
                                    email=user.email,
                                    role=user.role,
                                    position=position)
    except Exception:
        raise exp.HandlePositionException
