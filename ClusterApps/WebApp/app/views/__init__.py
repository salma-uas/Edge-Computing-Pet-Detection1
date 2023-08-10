from fastapi import APIRouter

from .home_view import router as home_view

router = APIRouter()
router.include_router(router=home_view, tags=['views'])