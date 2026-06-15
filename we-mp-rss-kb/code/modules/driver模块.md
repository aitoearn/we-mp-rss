---
type: module
created: 2026-06-13
updated: 2026-06-13
module: driver
tags: [后端, 采集]
---

# driver 模块

## 职责

微信公众号授权与浏览器自动化驱动，是 [[微信公众号采集]] 的基础设施层。

## 目录结构

```
driver/
├── base.py              # 驱动基类
├── wx.py                # Playwright 扫码登录（auth_web 模式）
├── wx_api.py            # 微信公众平台 API 登录
├── wxarticle.py         # 单篇文章正文抓取
├── playwright_driver.py # Playwright 封装
└── auth.py              # 授权服务启动
```

## 核心类/函数

| 名称 | 职责 |
|------|------|
| `driver/wx.py` | Web 扫码授权，Playwright 控制浏览器 |
| `driver/wx_api.py` | API Token 模式授权 |
| `driver/wxarticle.py` | 抓取单篇 HTML 正文 |
| `driver/auth.py` | `start_auth_service()` 后台授权服务 |

## 依赖关系

- 被 [[core模块]] `core/wx/` 采集逻辑调用
- 被 `main.py` 启动时初始化

## 相关概念

- [[微信公众号采集]]

## 注意事项

- Windows 需 ProactorEventLoop（`main.py` 已处理）
- Playwright 需安装浏览器：`playwright install`
- 代理配置影响授权成功率
