from datetime import datetime, timedelta

import pytest
from jose import jwt

from fakes.data import USERS, COMPANIES, TASKS
from models import CompanyModel, UserModel, TaskModel
import funcs
from config import settings


@pytest.fixture
async def set_company_user_data(async_session):
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.clean_table(async_session, UserModel)
    await async_session.commit()

    await funcs.add_item(async_session, CompanyModel, COMPANIES["Google"])
    await funcs.add_item(async_session, CompanyModel, COMPANIES["Microsoft"])
    await funcs.add_item(async_session, UserModel, USERS["John"])
    await funcs.add_item(async_session, UserModel, USERS["Peter"])
    await funcs.add_item(async_session, UserModel, USERS["George"])
    await async_session.commit()

    yield

    await funcs.clean_table(async_session, UserModel)
    await funcs.clean_table(async_session, CompanyModel)
    await async_session.commit()


@pytest.fixture
async def set_task_data(async_session):
    await funcs.clean_table(async_session, TaskModel)
    await async_session.commit()

    data = TASKS["Test"].copy()
    data["deadline"] = datetime.fromisoformat(data["deadline"])
    data["estimate"] = timedelta(hours=int(data["estimate"]))
    data["id"] = 2
    await funcs.add_item(async_session, TaskModel, data)
    await async_session.commit()

    yield

    await funcs.clean_table(async_session, TaskModel)
    await async_session.commit()


@pytest.fixture
def admin_token():
    data = {
        'sub': USERS["John"]["email"],
        'scopes': [USERS["John"]["role"].value]
    }
    token = jwt.encode(data, settings.JWT_SECRET_KEY, "HS256")
    return f"Bearer {token}"
