from api.v1.auth.services import hash


def test_hash():
    password = "password"
    hashed_password: str = hash.get_password_hash(password)
    assert hash.verify_password(password, hashed_password)
