---
type: module
created: 2026-06-13
updated: 2026-06-13
module: apis
tags: [后端, API]
---

# apis 模块

## 职责

FastAPI REST API 路由层，对外提供 HTTP 接口。

## 路由注册

在 `web.py` 中通过 `api_router`（前缀 `API_BASE`）统一挂载：

| Router | 文件 | 功能 |
|--------|------|------|
| auth | `apis/auth.py` | 登录认证 |
| user | `apis/user.py` | 用户管理 |
| article | `apis/article.py` | 文章 CRUD |
| mps | `apis/mps.py` | 公众号管理 |
| rss | `apis/rss.py` | RSS 订阅（独立 feeds_router） |
| export | `apis/export.py` | 导出 |
| message_task | `apis/message_task.py` | 消息任务 |
| cascade | `apis/cascade.py` | 级联管理 |
| config | `apis/config_management.py` | 配置管理 |
| filter_rule | `apis/filter_rule.py` | 过滤规则 |
| tags | `apis/tags.py` | 标签 |
| task_queue | `apis/task_queue.py` | 任务队列 |
| tools | `apis/tools.py` | 工具接口 |
| sys_info | `apis/sys_info.py` | 系统信息 |
| env_exception | `apis/env_exception.py` | 环境异常统计 |
| proxy | `apis/proxy.py` | 代理配置 |

## 特殊路由

- **RSS**：`feeds_router` 无 API 前缀，公开访问
- **遗留视图**：`views/` → `/views/*`

## 依赖关系

- 依赖 [[core模块]] 业务逻辑
- 被 [[web_ui模块]] 前端调用

## 相关概念

- [[RSS订阅服务]]
- [[认证体系]]
- [[导出服务]]
