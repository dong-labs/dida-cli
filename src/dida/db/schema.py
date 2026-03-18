"""数据库 Schema 定义和版本管理

继承 dong.db.SchemaManager，管理 dida-cli 的数据库 schema。
"""

from dong.db import SchemaManager
from .connection import DidaDatabase

SCHEMA_VERSION = "1.0.0"


class DidaSchemaManager(SchemaManager):
    """待咚咚 Schema 管理器"""

    def __init__(self):
        super().__init__(
            db_class=DidaDatabase,
            current_version=SCHEMA_VERSION
        )

    def init_schema(self) -> None:
        self._create_todos_table()
        self._create_indexes()

    def _create_todos_table(self) -> None:
        with DidaDatabase.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    priority TEXT DEFAULT 'medium',
                    due_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    note TEXT
                )
            """)

    def _create_indexes(self) -> None:
        with DidaDatabase.get_cursor() as cur:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_todos_due_date ON todos(due_date)")


# 兼容性函数
def get_schema_version() -> str | None:
    return DidaSchemaManager().get_stored_version()

def set_schema_version(version: str) -> None:
    DidaDatabase.set_meta(DidaSchemaManager.VERSION_KEY, version)

def is_initialized() -> bool:
    return DidaSchemaManager().is_initialized()

def init_database() -> None:
    schema = DidaSchemaManager()
    if not schema.is_initialized():
        schema.initialize()
