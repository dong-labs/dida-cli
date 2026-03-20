"""导入命令"""
import json
import typer
from rich.console import Console
from dong.io import ImporterRegistry
from dida.importer import DidaImporter

console = Console()

def import_data(file: str = typer.Option(..., "-f", "--file"), merge: bool = typer.Option(False, "--merge"), dry_run: bool = typer.Option(False, "--dry-run")):
    if not ImporterRegistry.get("dida"):
        ImporterRegistry.register(DidaImporter())
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        console.print(f"❌ 文件不存在: {file}", style="red")
        raise typer.Exit(1)
    
    if isinstance(data, dict) and "dida" in data:
        data = data["dida"]
    
    importer = ImporterRegistry.get("dida")
    is_valid, error_msg = importer.validate(data)
    if not is_valid:
        console.print(f"❌ 数据验证失败: {error_msg}", style="red")
        raise typer.Exit(1)
    
    if dry_run:
        console.print(f"\n📋 预览: 将导入 {len(data)} 条待办数据\n")
        return
    
    result = importer.import_data(data, merge=merge)
    mode = "合并" if merge else "替换"
    console.print(f"\n✅ 导入完成（{mode}模式）\n", style="green")
    console.print(f"导入成功: {result['imported']}  跳过: {result['skipped']}  总计: {result['total']}")
