from typing import List
import aiomysql

from app.Configs.app_variables import TABLE_CONDIDANCE, TABLE_SENSOR


table_sql = {
    TABLE_SENSOR: f"""
        CREATE TABLE {TABLE_SENSOR} (
            id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            image_name VARCHAR(255) NOT NULL,
            detected_at timestamp NOT NULL,
            created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """,
    TABLE_CONDIDANCE: f"""
        CREATE TABLE {TABLE_CONDIDANCE} (
            id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            animal_name VARCHAR(255) NOT NULL,
            confidance_ratio INT NOT NULL,
            sensor_data_id INT NOT NULL,
            FOREIGN KEY (sensor_data_id)
                REFERENCES sensor_data (id)
                ON UPDATE RESTRICT ON DELETE CASCADE
        );
    """
}


async def get_all_talbe_names(cursor) -> List[str]:
    await cursor.execute('SHOW tables;')
    results = await cursor.fetchall()
    tables = [list(talble_info.values())[0] for talble_info in results]
    
    return tables

async def initialize_database(conn_pool):
    async with conn_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            all_tables = await get_all_talbe_names(cursor=cursor)
            
            for name, sql in table_sql.items():
                if not name in all_tables:
                    await cursor.execute(sql)