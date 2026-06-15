---
type: entity
created: 2026-06-13
updated: 2026-06-13
tags: [安全]
---

# User

## 存储

表名：`users`（`core/models/user.py`）

## 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 用户 ID |
| username | String | 用户名 |
| password_hash | String | bcrypt 哈希 |
| role | String | 角色（admin / user） |
| permissions | Text/JSON | 细粒度权限列表 |
| created_at | DateTime | 创建时间 |

## 权限示例

| 权限 | 说明 |
|------|------|
| wechat:manage | 公众号管理 |
| message_task:* | 消息任务 |
| config:view | 配置查看 |
| tag:* | 标签管理 |
| admin | 全部权限 |

## 关系

- 一对多 → AccessKey（API 密钥）

## 相关 API

- `apis/auth.py` — 登录、Token 刷新
- `apis/user.py` — 用户 CRUD

## 相关概念

- [[认证体系]]

## 注意事项

- 首次启动 `-init True` 创建默认 admin 用户
- 密码修改页面：`web_ui/src/views/ChangePassword.vue`
