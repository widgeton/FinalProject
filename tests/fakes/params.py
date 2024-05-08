from contextlib import nullcontext

from sqlalchemy.exc import CompileError, NoResultFound, IntegrityError
import pytest

from schemas import DepartmentInDB
from fakes.data import (
    COMPANIES,
    USERS,
    NO_ID_USER,
    DEPARTMENTS,
    CHANGED_DEPARTMENTS,
    TASKS,
    EXPECTED_TASKS_DATA
)

ADD_COMPANY_PARAMS = [
    (COMPANIES["Google"], nullcontext()),
    (COMPANIES["Apple"], nullcontext()),
    ({"...": "gibberish"}, pytest.raises(CompileError)),
]

GET_COMPANY_PARAMS = [
    (COMPANIES["Google"], {"id": COMPANIES["Google"]["id"]}, nullcontext()),
    (COMPANIES["Apple"], {"id": 10}, pytest.raises(AssertionError, match="Got None object")),
]

UPDATE_COMPANY_PARAMS = [
    (COMPANIES["Google"], COMPANIES["Google"]["id"], {"name": "Google Inc"}, nullcontext()),
    (COMPANIES["Apple"], 10, {"name": "Apple Inc"}, pytest.raises(NoResultFound)),
    (COMPANIES["Microsoft"], COMPANIES["Microsoft"]["id"], {"...": "gibberish"}, pytest.raises(CompileError)),
]

ADD_USER_PARAMS = [
    (USERS["John"], COMPANIES["Google"], nullcontext()),
    (USERS["John"], COMPANIES["Apple"], pytest.raises(IntegrityError)),
    ({"...": "gibberish"}, COMPANIES["Google"], pytest.raises(CompileError)),
]

ADD_UNIQUE_EMAIL_USER_PARAMS = [
    (USERS["John"], USERS["Jack"], COMPANIES["Google"], nullcontext()),
    (NO_ID_USER["Jack"], USERS["Jack"], COMPANIES["Google"], pytest.raises(IntegrityError)),
]

GET_USER_PARAMS = [
    (USERS["John"], COMPANIES["Google"], {"email": USERS["John"]["email"]}, nullcontext()),
    (USERS["John"], COMPANIES["Google"], {"email": USERS["George"]["email"]},
     pytest.raises(AssertionError, match="Got None object")),
]

UPDATE_USER_PARAMS = [
    (USERS["John"], COMPANIES["Google"], USERS["John"]["id"], {"first_name": "Johnny"}, nullcontext()),
    (USERS["John"], COMPANIES["Google"], 10, {"first_name": "Johnny"}, pytest.raises(NoResultFound)),
    (USERS["John"], COMPANIES["Google"], USERS["John"]["id"], {"...": "gibberish"}, pytest.raises(CompileError)),
]

UPDATE_DEPARTMENT_PARAMS = [
    (
        COMPANIES["Google"],
        DEPARTMENTS.values(),
        {
            "id_": DEPARTMENTS["Test"]["id"],
            "path": f"{DEPARTMENTS['Development']['path']}.{DEPARTMENTS['Development']['id']}",
            "old_path": DEPARTMENTS["Test"]["path"]
        },
        [DepartmentInDB.model_validate(i, from_attributes=True) for i in CHANGED_DEPARTMENTS.values()]
    ),
    (
        COMPANIES["Google"],
        [DEPARTMENTS["Legal"]],
        {
            "id_": DEPARTMENTS["Legal"]["id"],
            "name": "Illegal"
        },
        [DepartmentInDB(
            id=DEPARTMENTS["Legal"]["id"],
            name="Illegal",
            company_id=DEPARTMENTS["Legal"]["company_id"],
            path=DEPARTMENTS["Legal"]["path"]
        )]
    )
]

_right_data = TASKS["Auth"]

_auth = TASKS["Auth"].copy()
_auth["charged_id"] = 78
_nonexistent_id = _auth

_auth = TASKS["Auth"].copy()
_auth["charged_id"] = USERS["George"]["id"]
_another_company_user_id = _auth

CREATE_TASK_PARAMS = (
    (_right_data, EXPECTED_TASKS_DATA["Auth"]),
    (_nonexistent_id, {'detail': 'Wrong user reference.'}),
    (_another_company_user_id, {'detail': 'User is not in admin company.'})
)

_expected = EXPECTED_TASKS_DATA["Test"].copy()
_expected["title"] = "Testing"

UPDATE_TASK_PARAMS = (
    (_expected["id"], {"title": "Testing"}, _expected),
    (4, {"title": "Testing"}, {"detail": "Wrong task reference."})
)
