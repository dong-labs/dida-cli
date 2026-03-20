"""导出命令"""
import typer
from rich.console import Console
from dong.io import ExporterRegistry
from dida.exporter import DidaExporter

console = Console()

def export(output: str = typer.Option("dida.json", "-o", "--output"), format: str = typer.Option("json", "-f", "--format")):
    if not ExporterRegistry.get("dida"):
        ExporterRegistry.register(DidaExporter())
    exporter = ExporterRegistry.get("dida")
    data = exporter.to_json() if format == "json" else exporter.to_markdown()
    with open(output, "w", encoding="utf-8") as f:
        f.write(data)
    console.print(f"✅ 已导出 {len(exporter.fetch_all())} 条待办数据到 {output}", style="green")
