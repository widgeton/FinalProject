import pytest

from repositories import DepartmentRepository
from models import DepartmentModel, CompanyModel
from schemas import DepartmentInDB
import funcs
from fakes.params import UPDATE_DEPARTMENT_PARAMS
from fakes.data import DEPARTMENTS

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "company, deps, change, exp",
    UPDATE_DEPARTMENT_PARAMS
)
async def test_update_department(async_session, company, deps, change, exp):
    await funcs.clean_table(async_session, DepartmentModel)
    await funcs.clean_table(async_session, CompanyModel)
    await funcs.add_item(async_session, CompanyModel, company)
    for dep in deps:
        await funcs.add_item(async_session, DepartmentModel, dep)
    await async_session.commit()

    repo = DepartmentRepository(async_session)
    await repo.update(**change)
    await async_session.commit()

    new_deps = await funcs.get_all_items(async_session, DepartmentModel)
    new_deps = [DepartmentInDB.model_validate(i, from_attributes=True) for i in new_deps]
    assert len(new_deps) == len(exp)
    for dep in new_deps:
        assert dep in new_deps


async def test_delete_department(async_session):
    await funcs.clean_table(async_session, DepartmentModel)
    await funcs.add_item(async_session, DepartmentModel, DEPARTMENTS["Development"])
    await async_session.commit()

    repo = DepartmentRepository(async_session)
    await repo.delete(DEPARTMENTS["Development"]["id"])
    await async_session.commit()

    dep = await funcs.get_item(async_session, DepartmentModel, DEPARTMENTS["Development"]["id"])
    assert dep is None
