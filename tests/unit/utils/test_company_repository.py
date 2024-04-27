import pytest

from repositories import CompanyRepository
from models import CompanyModel
from unit import funcs
from fakes.params import ADD_COMPANY_PARAMS, GET_COMPANY_PARAMS, UPDATE_COMPANY_PARAMS

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "data, expectation",
    ADD_COMPANY_PARAMS
)
async def test_add_company(async_session, data, expectation):
    await funcs.clean_table(async_session, CompanyModel)
    repo = CompanyRepository(async_session)
    with expectation:
        item = await repo.add(**data)
        await async_session.commit()
        db_item = await funcs.get_item(async_session, CompanyModel, data["id"])
        assert item == db_item
        for arg, value in data.items():
            assert db_item.__dict__[arg] == value


@pytest.mark.parametrize(
    "data, reference, expectation",
    GET_COMPANY_PARAMS
)
async def test_get_company(async_session, data, reference, expectation):
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, data)
    await async_session.commit()
    repo = CompanyRepository(async_session)
    with expectation:
        item = await repo.get(reference=reference)
        db_item = await funcs.get_item(async_session, CompanyModel, data["id"])
        assert item is not None, "Got None object"
        assert item == db_item
        for arg, value in data.items():
            assert db_item.__dict__[arg] == value


@pytest.mark.parametrize(
    "data, id_, new_data, expectation",
    UPDATE_COMPANY_PARAMS
)
async def test_update_company(async_session, data, id_, new_data, expectation):
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, data)
    await async_session.commit()
    repo = CompanyRepository(async_session)
    with expectation:
        item = await repo.update(id_=id_, **new_data)
        await async_session.commit()
        db_item = await funcs.get_item(async_session, CompanyModel, data["id"])
        assert item == db_item
        for arg, value in new_data.items():
            assert db_item.__dict__[arg] == value
