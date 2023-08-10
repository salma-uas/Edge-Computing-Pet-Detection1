
import uvicorn

from app.Configs.server_configs import get_settings

APP_SETTINGS = get_settings()


if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host= APP_SETTINGS.cloud_comp_host,
        port=APP_SETTINGS.cloud_comp_port,
        log_level="info",
        reload=APP_SETTINGS.debug
    )