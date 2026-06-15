---
type: entity
created: 2026-06-13
updated: 2026-06-13
tags: [核心]
---

# Feed

## 存储

表名：`feeds`（`core/models/feed.py`）

## 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(255) PK | 公众号 ID |
| mp_name | String(255) | 公众号名称 |
| mp_cover | String(255) | 封面 URL |
| mp_intro | String(255) | 简介 |
| status | Integer | 状态（索引） |
| sync_time | Integer | 最后同步时间 |
| update_time | Integer | 更新时间 |
| faker_id | String(255) | **采集关键 ID**，微信内部标识 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 特殊常量

- `FEATURED_MP_ID = "MP_WXS_FEATURED_ARTICLES"` — 精选文章归类

## 关系

- 一对多 → [[Article]]（通过 `mp_id`）
- 被 [[MessageTask]] 引用

## 相关 API

- `apis/mps.py` — 公众号 CRUD、同步触发
- `apis/rss.py` — 按 Feed 生成 RSS

## 相关概念

- [[微信公众号采集]]
- [[RSS订阅服务]]

## 注意事项

- `faker_id` 是采集的核心标识，添加订阅时必须正确获取
- 同步状态通过 `status` 和 `sync_time` 追踪
