from time import sleep
from contextlib import nullcontext
from datetime import timedelta

import pytest

from api.v1.auth.services import jwt
from api.v1.auth.schemas import TokenData
from api.v1.auth.exceptions import TokenDataException


@pytest.mark.parametrize(
    "data, encode_secret_key, decode_secret_key, expires, wait, expectation",
    [
        ({"sub": "data"}, "secret", "secret", timedelta(minutes=1), 0, nullcontext(TokenData(email="data"))),
        ({"sub": "data"}, "secret", "secret", timedelta(seconds=1), 2, pytest.raises(TokenDataException)),
        ({"sub": "data"}, "secret", "hack", timedelta(minutes=1), 0, pytest.raises(TokenDataException)),

    ]
)
def test_jwt(data, encode_secret_key, decode_secret_key, expires, wait, expectation):
    with expectation as exp:
        token = jwt.generate_token(data, encode_secret_key, expires)
        if wait:
            sleep(wait)
        token_data: TokenData = jwt.decode_token(token, decode_secret_key)
        assert token_data == exp
