import logging
import aiomysql
from fastapi import FastAPI

from app.Configs.server_configs import SETTINGS
from app.db import sql_db_initilizer


async def connect_to_db(app: FastAPI) -> None:
    logging.info("Connecting to the database")
    
    pool = await aiomysql.create_pool(
        host=str(SETTINGS.mysql_host), port=int(SETTINGS.mysql_port),
        user=str(SETTINGS.mysql_user), password=str(SETTINGS.mysql_password),
        db=str(SETTINGS.mysql_db_name), loop=None, autocommit=False
    )
    logging.info("MySql connenction established")
    await sql_db_initilizer.initialize_database(pool)
    app.state.pool = pool
    logging.info("Mysql Table Initialized")
    return pool
    
def close_conneciton(app: FastAPI) -> None:
    logging.info("Closing DB connection")
    
    app.state.pool.close()
    logging.info("Db connecion closed")
    
