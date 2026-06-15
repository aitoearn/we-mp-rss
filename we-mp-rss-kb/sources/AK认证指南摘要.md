---
type: source
created: 2026-06-13
updated: 2026-06-13
tags: [安全, 认证]
source_file: ../docs/AK_Authentication_Guide.md
---

# AK认证指南摘要

## 来源

`docs/AK_Authentication_Guide.md` — Access Key 管理 UI 使用指南。

## 概述

WeRSS 支持 Access Key (AK-SK) 认证，用于程序化访问 API，无需 JWT 登录会话。

## 功能

| 功能 | 说明 |
|------|------|
| 创建 AK | 自定义名称、描述、权限范围、过期时间 |
| 列表管理 | 查看状态（活跃/停用/过期）、最后使用时间 |
| 编辑/停用/删除 | 完整生命周期管理 |

## 使用方式

请求头格式：
```
Authorization: AK-SK {access_key}:{secret_key}
```

中间件：`web.py` 中 `AKMiddleware` 解析 AK-SK 头并注入 `request.state.ak_auth`。

## 权限范围

- 读（read）
- 写（write）
- 删除（delete）
- 管理（admin）

## Web UI

- 页面：`/access-keys`（AccessKeyManagement.vue）
- 权限：admin

## 关联 Wiki 页面

- [[认证体系]]
- [[User]]
- [[apis模块]]

## 注意事项

- Secret Key 只在创建时显示一次，需立即保存
- 生产环境应设置过期时间和最小权限
- 认证优先级：级联 AK/SK > 用户 AK/SK > JWT
