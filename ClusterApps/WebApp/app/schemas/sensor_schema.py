import datetime
from typing import List, Optional
from pydantic import BaseModel, validator



class Confidance(BaseModel):
    # id: Optional[int]
    # sensor_data_id: Optional[int]
    animal_name: str
    confidance_ratio: int
    
    @validator('confidance_ratio', pre=True)
    def ratio_is_not_int(cls, v):
        if not isinstance(v, int):
            return int(float(v) * 100)
        return v
        
    
class SensorData(BaseModel):
    image_name: str
    detected_at: datetime.datetime
    created_at: Optional[datetime.datetime]
    ulpdated_at: Optional[datetime.datetime]
    confidances: List[Confidance]