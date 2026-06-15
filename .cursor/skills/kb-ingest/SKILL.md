---
name: kb-ingest
description: 摄入新材料到 we-mp-rss-kb LLM-Wiki 知识库。用户提供文档路径、代码变更说明或主题时，读取 L1 源、更新 Wiki 页面、维护交叉引用与 index。Use when adding documents, code changes, or new topics to the knowledge base.
---

# kb-ingest 知识库摄入

## Overview

将 L1 原始材料（文档、代码、用户描述）编译进 L2 Wiki 层。遵循 `we-mp-rss-kb/CLAUDE.md` 的 Ingest 流程。

## 前置条件

1. 全局搜索 `KB-META.md` 定位知识库根目录
2. 读取 `KB-META.md` 获取路径配置
3. 读取 `CLAUDE.md` 确认工作规范

## Hard Gates

| # | 检查项 | 不通过行为 |
|---|--------|-----------|
| 1 | 找到 KB-META.md | 询问用户知识库路径 |
| 2 | L1 源可读 | 报告无法读取的文件 |
| 3 | 不修改 L1 源 | 只读 docs/ 和代码仓 |

## 摄入流程

### Phase 1: 读取源材料

- 用户提供：文件路径、目录、或粘贴内容
- 读取 L1 源，提取：实体、概念、模块关系、关键决策

### Phase 2: 创建/更新摘要

- 在 `sources/` 创建摘要页（Frontmatter 含 `source_file`）
- 摘要写**结论**，不复制全文

### Phase 3: 更新 Wiki 页面

按影响范围更新：
- `entities/` — 新实体或字段变更
- `concepts/` — 新业务/技术概念
- `code/modules/` — 模块结构变化
- `code/classes/` — 核心类详情（按需）

每页补充 `[[双向链接]]`。

### Phase 4: 更新索引与日志

1. 更新 `index.md` 统计与导航
2. 在 `log.md` 追加记录（日期、变更页面、摘要）

## 输出

向用户报告：
- 新建/更新了哪些页面
- 发现了哪些 `[待补充]` 缺口
- 建议的下一步 Lint 或 Query

## 禁止

- ❌ 修改 `../docs/` 或代码仓
- ❌ 编造不存在的类/字段
- ❌ 跳过 log.md 记录
