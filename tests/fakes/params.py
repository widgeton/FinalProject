from contextlib import nullcontext

from sqlalchemy.exc import CompileError, NoResultFound, IntegrityError
import pytest

from fakes.data import COMPANIES, USERS, NO_ID_USER

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
