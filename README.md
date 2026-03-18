# 事咚咚 (Dida)

> 管理个人待办事项的 CLI 工具 —— 为事咚咚智能体提供底层能力

## 产品定位

> **在你最自然的地方，用最自然的方式，管理你要做的事**

### 我们解决什么问题

| 痛点 | 描述 |
|------|------|
| 记不住 | 说过的话、答应的事转头就忘 |
| 懒得记 | 专门的 todo app 太重，打开步骤多 |
| 易遗漏 | 任务到期了才想起，或者根本没想起 |
| 难追踪 | 想知道"今天要做什么"要到处翻 |
| 不连贯 | 聊天中说要做的事，得手动复制到 todo app |

### 核心价值

- **零摩擦**：记录一个任务 ≤ 5 秒
- **不遗漏**：到期主动提醒
- **心有数**：随时随地问，立即知道要做什么
- **可信赖**：它记住的，就是你要做的

### 我们不做什么

| 不做 | 原因 |
|------|------|
| 复杂项目管理 | 超出个人日常范畴，交给专业工具 |
| 多人协作 | 专注个人事务 |
| 复杂依赖关系 | 保持简单，"今天要做什么"就够了 |
| 精密时间块规划 | 番茄钟、日历视图交给专业 app |

---

## 安装

```bash
pip install dida-cli
```

## 快速开始

```bash
# 初始化
dida init

# 记录待办
dida add "给妈妈打电话"
dida add "明天下午三点开会" --due "2026-03-16 15:00"
dida add "周五前把报告写完" --due "2026-03-14" --priority high

# 列出待办
dida ls

# 标记完成
dida done 1

# 删除
dida delete 1
```

## 命令

| 命令 | 说明 |
|------|------|
| `dida init` | 初始化数据库 |
| `dida add` | 创建待办 |
| `dida ls` | 列出待办 |
| `dida get` | 获取详情 |
| `dida done` | 标记完成 |
| `dida undo` | 取消完成 |
| `dida update` | 更新待办 |
| `dida delete` | 删除待办 |
| `dida search` | 搜索待办 |
| `dida stats` | 统计信息 |

## 数据存储

```
~/.dida/dida.db
```

## 开发

```bash
# 克隆
git clone https://github.com/gudong/dida-cli.git
cd dida-cli

# 安装依赖
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# 运行测试
pytest
```

## License

MIT
