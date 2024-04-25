from fastapi import FastAPI

from api import router
from config import settings


def create_fast_api_app():
    if settings.MODE == 'PROD':
        _app = FastAPI(
            docs_url=None,
            redoc_url=None,
        )
    else:
        _app = FastAPI()

    _app.include_router(router, prefix='/api')
    return _app


app = create_fast_api_app()
