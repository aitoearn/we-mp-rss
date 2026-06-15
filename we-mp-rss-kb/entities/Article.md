---
type: entity
created: 2026-06-13
updated: 2026-06-13
tags: [核心]
---

# Article

## 存储

表名：`articles`（`core/models/article.py`）

## 字段（核心）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(255) PK | 文章全局唯一 ID |
| mp_id | String(255) | 公众号 ID，关联 [[Feed]] |
| title | String(1000) | 标题 |
| pic_url | String(500) | 封面图 URL |
| url | String(500) | 永久链接 |
| description | Text | 摘要 |
| content | Text | 正文（纯文本） |
| content_html | Text | 正文 HTML |
| status | Integer | 删除标记 |
| publish_time | Integer | 发布时间（Unix 戳） |
| has_content | Integer | 是否有正文（0/1，索引） |
| is_export | Integer | 是否已导出 |
| is_read | Integer | 是否已读 |
| is_favorite | Integer | 是否收藏 |
| fix_fail_count | Integer | 正文修正失败次数 |
| art_type | Integer | 内容类型（1=图文/视频/音频, 9=贴图） |

## 关系

- 多对一 → [[Feed]]（`mp_id`）
- 可被 Tags 分组

## 相关 API

- `apis/article.py` — 文章 CRUD、搜索、正文补全
- `apis/export.py` — 导出
- `apis/rss.py` — RSS item 数据源

## 相关概念

- [[微信公众号采集]]
- [[RSS订阅服务]]
- [[导出服务]]

## 注意事项

- `has_content=0` 表示仅有列表信息，正文待补全
- 正文抓取失败时 `fix_fail_count` 递增
- 大量索引字段用于前端筛选与排序
