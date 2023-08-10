from minio import Minio
from app.Configs.server_configs import SETTINGS


def get_minio_conn() -> Minio:
    return Minio(
        f'{SETTINGS.minio_host}:{SETTINGS.minio_port}',
        access_key=SETTINGS.minio_accsess_key,
        secret_key=SETTINGS.minio_secret_key,
        secure=False
    )