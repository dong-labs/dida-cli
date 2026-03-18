# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Project: dida CLI

**待咚咚 (Dida)** - 个人待办管理的 CLI 工具

### 核心设计原则

1. **Agent First, Human Second** - 所有命令设计优先考虑 AI 调用
2. **极简主义** - 只做核心功能，不做复杂报表
3. **确定性输出** - 所有命令返回 JSON
4. **边界清晰** - 明确功能边界

### 技术栈

- **语言**: Python 3.11+
- **CLI 框架**: Typer
- **数据库**: SQLite (单文件 `~/.dida/dida.db`)
- **输出**: 所有命令返回 JSON

### 安装与运行

```bash
# 开发模式安装
pip install -e .

# 运行
dida init
dida ls
```

### 项目边界

**做的：** 待办事项、状态管理、优先级
**不做的：** 不做团队协作、不做提醒功能
