---
type: module
created: 2026-06-13
updated: 2026-06-13
module: jobs
tags: [后端, 调度]
---

# jobs 模块

## 职责

后台定时任务与异步作业：采集调度、WebHook 投递、级联同步、通知。

## 目录结构

```
jobs/
├── mps.py                    # 主采集调度
├── webhook.py                # WebHook 回调
├── notice.py                 # 通知任务
├── cascade_sync.py           # 子节点同步服务
├── cascade_task_dispatcher.py# 任务分发器
└── cascade_init.py           # 级联初始化
```

## 核心类/函数

| 名称 | 职责 |
|------|------|
| `start_job()` | 启动定时采集（`jobs/__init__.py`） |
| `jobs/mps.py` | 按 interval 遍历 Feed 采集 |
| `cascade_sync_service` | 子节点定期 Pull 数据 |
| `cascade_schedule_service` | 父节点任务调度 |
| `start_child_task_worker()` | 子节点任务拉取 |

## 启动条件

- 采集：`python main.py -job True` 且 `server.enable_job=True`
- 级联：由 `cascade.enabled` 和 `node_type` 决定

## 依赖关系

- 依赖 [[core模块]] 采集与持久化
- 依赖 [[driver模块]] 授权状态

## 相关概念

- [[定时任务调度]]
- [[级联系统]]
