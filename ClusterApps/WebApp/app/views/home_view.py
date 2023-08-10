import base64
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from minio import Minio

from app.Configs.app_configs import MINIO_ANIMAL_BUCKET
from app.db.repositories.sensor_repo import SensorRepository
from app.api.dependencies.database import get_repository
from app.db import get_minio_conn
from app.db.repositories.image_repo import ImageRepo


router = APIRouter()
templates = Jinja2Templates('app/templates')


@router.get("/", name="home",)
async def index(
    request: Request, sensor_repo: SensorRepository = Depends(get_repository(SensorRepository))):
    """Renders the login page"""

    data = {'request': request, 'sensor_data': await sensor_repo.get_sensor_data()}
    return templates.TemplateResponse('home.html', data)


@router.get("/get-image/{img}", name="get_image")
async def get_image(img: str, request: Request, minio_client: Minio = Depends(get_minio_conn)):
    
    image_repo = ImageRepo(minio_client=minio_client, bucket=MINIO_ANIMAL_BUCKET)
    image_data = image_repo.get_image(image_name=img)
    
    img_content = base64.b64encode(image_data).decode("utf-8")
    data = {'request': request, 'img_content': img_content}
    return templates.TemplateResponse('view_image.html', data)
