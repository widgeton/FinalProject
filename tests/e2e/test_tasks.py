import pytest

from models import TaskModel, UserModel
from models.task import TaskExecutorModel
import funcs
from fakes.params import CREATE_TASK_PARAMS, UPDATE_TASK_PARAMS
from fakes.data import EXPECTED_TASKS_DATA


@pytest.mark.parametrize(
    "data, exp",
    CREATE_TASK_PARAMS
)
def test_create_task(set_company_user_data,
                     admin_token,
                     client,
                     data, exp):
    client.cookies.set("access_token", admin_token)
    res = client.post('/api/v1/tasks/create-task', json=data)
    assert res.json() == exp


@pytest.mark.parametrize(
    "task_id, data, exp",
    UPDATE_TASK_PARAMS
)
def test_update_task(set_company_user_data,
                     set_task_data,
                     admin_token,
                     client,
                     task_id,
                     data, exp):
    client.cookies.set("access_token", admin_token)
    res = client.put(f'/api/v1/tasks/update-task/{task_id}', json=data)
    assert res.json() == exp


@pytest.mark.asyncio
async def test_add_observer(async_session,
                            set_company_user_data,
                            set_task_data,
                            admin_token,
                            client):
    data = {"task_id": 2, "user_id": 2}
    client.cookies.set("access_token", admin_token)
    res = client.post('/api/v1/tasks/add-observer', json=data)
    assert res.json() == EXPECTED_TASKS_DATA["Test"]
    task = await funcs.get_item(async_session, TaskModel, data["task_id"])
    user = await funcs.get_item(async_session, UserModel, data["user_id"])
    assert user in task.observers


@pytest.mark.parametrize(
    "set_data, send_data, result",
    (
            (
                    {"task_id": 2, "executor_id": 2},
                    {"task_id": 2, "user_id": 2},
                    EXPECTED_TASKS_DATA["Test"]
            ),
            (
                    {"task_id": 2, "executor_id": 2},
                    {"task_id": 2, "user_id": 1},
                    {"detail": "User is not executor of the task."}
            ),
    )
)
@pytest.mark.asyncio
async def test_remove_executor(async_session,
                               set_company_user_data,
                               set_task_data,
                               admin_token,
                               client,
                               set_data, send_data, result):
    await funcs.add_item(async_session, TaskExecutorModel, set_data)
    await async_session.commit()

    client.cookies.set("access_token", admin_token)
    res = client.request('DELETE', '/api/v1/tasks/remove-executor', json=send_data)
    assert res.json() == result

    task = await funcs.get_item(async_session, TaskModel, send_data["task_id"])
    user = await funcs.get_item(async_session, UserModel, send_data["user_id"])
    assert user not in task.executors

    await funcs.clean_table(async_session, TaskExecutorModel)
    await async_session.commit()
