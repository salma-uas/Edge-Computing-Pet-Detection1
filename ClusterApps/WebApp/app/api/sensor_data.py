from ast import literal_eval as make_tuple
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form

from fastapi import Depends
from minio import Minio

from app.schemas.sensor_schema import Confidance, SensorData
from app.db.repositories.sensor_repo import SensorRepository
from app.api.dependencies.database import get_repository
from app.db import get_minio_conn
from app.db.repositories.image_repo import ImageRepo
from app.Configs.app_configs import MINIO_ANIMAL_BUCKET

router = APIRouter()



@router.get("/", name="api_home")
async def api_home(
    sensor_repo: SensorRepository = Depends(get_repository(SensorRepository))):
    
    await sensor_repo.get_sensor_data()
    return {
        "greedings": "Helo world"
    }
    
@router.get("/sensor-data", name="api_home")
async def api_home(
    sensor_repo: SensorRepository = Depends(get_repository(SensorRepository))):
    
    data = await sensor_repo.get_sensor_data()
    return {
        "Sensor Data": data
    }  

@router.post("/", name="sensor_data")
async def sensor_data_upload(
    detected_at: datetime = Form(...),
    confidances: list = Form(...),
    image: UploadFile = File(...),
    minio_client: Minio = Depends(get_minio_conn),
    sensor_repo: SensorRepository = Depends(get_repository(SensorRepository))
    ) -> None:
    
    # from app.helpers import file_helper
    # image_path = file_helper.get_log_dir() / 'image.png'
    # async with aiofiles.open(image_path, 'wb') as wb_file:
    #         image_data = await image.read()
    #         await wb_file.write(image_data)
    #         await wb_file.flush()

    image = await image.read()
    im_name, _ = ImageRepo(minio_client=minio_client, bucket=MINIO_ANIMAL_BUCKET).upload_image(image=image)
    
    confis = []
    for confidance_data in confidances:
        animal_name, confidance = make_tuple(confidance_data)
        confis.append(Confidance(animal_name=animal_name, confidance_ratio=confidance))
        
    await sensor_repo.save_sensor_data(data=SensorData(image_name=im_name, detected_at=detected_at, confidances=confis))
    
    # sensor_id = await sensor_repo.insert_sensor_data(image_name=im_name, detected_at=datetime)
    # for confidance_data in confidances:
    #     confidance_data = make_tuple(confidance_data)
    #     animal_name, confidance = confidance_data
        
    #     await sensor_repo.insert_confidance_data(animale_name=animal_name,
    #                                              confidance_ratio=int(float(confidance) * 100),
    #                                              sensor_id=sensor_id)
    
    
    return {
        "datetime": detected_at,
        "confidances": confidances
    }


# @router.post("/upload")
# async def upload(image: UploadFile = File(...), minio_client: Minio = Depends(get_minio_conn)):
    
#     image = await image.read()
#     image_rep = ImageRepo(minio_client=minio_client, bucket=MINIO_ANIMAL_BUCKET)
#     image_rep.upload_image(image=image)
    
#     return {
#         "greedings": "Helo world"
#     }

# @router.get("/get-image")
# async def get_image(minio_client: Minio = Depends(get_minio_conn)):
    
#     image_repo = ImageRepo(minio_client=minio_client, bucket=MINIO_ANIMAL_BUCKET)
#     image_data = image_repo.get_image(image_name="9ecbbb1563784cf3ada81b0acdcc5630.jpg")
    
#     from app.helpers import file_helper
#     image_path = file_helper.get_log_dir() / 'image_from_minio.png'
#     async with aiofiles.open(image_path, 'wb') as wb_file:
#             # image_data = await image.read()
#             await wb_file.write(image_data)
#             await wb_file.flush()
            