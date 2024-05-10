from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas import Task, TaskUpdate, UserInDB
from utils.unit_of_work import UnitOfWork
from api.v1.tasks import dependencies as dep
from api.v1.tasks import exceptions as exp
from api.v1.tasks import services as srv
from api.v1.tasks.data_models import UserTaskID
from api.v1.auth.dependencies import get_current_admin

router = APIRouter()


@router.post("/create-task")
async def create_task(
        data: Annotated[Task, Depends(dep.check_task_user_data)],
        admin: Annotated[UserInDB, Depends(get_current_admin)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        task = await srv.create_task(data, admin.id, uow)
        return task
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in create task.")


@router.put("/update-task/{task_id}")
async def update_task(
        task_id: Annotated[int, Depends(dep.check_task_id)],
        data: Annotated[TaskUpdate, Depends(dep.check_update_task_user_data)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        task = await srv.update_task(task_id, data, uow)
        return task
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in update task.")


@router.delete("/delete-task/{task_id}")
async def delete_task(
        task_id: Annotated[int, Depends(dep.check_task_id)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        await srv.delete_task(task_id, uow)
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in delete task.")


@router.post("/add-observer")
async def add_observer(
        data: Annotated[UserTaskID, Depends(dep.check_user_task_id)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        task = await srv.add_observer_to_task(data, uow)
        return task
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in add observer to the task.")


@router.delete("/remove-observer")
async def remove_observer(
        data: Annotated[UserTaskID, Depends(dep.check_observers_data_for_remove)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        task = await srv.remove_observer_from_task(data, uow)
        return task
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in remove observer from the task.")


@router.post("/add-executor")
async def add_executor(
        data: Annotated[UserTaskID, Depends(dep.check_user_task_id)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        task = await srv.add_executor_to_task(data, uow)
        return task
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in add executor to the task.")


@router.delete("/remove-executor")
async def remove_executor(
        data: Annotated[UserTaskID, Depends(dep.check_executors_data_for_remove)],
        uow: Annotated[UnitOfWork, Depends()]
):
    try:
        task = await srv.remove_executor_from_task(data, uow)
        return task
    except exp.HandleTaskException:
        raise HTTPException(400, "Error in remove executor from the task.")
