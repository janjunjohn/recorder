from fastapi import APIRouter

import user_routers
import task_routers
import record_routers


router = APIRouter()
router.include_router(user_routers.router)
router.include_router(task_routers.router)
router.include_router(record_routers.router)
