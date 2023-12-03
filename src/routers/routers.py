from fastapi import APIRouter

from routers import user_routers, task_routers, record_routers


router = APIRouter()
router.include_router(user_routers.router)
router.include_router(task_routers.router)
router.include_router(record_routers.router)
