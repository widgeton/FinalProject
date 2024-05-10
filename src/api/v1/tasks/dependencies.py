from typing import Annotated

from fastapi import Depends, HTTPException

from api.v1.auth.dependencies import get_current_admin
from api.v1.tasks.data_models import UserTaskID
from utils.unit_of_work import UnitOfWork
from schemas import Task, UserInDB, TaskUpdate


async def check_user(
        reference: dict,
        admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
):
    async with uow:
        user = await uow.users.get(reference)
        if not user:
            raise HTTPException(400, "Wrong user reference.")
        if user.company_id != admin.company_id:
            raise HTTPException(400, "User is not in admin company.")
        return user


async def check_task_user_data(
        data: Task, admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
):
    if data.charged_id is not None:
        await check_user({"id": data.charged_id}, admin, uow)
    return data


async def check_task_id(
        task_id: int,
        admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
):
    async with uow:
        task = await uow.tasks.get({"id": task_id})
        if not task or task.author.company_id != admin.company_id:
            raise HTTPException(400, "Wrong task reference.")
        return task_id


async def check_update_task_user_data(
        data: TaskUpdate, admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
):
    await check_task_user_data(data, admin, uow)
    return data


async def check_user_task_id(
        data: UserTaskID, admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
):
    await check_user({"id": data.user_id}, admin, uow)
    await check_task_id(data.task_id, admin, uow)
    return data


async def check_observers_data_for_remove(
        data: Annotated[UserTaskID, Depends(check_user_task_id)],
        uow: Annotated[UnitOfWork, Depends()]
):
    async with uow:
        user = await uow.users.get({"id": data.user_id})
        task = await uow.tasks.get({"id": data.task_id})
        observers = await task.awaitable_attrs.observers
        if user not in observers:
            raise HTTPException(400, "User is not observer of the task.")
        return data


async def check_executors_data_for_remove(
        data: Annotated[UserTaskID, Depends(check_user_task_id)],
        uow: Annotated[UnitOfWork, Depends()]
):
    async with uow:
        user = await uow.users.get({"id": data.user_id})
        task = await uow.tasks.get({"id": data.task_id})
        executors = await task.awaitable_attrs.executors
        if user not in executors:
            raise HTTPException(400, "User is not executor of the task.")
        return data
