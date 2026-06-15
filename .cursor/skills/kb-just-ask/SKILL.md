---
name: kb-just-ask
description: WeRSS 知识库全能管家。直接提问即可，自动路由到 kb-query、kb-ingest、kb-lint、kb-sync 等技能。Use as the default entry point for any WeRSS KB question or operation.
---

# kb-just-ask 全能管家

## Overview

WeRSS 知识库的总入口。理解用户意图，路由到合适的子技能或直接回答。

## 路由规则

| 用户意图 | 路由 |
|----------|------|
| 提问、了解、解释 | → **kb-query** |
| 添加文档、更新知识 | → **kb-ingest** |
| 检查质量、巡检 | → **kb-lint** |
| 同步、拉取、推送 | → **kb-sync** |
| 不确定 | 先 kb-query，发现缺口再建议 kb-ingest |

## 启动流程

1. 搜索 `KB-META.md` 定位 `we-mp-rss-kb/`
2. 读取 `index.md` 了解当前知识库状态
3. 理解用户问题
4. 执行对应子技能或直接回答

## 快速参考

| 我想… | 说… |
|-------|-----|
| 了解采集流程 | "微信公众号是怎么采集的？" |
| 添加新文档 | "摄入 docs/xxx.md 到知识库" |
| 检查健康度 | "巡检知识库" |
| 同步更新 | "kb-sync pull" |
| 查 API | "RSS 订阅的 API 路径是什么？" |
| 查实体 | "Feed 表有哪些字段？" |

## 交互原则

- 减少非必要询问，能自动发现 KB 路径就不问
- 中文回答，技术术语保留英文
- 回答后提示用户是否需要沉淀到 `queries/`

## 知识库位置

默认：`we-mp-rss-kb/`（与 we-mp-rss 代码仓同级目录内）
