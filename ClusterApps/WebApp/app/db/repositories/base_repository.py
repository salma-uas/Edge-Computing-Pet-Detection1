from string import Template
from typing import Any, Sequence, Tuple, List, Union
from aiomysql.cursors import Cursor
from abc import ABC, abstractmethod

_INSERT_DATA = Template(
    "INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ($VALUES)"
)

_FETCH_ALL = Template(
    "SELECT * FROM $TABLE_NAME"
)

_FETCH_COLS = Template(
    "SELECT $COLUMNS FROM $TABLE"
)

_WHARE = Template("WHERE $CLAUSE")


class QueryBuilderBase(ABC):
    
    @abstractmethod
    def query():
        ...
        
    @abstractmethod
    def insert():
        ...
        
    @abstractmethod
    def update():
        ...
        
    @abstractmethod
    def delete():
        ...
        
    @abstractmethod
    def fetch():
        ...
        
    @abstractmethod
    def limit():
        ...

class BaseRepository:
    def __init__(self, cur: Cursor) -> None:
        self._cur = cur
        
    @property
    def cursor(self) -> Cursor:
        self._cur
        
    async def save(self, query: str, *query_params: Any) -> int:
        await self._cur.execute(query, *query_params)
        created_id = self._cur.lastrowid
        
        return created_id
        
    async def save_many(self, query: str, queryparams: Sequence[Tuple[Any, ...]]) -> None:
        await self._cur.executemany(query, queryparams)
        
    async def fetch_one(self, query: str, *queryparams: Any) -> Any:
        await self._cur.execute(query, *queryparams)
        return await self._cur.fetchone()
    
    async def fetch_all(self, query: str, *queryparams: Any) -> Any:
        await self._cur.execute(query, *queryparams)
        return await self._cur.fetchall()


class MySQLQueryBuilder(QueryBuilderBase):
    
    def __init__(self) -> None:
        self._insert_template = _INSERT_DATA
        self._fetch_all_template = _FETCH_ALL
        self._fetch_cols = _FETCH_COLS
        self._whare = _WHARE
        self._query = ""
        
    def query(self):
        return self._query
    
    def insert(self, table: str, columns: List[str]):
        
        value_place = ", ".join(["%s" for _ in range(len(columns))])
        columns = ", ".join(columns)
        
        self._query = self._insert_template.substitute(TABLE_NAME=table, COLUMNS=columns, VALUES=value_place)
        
        return self
    
    def update(self):
        pass
    
    def delete(self):
        pass
    
    def fetch(self, table: str, columns: List[str] = None):
        
        cloumns = " *" if not columns else ", ".join[columns]
        self._query = self._fetch_cols.substitute(COLUMNS=cloumns, TABLE=table)
        
        return self
    
    def where(self, sql_condition: str):
        self._query += f" {self._whare.substitute(CLAUSE=sql_condition)}"
        
        return self
    
    def order_by(self, order_by: Union[str, List[str]], desc: bool = False):
        order_by = order_by if not isinstance(order_by, list) else ", ".join(order_by)
        sort = "ASC" if not desc else "DESC"
        
        self._query += f" ORDER BY {order_by} {sort}"
        return self
    
    def limit(self, limit: int):
        self._query += f" LIMIT {int(limit)}"
        
        return self