import pytest

from repositories import UserRepository
from models import UserModel, CompanyModel
import funcs
from fakes.params import (
    ADD_USER_PARAMS,
    ADD_UNIQUE_EMAIL_USER_PARAMS,
    GET_USER_PARAMS,
    UPDATE_USER_PARAMS,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "user_data, company_data, expectation",
    ADD_USER_PARAMS
)
async def test_add_user(async_session, user_data, company_data, expectation):
    await funcs.clean_table(async_session, UserModel)
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, company_data)
    await async_session.commit()
    repo = UserRepository(async_session)
    with expectation:
        item = await repo.add(**user_data)
        await async_session.commit()
        db_item = await funcs.get_item(async_session, UserModel, user_data["id"])
        assert item == db_item
        for arg, value in user_data.items():
            assert db_item.__dict__[arg] == value


@pytest.mark.parametrize(
    "user1_data, user2_data, company_data, expectation",
    ADD_UNIQUE_EMAIL_USER_PARAMS
)
async def test_add_unique_email_users(async_session, user1_data, user2_data, company_data, expectation):
    await funcs.clean_table(async_session, UserModel)
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, company_data)
    await funcs.add_item(async_session, UserModel, user1_data)
    await async_session.commit()
    repo = UserRepository(async_session)
    with expectation:
        item = await repo.add(**user2_data)
        db_item = await funcs.get_item(async_session, UserModel, user2_data["id"])
        assert item == db_item


@pytest.mark.parametrize(
    "user_data, company_data, reference, expectation",
    GET_USER_PARAMS
)
async def test_get_user(async_session, user_data, company_data, reference, expectation):
    await funcs.clean_table(async_session, UserModel)
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, company_data)
    await funcs.add_item(async_session, UserModel, user_data)
    await async_session.commit()
    repo = UserRepository(async_session)
    with expectation:
        item = await repo.get(reference=reference)
        db_item = await funcs.get_item(async_session, UserModel, user_data["id"])
        assert item is not None, "Got None object"
        assert item == db_item
        for arg, value in user_data.items():
            assert db_item.__dict__[arg] == value


@pytest.mark.parametrize(
    "user_data, company_data, id_, new_data, expectation",
    UPDATE_USER_PARAMS
)
async def test_update_user(async_session, user_data, company_data, id_, new_data, expectation):
    await funcs.clean_table(async_session, UserModel)
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, company_data)
    await funcs.add_item(async_session, UserModel, user_data)
    await async_session.commit()
    repo = UserRepository(async_session)
    with expectation:
        item = await repo.update(id_=id_, **new_data)
        await async_session.commit()
        db_item = await funcs.get_item(async_session, UserModel, user_data["id"])
        assert item == db_item
        for arg, value in new_data.items():
            assert db_item.__dict__[arg] == value
