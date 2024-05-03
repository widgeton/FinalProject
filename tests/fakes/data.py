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

DEPARTMENTS = {
    "Development": {
        "id": 1,
        "company_id": 1,
        "name": "Development",
        "path": "1"
    },
    "Backend": {
        "id": 5,
        "company_id": 1,
        "name": "Backend",
        "path": "1.5"
    },
    "Legal": {
        "id": 2,
        "company_id": 1,
        "name": "Legal",
        "path": "2"
    },
    "Test": {
        "id": 3,
        "company_id": 1,
        "name": "Test",
        "path": "1.5.3"
    },
    "Unit": {
        "id": 4,
        "company_id": 1,
        "name": "Test",
        "path": "1.5.3.4"
    },
    "E2E": {
        "id": 6,
        "company_id": 1,
        "name": "E2E",
        "path": "1.5.3.6"
    },
}

CHANGED_DEPARTMENTS = {
    "Development": {
        "id": 1,
        "company_id": 1,
        "name": "Development",
        "path": "1"
    },
    "Backend": {
        "id": 5,
        "company_id": 1,
        "name": "Backend",
        "path": "1.5"
    },
    "Legal": {
        "id": 2,
        "company_id": 1,
        "name": "Legal",
        "path": "2"
    },
    "Test": {
        "id": 3,
        "company_id": 1,
        "name": "Test",
        "path": "1.3"
    },
    "Unit": {
        "id": 4,
        "company_id": 1,
        "name": "Test",
        "path": "1.3.4"
    },
    "E2E": {
        "id": 6,
        "company_id": 1,
        "name": "E2E",
        "path": "1.3.6"
    },
}
