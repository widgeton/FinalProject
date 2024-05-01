from models.field_types import Roles

COMPANIES = {
    "Google": {
        "id": 1,
        "name": "Google"
    },
    "Microsoft": {
        "id": 2,
        "name": "Microsoft"
    },
    "Apple": {
        "id": 3,
        "name": "Apple"
    },
}

USERS = {
    "John": {
        "id": 1,
        "email": "john@gmail.com",
        "hashed_pass": "hashed_pass",
        "first_name": "John",
        "last_name": "Doe",
        "role": Roles.admin,
        "company_id": 1,
    },
    "Jack": {
        "id": 2,
        "email": "jack@gmail.com",
        "hashed_pass": "hashed_pass",
        "first_name": "Jack",
        "last_name": "Smith",
        "role": Roles.admin,
        "company_id": 1,
    },
    "George": {
        "id": 3,
        "email": "george@gmail.com",
        "hashed_pass": "hashed_pass",
        "first_name": "George",
        "last_name": "Logan",
        "role": Roles.admin,
        "company_id": 2,
    },
}

NO_ID_USER = {
    key: {k: v for k, v in value.items() if k != "id" or k != "company_id"} for key, value in USERS.items()
}
