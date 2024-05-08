from contextlib import nullcontext

import pytest

from models import CompanyModel
from utils.unit_of_work import UnitOfWork
from schemas import CompanyInDB
import funcs
from fakes.data import COMPANIES

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "company_data, commit, expectation",
    [
        (COMPANIES["Apple"], False, pytest.raises(AssertionError, match="Got None object")),
        (COMPANIES["Apple"], True, nullcontext(CompanyInDB(**COMPANIES["Apple"]))),
    ]
)
async def test_uow_commit(async_session, company_data, commit, expectation):
    await funcs.clean_table(async_session, CompanyModel)
    await async_session.commit()
    uow = UnitOfWork()
    async with uow:
        await uow.companies.add(**company_data)
        if commit:
            await uow.commit()

    with expectation as exp:
        db_company = await funcs.get_item(async_session, CompanyModel, company_data["id"])
        assert db_company is not None, "Got None object"
        company = CompanyInDB.model_validate(db_company, from_attributes=True)
        assert company == exp


@pytest.mark.parametrize(
    "company_data",
    [*COMPANIES.values()]
)
async def test_uow_rollback(async_session, company_data):
    await funcs.clean_table(async_session, CompanyModel)
    await async_session.commit()
    uow = UnitOfWork()
    with pytest.raises(Exception):
        async with uow:
            await uow.companies.add(**company_data)
            raise Exception

    db_company = await funcs.get_item(async_session, CompanyModel, company_data["id"])
    assert db_company is None
