from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "cloud_computing_logger" # TODO: Make it dynamic
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s [%(thread)d - %(threadName)s] in %(module)s - %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default'
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': 'app/Logs/logs.log',
            'filename': '/usr/src/app/app/Logs/logs.log',
            'formatter': 'default',
            'maxBytes': 1000000,
            'backupCount': 10,
            "level": LOG_LEVEL,
        }
    }
    loggers = {
        "spm_logger": {
            "handlers": ["default", "logfile"],
            "level": LOG_LEVEL
        },
    }