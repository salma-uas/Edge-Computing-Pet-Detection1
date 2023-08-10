
import  logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import app_version
from app.Configs.server_configs import get_settings, ALLOWED_ORIGINS
from app.Configs.app_configs import AppConfig
from app.Configs.log_cofigs import LogConfig

from app.api import router as api_router
from app.views import router as view_router


settings = get_settings()
def get_app() -> FastAPI:
    """Returns fastapi app"""
    
    app = FastAPI(
        title="WebServer to manage detected image my sensor nodes",
        description="This App will accept animal image with the detected animal \
            lmetadate and store the date into database and visualize in the frontend",
        version= app_version,
        debug=settings.debug
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"] #TODO: Change it
    )
    
    app.mount("/app/static/", 
              StaticFiles(directory="app/static"), name="static")
    
    return app


# initialize app
app = get_app()

    
# configure app
app_config = AppConfig(app=app)
app_config.configure_startup_shoudown(log_configs=LogConfig())
app_config.configure_router(routers=[api_router, view_router])
