---
name: kb-query
description: 基于 we-mp-rss-kb LLM-Wiki 知识库回答用户问题。读取 Wiki 页面综合回答，有价值的结果沉淀到 queries/。Use when asking questions about WeRSS architecture, features, or implementation.
---

# kb-query 知识库查询

## Overview

基于 L2 Wiki 层回答用户问题。好答案写回 Wiki，不消失在聊天历史。

## 前置条件

1. 搜索 `KB-META.md` 定位知识库
2. 读取 `index.md` 定位主题

## 查询流程

### Phase 1: 定位

按问题类型选择目录：

| 问题类型 | 优先目录 |
|----------|----------|
| 业务/功能 | `concepts/` |
| 数据结构 | `entities/` |
| 代码实现 | `code/modules/`、`code/classes/` |
| 历史设计 | `sources/` |
| 已有问答 | `queries/` |

### Phase 2: 综合回答

1. 读取相关 Wiki 页面
2. 信息不足时 → 回查代码仓（只读）或标注 `[待补充]`
3. **冲突时优先采纳代码仓**

### Phase 3: 沉淀（可选）

若答案有长期价值：
- 写入 `queries/YYYY-MM-DD-{主题}.md`
- 更新 `log.md`

## 输出格式

- 中文回答，技术术语保留英文
- 引用 Wiki 页面时用 `[[页面名]]`
- 引用代码时用路径格式

## 禁止

- ❌ 不查 Wiki 直接凭记忆回答
- ❌ 编造 Wiki 中不存在且代码中找不到的信息
