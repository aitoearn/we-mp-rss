---
name: kb-sync
description: 同步 we-mp-rss-kb 知识库：pull 远程更新，或 push 本地变更。也支持从 docs/ 和代码仓 diff 触发增量摄入。Use when syncing KB with remote git or updating from code changes.
---

# kb-sync 知识库同步

## Overview

管理知识库版本同步与增量更新。

## 模式

### Pull（使用方）

```bash
# 在知识库目录执行
git pull origin main
```

拉取远程 Wiki 更新到本地。

### Push（开发方）

1. 确认本地 Wiki 变更已完成 Lint
2. 更新 `log.md`
3. `git add we-mp-rss-kb/` → commit → push

### 增量摄入（代码/文档变更）

触发：代码仓有显著变更，或 `docs/` 新增文档。

流程：
1. `git diff` 或用户指定变更范围
2. 调用 **kb-ingest** 技能更新受影响页面
3. 运行 **kb-lint** 确认健康度
4. 更新 `log.md`

## 建议节奏

| 源 | 频率 |
|----|------|
| docs/ 新文档 | 按需（kb-ingest） |
| 代码结构变更 | 每周或 PR 合并后 |
| 全量 Lint | 每月或 ≥10 页变更后 |

## Hard Gates

- Push 前必须更新 `log.md`
- ≥10 页变更建议先跑 kb-lint

## 路径

- 知识库：`we-mp-rss-kb/`（项目内）
- 代码仓：`..`（we-mp-rss 根目录）
- 文档源：`../docs/`
