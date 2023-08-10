
from fastapi import APIRouter

from .sensor_data import router as sensor_data


router = APIRouter()
router.include_router(router=sensor_data, prefix="/api", tags=['api'])