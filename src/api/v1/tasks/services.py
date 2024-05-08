from schemas import Task, TaskUpdate
from models.field_types import Statuses
from utils.unit_of_work import AbstractUnitOfWork

from api.v1.tasks import exceptions as exp
from api.v1.tasks.data_models import UserTaskID


async def create_task(data: Task, uow: AbstractUnitOfWork):
    try:
        async with uow:
            task = await uow.tasks.add(**data.model_dump(exclude={"status"}), status=Statuses.wait)
            await uow.commit()
            return task.to_pydantic_schema()
    except Exception:
        raise exp.HandleTaskException


async def update_task(task_id: int, data: TaskUpdate, uow: AbstractUnitOfWork):
    try:
        async with uow:
            task = await uow.tasks.update(id_=task_id, **data.model_dump(exclude_none=True))
            await uow.commit()
            return task.to_pydantic_schema()
    except Exception:
        raise exp.HandleTaskException


async def delete_task(task_id: int, uow: AbstractUnitOfWork):
    try:
        async with uow:
            await uow.tasks.delete(id_=task_id)
            await uow.commit()
    except Exception:
        raise exp.HandleTaskException


async def add_observer_to_task(data: UserTaskID, uow: AbstractUnitOfWork):
    try:
        async with uow:
            user = await uow.users.get({"id": data.user_id})
            task = await uow.tasks.get({"id": data.task_id})
            task.observers.add(user)
            await uow.commit()
            return task.to_pydantic_schema()
    except Exception:
        raise exp.HandleTaskException


async def remove_observer_from_task(data: UserTaskID, uow: AbstractUnitOfWork):
    try:
        async with uow:
            user = await uow.users.get({"id": data.user_id})
            task = await uow.tasks.get({"id": data.task_id})
            task.observers.remove(user)
            await uow.commit()
            return task.to_pydantic_schema()
    except Exception:
        raise exp.HandleTaskException


async def add_executor_to_task(data: UserTaskID, uow: AbstractUnitOfWork):
    try:
        async with uow:
            user = await uow.users.get({"id": data.user_id})
            task = await uow.tasks.get({"id": data.task_id})
            task.executors.add(user)
            await uow.commit()
            return task.to_pydantic_schema()
    except Exception:
        raise exp.HandleTaskException


async def remove_executor_from_task(data: UserTaskID, uow: AbstractUnitOfWork):
    try:
        async with uow:
            user = await uow.users.get({"id": data.user_id})
            task = await uow.tasks.get({"id": data.task_id})
            task.executors.remove(user)
            await uow.commit()
            return task.to_pydantic_schema()
    except Exception:
        raise exp.HandleTaskException
