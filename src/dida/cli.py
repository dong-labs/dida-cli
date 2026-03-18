"""CLI 主入口

使用 Typer 构建命令行接口，使用 dong-core 的 json_output 装饰器。
"""

import typer
from datetime import datetime
from dong import json_output, ValidationError, NotFoundError

from . import __version__
from .db.connection import init_db, get_connection
from .const import DB_PATH, PRIORITIES

app = typer.Typer(
    name="dida",
    help=f"事咚咚 - 个人待办管理 CLI (v{__version__})",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def main_callback(
    version: bool = typer.Option(False, "--version", "-v", help="显示版本"),
) -> None:
    """主回调"""
    if version:
        typer.echo(f"dida {__version__}")
        raise typer.Exit()


@app.command()
@json_output
def init():
    """初始化数据库"""
    init_db()
    return {
        "message": "数据库初始化成功",
        "db_path": str(DB_PATH)
    }


@app.command()
@json_output
def add(
    content: str = typer.Argument(..., help="待办内容"),
    due: str = typer.Option(None, "--due", "-d", help="截止时间 (YYYY-MM-DD HH:MM)"),
    priority: str = typer.Option("medium", "--priority", "-p",
                                   help=f"优先级: {','.join(PRIORITIES)}"),
    note: str = typer.Option(None, "--note", "-n", help="备注"),
):
    """创建待办"""
    if not content or not content.strip():
        raise ValidationError("content", "待办内容不能为空")

    if priority not in PRIORITIES:
        raise ValidationError("priority", f"无效的优先级: {priority}")

    with get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute(
            """
            INSERT INTO todos (content, due_date, priority, note, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (content.strip(), due, priority, note, now, now)
        )
        todo_id = cursor.lastrowid

    return {"id": todo_id, "content": content, "priority": priority}


@app.command()
@json_output
def ls(
    limit: int = typer.Option(20, "--limit", "-l", help="显示数量"),
    completed: bool = typer.Option(None, "--completed", help="按完成状态筛选"),
    priority: str = typer.Option(None, "--priority", "-p", help="按优先级筛选"),
):
    """列出待办"""
    with get_connection() as conn:
        cursor = conn.cursor()

        conditions = []
        params = []

        if completed is not None:
            conditions.append("completed = ?")
            params.append(1 if completed else 0)

        if priority:
            conditions.append("priority = ?")
            params.append(priority)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        params.append(limit)

        cursor.execute(
            f"""
            SELECT id, content, completed, priority, due_date, created_at, note
            FROM todos
            WHERE {where_clause}
            ORDER BY completed ASC, created_at DESC
            LIMIT ?
            """,
            params
        )
        rows = cursor.fetchall()

    todos = [dict(row) for row in rows]
    return {"todos": todos, "total": len(todos)}


@app.command()
@json_output
def get(
    todo_id: int = typer.Argument(..., help="待办 ID"),
):
    """获取待办详情"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM todos WHERE id = ?",
            (todo_id,)
        )
        row = cursor.fetchone()

    if not row:
        raise NotFoundError("Todo", todo_id, message=f"未找到 ID 为 {todo_id} 的待办")

    return dict(row)


@app.command()
@json_output
def done(
    todo_id: int = typer.Argument(..., help="待办 ID"),
):
    """标记完成"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise NotFoundError("Todo", todo_id)

        now = datetime.now().isoformat()
        cursor.execute(
            "UPDATE todos SET completed = 1, updated_at = ? WHERE id = ?",
            (now, todo_id)
        )

    return {"id": todo_id, "completed": True}


@app.command()
@json_output
def undo(
    todo_id: int = typer.Argument(..., help="待办 ID"),
):
    """取消完成"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise NotFoundError("Todo", todo_id)

        now = datetime.now().isoformat()
        cursor.execute(
            "UPDATE todos SET completed = 0, updated_at = ? WHERE id = ?",
            (now, todo_id)
        )

    return {"id": todo_id, "completed": False}


@app.command()
@json_output
def update(
    todo_id: int = typer.Argument(..., help="待办 ID"),
    content: str = typer.Option(None, "--content", "-c", help="更新内容"),
    due: str = typer.Option(None, "--due", "-d", help="更新截止时间"),
    priority: str = typer.Option(None, "--priority", "-p", help="更新优先级"),
    note: str = typer.Option(None, "--note", "-n", help="更新备注"),
):
    """更新待办"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise NotFoundError("Todo", todo_id)

        updates = []
        params = []

        if content is not None:
            updates.append("content = ?")
            params.append(content.strip())
        if due is not None:
            updates.append("due_date = ?")
            params.append(due)
        if priority is not None:
            if priority not in PRIORITIES:
                raise ValidationError("priority", f"无效的优先级: {priority}")
            updates.append("priority = ?")
            params.append(priority)
        if note is not None:
            updates.append("note = ?")
            params.append(note)

        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(todo_id)

            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)

    return {"id": todo_id, "updated": True}


@app.command()
@json_output
def delete(
    todo_id: int = typer.Argument(..., help="待办 ID"),
    force: bool = typer.Option(False, "--force", "-f", help="强制删除"),
):
    """删除待办"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()

        if not row:
            raise NotFoundError("Todo", todo_id)

        if not force:
            confirm = typer.confirm(f"确定要删除待办吗？\n{row['content']}")
            if not confirm:
                return {"cancelled": True, "message": "已取消删除"}

        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

    return {"deleted": True, "id": todo_id}


@app.command()
@json_output
def search(
    keyword: str = typer.Argument(..., help="搜索关键词"),
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
):
    """搜索待办"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM todos
            WHERE content LIKE ? OR note LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (f"%{keyword}%", f"%{keyword}%", limit)
        )
        rows = cursor.fetchall()

    todos = [dict(row) for row in rows]
    return {"todos": todos, "total": len(todos), "keyword": keyword}


@app.command()
@json_output
def stats():
    """统计信息"""
    with get_connection() as conn:
        cursor = conn.cursor()

        # 总数
        cursor.execute("SELECT COUNT(*) FROM todos")
        total = cursor.fetchone()[0]

        # 已完成
        cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
        completed = cursor.fetchone()[0]

        # 未完成
        pending = total - completed

        # 按优先级统计
        cursor.execute("SELECT priority, COUNT(*) FROM todos GROUP BY priority")
        by_priority = dict(cursor.fetchall())

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "by_priority": by_priority
    }


if __name__ == "__main__":
    app()
