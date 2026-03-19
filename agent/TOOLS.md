# TOOLS.md - 工具箱

我的核心工具是 `dong-dida` CLI。

## 安装

```bash
pipx install dida-cli
```

## 命令列表

### 初始化

```bash
dong-dida init
```

### 创建待办

```bash
dong-dida add "完成项目报告"
dong-dida add "重要会议" --due "2026-03-20" --priority high
dong-dida add "开发任务" --tags "工作,开发"
```

### 列出待办

```bash
dong-dida ls                    # 列出所有待办
dong-dida ls --limit 50         # 指定数量
dong-dida ls --completed        # 只看已完成
dong-dida ls --priority high    # 按优先级筛选
dong-dida ls --tag "工作"       # 按标签筛选
```

### 搜索待办

```bash
dong-dida search "关键词"
dong-dida search "报告" --limit 10
```

### 获取详情

```bash
dong-dida get 123               # 获取待办详情
```

### 更新待办

```bash
dong-dida update 123 --content "更新内容"
dong-dida update 123 --due "2026-03-25"
dong-dida update 123 --priority critical
```

### 标记完成

```bash
dong-dida done 123              # 标记完成
dong-dida undo 123              # 取消完成
```

### 删除待办

```bash
dong-dida delete 123 --force    # 删除待办
```

### 查看标签

```bash
dong-dida tags                  # 列出所有标签及数量
```

### 统计信息

```bash
dong-dida stats                 # 统计待办数量、完成情况、优先级分布
```

## JSON 输出

所有命令支持 JSON 输出，方便 AI 解析：

```bash
dong-dida add "xxx"
dong-dida ls
dong-dida search "关键词"
dong-dida stats
```

## 数据库

数据存储在 `~/.dong/dida.db`

---

*✅ 待办不遗漏，事事有着落*
