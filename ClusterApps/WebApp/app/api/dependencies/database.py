from typing import Callable, Type, AsyncGenerator

import aiomysql
from aiomysql.pool import Pool
from starlette.requests import Request
from fastapi import Depends

from app.db.repositories.base_repository import BaseRepository



def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


def get_repository(reqpo_type: Type[BaseRepository]) -> Callable:
    async def _get_repo(
        pool: Pool = Depends(_get_db_pool)
    ) -> AsyncGenerator[BaseRepository, None]:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                yield reqpo_type(cur=cur)
            await conn.commit()
                
    return _get_repo