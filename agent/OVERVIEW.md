# OVERVIEW.md - 事咚咚项目概览

## 项目信息

- **名称**：事咚咚 (Dida)
- **版本**：0.1.0
- **类型**：个人待办管理 CLI
- **仓库**：dida-cli

---

## 核心功能

1. **快速记录** - 一句话添加待办
2. **优先级管理** - critical/high/medium/low
3. **截止时间** - 支持 due_date
4. **状态追踪** - 完成/未完成
5. **智能搜索** - 内容和备注搜索
6. **统计分析** - 总数、完成率

---

## 技术架构

- **语言**：Python 3.11+
- **框架**：Typer
- **数据库**：SQLite (~/.dida/dida.db)
- **输出**：JSON (Agent 友好)
- **依赖**：dong-core

---

## 命令速查

```
dida init    初始化
dida add     添加待办
dida ls      列出待办
dida get     获取详情
dida done    标记完成
dida undo    取消完成
dida update  更新待办
dida delete  删除待办
dida search  搜索待办
dida stats   统计信息
```

---

## 产品边界

**做的**：
- ✅ 记录待办
- ✅ 状态追踪
- ✅ 优先级
- ✅ 截止时间
- ✅ 搜索

**不做的**：
- ❌ 项目管理
- ❌ 多人协作
- ❌ 复杂依赖
- ❌ 子任务
- ❌ 番茄钟
- ❌ 日历视图

---

*记住要做的事，滴滴答答 🕐*
