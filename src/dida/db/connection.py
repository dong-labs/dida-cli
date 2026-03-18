"""数据库连接管理模块

继承 dong.db.Database，提供 dida-cli 专用数据库访问。
"""

import sqlite3
from typing import Iterator
from contextlib import contextmanager

from dong.db import Database as DongDatabase


class DidaDatabase(DongDatabase):
    """待咚咚数据库类 - 继承自 dong.db.Database

    数据库路径: ~/.dong/dida.db
    """

    @classmethod
    def get_name(cls) -> str:
        return "dida"


# 兼容性函数
def get_connection(db_path=None):
    return DidaDatabase.get_connection()

def close_connection():
    DidaDatabase.close_connection()

@contextmanager
def get_cursor() -> Iterator[sqlite3.Cursor]:
    with DidaDatabase.get_cursor() as cur:
        yield cur

def get_db_path():
    return DidaDatabase.get_db_path()

# init_db 作为 init_database 的别名（向后兼容）
# 延迟导入避免循环依赖
def init_db():
    from .schema import init_database
    return init_database()
