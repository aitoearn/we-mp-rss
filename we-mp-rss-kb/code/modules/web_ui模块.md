---
type: module
created: 2026-06-13
updated: 2026-06-13
module: web_ui
tags: [前端]
---

# web_ui 模块

## 职责

Vue 3 + Vite 前端 SPA，提供 Web 管理界面。构建产物输出到 `static/`。

## 技术栈

- Vue 3 + TypeScript
- Vue Router 4
- Arco Design + Ant Design Vue
- Monaco Editor / CodeMirror

## 目录结构

```
web_ui/src/
├── views/           # 页面（PascalCase 命名）
├── components/      # 组件
├── api/             # API 封装（auth.ts, tools.ts 等）
├── router/          # 路由与权限守卫
├── utils/           # 工具函数
└── types/           # TypeScript 类型（含 electron.d.ts）
```

## 主要页面

| 路由 | 视图 | 权限 |
|------|------|------|
| `/` | ArticleList | 登录 |
| `/wechat/mp` | WeChatMpManagement | wechat:manage |
| `/message-tasks` | MessageTaskList | message_task:* |
| `/export/records` | ExportRecords | config:view |
| `/cascade` | CascadeManagement | admin |
| `/access-keys` | AccessKeyManagement | admin |
| `/configs` | ConfigList | config:view |
| `/sys-info` | SysInfo | admin |

## 开发命令

```bash
cd web_ui && npm install
npm run dev    # 开发
npm run build  # 构建到 static/
```

## 依赖关系

- 调用 [[apis模块]] REST 接口
- Electron 桌面版通过 IPC 扩展（[[导出服务]]）

## 相关概念

- [[认证体系]]
- [[导出服务]]
