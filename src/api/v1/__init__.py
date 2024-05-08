__all__ = (
    "router",
)

from fastapi import APIRouter

from api.v1.auth.routes import router as auth_router
from api.v1.structure.routes import router as structure_router
from api.v1.tasks.routes import router as tasks_router

router = APIRouter()
router.include_router(auth_router, prefix='/auth', tags=['Auth'])
router.include_router(structure_router, prefix='/structure', tags=['Structure'])
router.include_router(tasks_router, prefix='/tasks', tags=['Tasks'])
