"""导入器模块"""
from typing import Any
from dong.io import BaseImporter, ImporterRegistry
from .db.connection import DidaDatabase

class DidaImporter(BaseImporter):
    name = "dida"
    
    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        if not isinstance(data, list):
            return False, "数据必须是列表格式"
        for i, item in enumerate(data):
            if not isinstance(item, dict) or "content" not in item:
                return False, f"第 {i+1} 条数据缺少 content 字段"
        return True, ""
    
    def import_data(self, data: list[dict[str, Any]], merge: bool = False) -> dict[str, Any]:
        with DidaDatabase.get_cursor() as cur:
            if not merge:
                cur.execute("DELETE FROM todos")
            imported, skipped = 0, 0
            for item in data:
                if merge:
                    cur.execute("SELECT id FROM todos WHERE content = ?", (item["content"],))
                    if cur.fetchone():
                        skipped += 1
                        continue
                cur.execute(
                    """INSERT INTO todos (content, completed, priority, due_date, note, tags)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (item["content"], item.get("completed", False), item.get("priority", "medium"),
                     item.get("due_date"), item.get("note"), ",".join(item.get("tags", [])))
                )
                imported += 1
            return {"imported": imported, "skipped": skipped, "total": len(data)}

ImporterRegistry.register(DidaImporter())
