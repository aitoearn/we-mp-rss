---
type: concept
created: 2026-06-13
updated: 2026-06-13
tags: [RSS, 输出]
---

# RSS订阅服务

## 概述

将入库的 [[Article]] 转换为 RSS/Atom/JSON/MD/TXT 格式，供 RSS 阅读器订阅。支持自定义标题、描述、封面与分页大小。

## 核心实现

| 组件 | 路径 | 职责 |
|------|------|------|
| RSS 生成器 | `core/rss.py` | 格式转换、分页、缓存 |
| RSS API | `apis/rss.py` | 对外订阅端点（无 API 前缀） |

## 订阅格式

- RSS 2.0 / Atom
- JSON Feed
- Markdown / 纯文本

## 缓存策略

- RSS 缓存目录：`data/cache/rss/`
- 正文缓存：`data/cache/content/`
- 可通过 `docs/cache-config.md` 配置缓存行为

## 相关模块

- [[apis模块]] — `feeds_router` 独立挂载，供 RSS 客户端直接访问
- [[core模块]] — RSS 生成逻辑

## 关键实体

- [[Feed]] — 每个公众号对应一条 RSS 源
- [[Article]] — RSS item 的数据来源

## 注意事项

- RSS 路由不走 JWT 认证中间件（公开订阅）
- 自定义 RSS 标题/描述/封面在 Feed 或全局配置中设置
- 分页大小影响 RSS 客户端加载体验
