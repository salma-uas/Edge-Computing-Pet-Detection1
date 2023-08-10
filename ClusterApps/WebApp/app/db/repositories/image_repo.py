from typing import Tuple
from minio import Minio
import io
import uuid


class ImageRepo():
    
    def __init__(self, minio_client: Minio, bucket: str) -> None:
        self.client = minio_client
        self.bucket_name = bucket
        
    def is_bucket_available(self) -> bool:
        return self.client.bucket_exists(bucket_name=self.bucket_name)
    
    @staticmethod
    def get_unique_name() -> str:
        return uuid.uuid4().hex
    
    def upload_image(self, image: bytes) -> Tuple[str, str]:
        
        result = self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=f'{self.get_unique_name()}.jpg',
            data=io.BytesIO(image),
            length=len(image),
            content_type='image/jpg'
        )
        
        return result.object_name, result.etag
    
    def get_image(self, image_name: str):
        

        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=image_name
            )
            # TODO: read the response
            print(type(response.data)) # byte
            image_byte = response.data
        finally:
            response.close()
            response.release_conn()

        return image_byte