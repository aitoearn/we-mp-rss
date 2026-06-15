---
type: entity
created: 2026-06-13
updated: 2026-06-13
tags: [调度]
---

# MessageTask

## 存储

表名：`message_tasks`（`core/models/` 下对应模型）

## 字段（核心）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 任务 ID |
| name | String | 任务名称 |
| mp_id | String | 关联 [[Feed]] 公众号 |
| webhook_url | String | WebHook 投递地址 |
| headers | Text/JSON | 自定义请求头 |
| cookies | Text/JSON | 自定义 Cookies |
| status | Integer | 启用/禁用 |
| cron/interval | — | 触发频率 `[待补充]` |

## 关联

- `message_task_logs` — 执行日志

## 关系

- 多对一 → [[Feed]]
- 可被 [[级联系统]] 父节点分发到子节点

## 相关 API

- `apis/message_task.py` — CRUD、手动触发、测试

## 相关概念

- [[定时任务调度]]

## 注意事项

- 支持自定义 Headers/Cookies 用于需认证的 WebHook
- 详见 `docs/headers_cookies_feature.md`
