"""测试 CLI 命令"""

from click.testing import CliRunner
from shi.cli import main


def test_version() -> None:
    """测试版本号"""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_init() -> None:
    """测试初始化"""
    runner = CliRunner()
    result = runner.invoke(main, ["init"])
    assert result.exit_code == 0
