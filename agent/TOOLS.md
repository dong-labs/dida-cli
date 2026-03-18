# TOOLS.md - 事咚咚的工具箱

## 命令行工具 (CLI)

### 安装
```bash
pip install dida-cli
```

### 基础命令
```bash
dida init              # 初始化
dida add "内容"        # 添加待办
dida add "内容" -p high  # 指定优先级
dida add "内容" -d "2026-03-16 15:00"  # 指定截止时间
dida ls                # 列出所有
dida ls -p high        # 按优先级筛选
dida get 1             # 获取单条
dida done 1            # 标记完成
dida undo 1            # 取消完成
dida update 1 -c "新内容"  # 更新
dida delete 1          # 删除
dida search "关键词"   # 搜索
dida stats             # 统计
```

---

## 数据位置

```
~/.dida/dida.db
```

备份：直接复制这个文件

---

## 优先级

| 级别 | 说明 |
|------|------|
| critical | 紧急重要 |
| high | 重要 |
| medium | 普通（默认） |
| low | 不急 |

---

## 用户意图映射

| 用户说 | 命令 |
|--------|------|
| "记一下..." | `dida add "..."` |
| "待办：..." | `dida add "..."` |
| "今天要做什么" | `dida ls` |
| "有多少待办" | `dida stats` |
| "做完了" | `dida done <id>` |
| "撤销完成" | `dida undo <id>` |
| "找关于...的" | `dida search "..."` |
| "删除这条" | `dida delete <id>` |

---

## 快捷操作

- 记任务：直接说"记一下：..."
- 查看列表：说"今天要做什么"
- 标记完成：说"做完了 [id]"
- 搜索：说"找：关键词"

---

## 任务状态

| 状态 | 说明 |
|------|------|
| 0 | 未完成 |
| 1 | 已完成 |

---

*工具齐备，随时记录 🕐*
