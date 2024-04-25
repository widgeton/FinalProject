from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router
from config import settings


def create_fast_api_app():
    if settings.MODE == 'PROD':
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            docs_url=None,
            redoc_url=None,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
        )

    _app.include_router(router, prefix='/api')
    return _app


app = create_fast_api_app()
