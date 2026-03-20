"""导出器模块"""
from typing import Any
from dong.io import BaseExporter, ExporterRegistry
from .db.connection import DidaDatabase

class DidaExporter(BaseExporter):
    name = "dida"
    
    def fetch_all(self) -> list[dict[str, Any]]:
        with DidaDatabase.get_cursor() as cur:
            cur.execute("""
                SELECT id, content, completed, priority, due_date, created_at, updated_at, note, tags
                FROM todos ORDER BY created_at DESC
            """)
            return [
                {
                    "id": row[0], "content": row[1], "completed": bool(row[2]),
                    "priority": row[3], "due_date": row[4],
                    "created_at": row[5], "updated_at": row[6],
                    "note": row[7], "tags": row[8].split(",") if row[8] else [],
                }
                for row in cur.fetchall()
            ]

ExporterRegistry.register(DidaExporter())
