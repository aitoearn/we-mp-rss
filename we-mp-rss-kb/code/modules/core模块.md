---
type: module
created: 2026-06-13
updated: 2026-06-13
module: core
tags: [后端, 核心]
---

# core 模块

## 职责

后端核心业务逻辑：数据模型、采集、RSS 生成、认证、配置、级联、通知、任务调度。

## 目录结构

```
core/
├── models/          # SQLAlchemy 数据模型
├── wx/              # 公众号采集（web/app/api 三种模式）
├── rss.py           # RSS/Atom/JSON 生成
├── auth.py          # JWT / AK-SK / 级联认证
├── db.py            # 数据库会话
├── config.py        # YAML + 环境变量配置
├── cascade.py       # 级联管理器
├── export_history.py# 导出历史
├── paths.py         # 数据目录路径
├── lax/             # 模板解析
├── notice/          # 通知渠道
├── task/            # TaskScheduler
├── queue/           # 任务队列
└── webhook/         # WebHook 投递
```

## 核心类/函数

| 名称 | 职责 |
|------|------|
| `Feed` / `Article` | 核心数据模型 |
| `core/wx/base.py` | 采集基类调度 |
| `core/rss.py` | RSS 格式转换 |
| `core/auth.py` | 认证逻辑 |
| `core/cascade.py` | 级联客户端 |

## 依赖关系

- 被 [[apis模块]] 调用
- 被 [[jobs模块]] 调用
- 依赖 [[driver模块]] 提供的授权状态

## 相关概念

- [[微信公众号采集]]
- [[RSS订阅服务]]
- [[级联系统]]
- [[认证体系]]
