import logging
from typing import List
import asyncio
from aiomysql.cursors import Cursor

from app.Configs.app_variables import TABLE_CONDIDANCE, TABLE_SENSOR
# from app.db.repositories.base_repo import BaseRepository
from app.db.repositories.base_repository import BaseRepository, MySQLQueryBuilder
from app.schemas.sensor_schema import SensorData, Confidance

# INSERT_SENSOR_DATA = """
# INSERT INTO sensor_data (image_name, detected_at)
# VALUES (%s, %s)
# """

# INSERT_CONFIDANCE_DATA = """
# INSERT INTO confidance (animal_name, confidance_ratio, sensor_data_id)
# VALUES (%s, %s, %s)
# """

# GET_ALL_SENSOR_DATA = """
# SELECT * FROM sensor_data
# """

# class SensorRepository(BaseRepository):
#     async def insert_sensor_data(self, image_name: str, detected_at: str) -> int:
#         sensor_id = await self.save(
#             INSERT_SENSOR_DATA,
#             [image_name, detected_at]
#         )
#         return sensor_id
        
#     async def insert_confidance_data(self, animale_name:str, confidance_ratio: int, sensor_id: int):
#         await self.save(
#             INSERT_CONFIDANCE_DATA,
#             [animale_name, confidance_ratio, sensor_id]
#         )
        
#     async def get_all_data(self):
#         sensor_data = await self.fetch_all(GET_ALL_SENSOR_DATA)
#         print(f'Sensor')
#         print(sensor_data)

class SensorRepository(BaseRepository):
    
    def __init__(self, cur: Cursor) -> None:
        super().__init__(cur)
        self.sensor_table = TABLE_SENSOR
        self._sensor_table_cols = ['image_name', 'detected_at']
        self.confidance_table = TABLE_CONDIDANCE
        self._confidance_talble_cols = ['animal_name', 'confidance_ratio', 'sensor_data_id']
        self._query_builder = MySQLQueryBuilder()
        
    async def save_sensor_data(self, data: SensorData) -> None:
        sensor_id = await self.save(
            self._query_builder.insert(table=self.sensor_table, columns=self._sensor_table_cols).query(),
            [data.image_name, data.detected_at.strftime(('%Y-%m-%d %H:%M:%S'))])
        
        conf_query = self._query_builder.insert(table=self.confidance_table,
                                                columns=self._confidance_talble_cols).query()
        
        conf_data = [(conf.animal_name, conf.confidance_ratio, sensor_id) for conf in data.confidances]
        await self.save_many(conf_query, conf_data)

        
    async def get_sensor_data(self, limit:int=10) -> List[SensorData]:
        sensor_data_list = []
        data_list = await self.fetch_all(
            query=self._query_builder
            .fetch(table=self.sensor_table)
            .order_by("detected_at", desc=True)
            .limit(limit).query())
        
        for data in data_list:
            query = self._query_builder.fetch(table=self.confidance_table).where(f"sensor_data_id=%s").query()
            cons = await self.fetch_all(query, [data.get('id'), ])
            
            sensor_data_list.append(SensorData(**data, confidances=cons))
            
        return sensor_data_list
