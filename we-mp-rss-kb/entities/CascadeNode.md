---
type: entity
created: 2026-06-13
updated: 2026-06-13
tags: [级联]
---

# CascadeNode

## 存储

表名：`cascade_nodes`（`core/models/cascade_node.py`）

## 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 节点 ID |
| node_type | Integer | 0=父节点, 1=子节点 |
| name | String | 节点名称 |
| api_key | String | 级联认证 AK |
| api_secret | String | 级联认证 SK |
| parent_id | Integer | 父节点 ID（子节点必填） |
| status | Integer | 在线状态 |
| sync_config | Text/JSON | 同步配置（容量、配额等） |
| last_heartbeat | DateTime | 最后心跳时间 |

## 关联表

- `cascade_sync_logs` — 同步日志（Pull/Push 记录）
- `cascade_task_allocations` — 任务分配状态机

## 关系

- 自引用：子节点 `parent_id` → 父节点
- 关联 [[MessageTask]] 任务分发

## 相关 API

- `apis/cascade.py` — 节点管理、凭证生成、同步日志

## 相关概念

- [[级联系统]]
- [[认证体系]]

## 注意事项

- 子节点凭证由父节点 Admin 生成
- 心跳超时影响任务分发决策
