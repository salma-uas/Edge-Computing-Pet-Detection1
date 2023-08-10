import logging
from typing import Callable
from fastapi import FastAPI

from app.helpers import file_helper
from logging.config import dictConfig
from app.db.events import connect_to_db, close_conneciton
from app.db import get_minio_conn
from app.Configs.app_variables import MINIO_ANIMAL_BUCKET



CLOUD_LOGGER = logging.getLogger("cloud_computing_logger")


class AppConfig():
    
    def __init__(self, app=FastAPI) -> None:
        self.app = app
    
    def configure_router(self, routers: list):
        for router in routers:
            self.app.include_router(router=router)
            
    def __run_startup_event(self, log_configs) -> Callable:
        async def start_app() -> None:
            file_helper.create_log_dir()
            # dictConfig(log_configs.dict())
            
            # MINIO
            minio = get_minio_conn()
            if not minio.bucket_exists(MINIO_ANIMAL_BUCKET):
                minio.make_bucket(MINIO_ANIMAL_BUCKET)
            
            # MySQL
            await connect_to_db(app=self.app)
            
        return start_app
            
    def __run_shutdouwn_events(self) -> Callable:
        async def stop_app() -> None:
            close_conneciton(app=self.app)
            CLOUD_LOGGER.warning("Amimal Detector Server just stopped")
            
        return stop_app
        
    def configure_startup_shoudown(self, log_configs):
        self.app.add_event_handler("startup", self.__run_startup_event(log_configs=log_configs))
        self.app.add_event_handler("shutdown", self.__run_shutdouwn_events())
        
    # async def configure_startup_shoudown(self, log_configs):
        
    #     @self.app.on_event('startup')
    #     async def startup_event():
    #         file_helper.create_log_dir()
    #         dictConfig(log_configs.dict())
    #         await connect_to_db()
            
    #         CLOUD_LOGGER.info("Animal detectoin webapp started running....")
            
    #     @self.app.on_event("shutdown")
    #     async def shutdown_event():
    #         await close_conneciton()
    #         CLOUD_LOGGER.warning("Amimal Detector Server just stopped")
    
