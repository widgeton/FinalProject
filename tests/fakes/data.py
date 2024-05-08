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
    "Peter": {
        "id": 2,
        "email": "peter@gmail.com",
        "hashed_pass": "hashed_pass",
        "first_name": "Peter",
        "last_name": "Potter",
        "role": Roles.worker,
        "company_id": 1,
    },
    "Jack": {
        "id": 3,
        "email": "jack@gmail.com",
        "hashed_pass": "hashed_pass",
        "first_name": "Jack",
        "last_name": "Smith",
        "role": Roles.admin,
        "company_id": 1,
    },
    "George": {
        "id": 4,
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

TASKS = {
    "Auth": {
        "title": "Implement authentication",
        "description": "Some description",
        "author_id": USERS["John"]["id"],
        "charged_id": USERS["John"]["id"],
        "deadline": "2024-05-06 00:00",
        "status": "wait",
        "estimate": "48",
    },
    "Test": {
        "title": "Test",
        "description": "Some description",
        "author_id": USERS["John"]["id"],
        "charged_id": USERS["Peter"]["id"],
        "deadline": "2024-05-06 00:00",
        "status": "wait",
        "estimate": "48",
    }
}

EXPECTED_TASKS_DATA = {
    "Auth": {
        "title": "Implement authentication",
        "description": "Some description",
        "author_id": 1,
        "charged_id": 1,
        "deadline": "2024-05-06T00:00:00",
        "status": "wait",
        "estimate": "P2D",
        "id": 1
    },
    "Test": {
        "title": "Test",
        "description": "Some description",
        "author_id": 1,
        "charged_id": 2,
        "deadline": "2024-05-06T00:00:00",
        "status": "wait",
        "estimate": "P2D",
        "id": 2
    }
}
