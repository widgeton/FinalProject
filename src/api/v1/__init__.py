__all__ = (
    "router",
)

from fastapi import APIRouter

from api.v1.auth.routes import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix='/auth', tags=['Auth'])
