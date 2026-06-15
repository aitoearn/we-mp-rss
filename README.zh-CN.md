<div align=center>
<img src="static/logo.svg" alt="We-MP-RSS Logo" width="20%">
<h1>WeRSS - 微信公众号订阅助手</h1>

[![Python Version](https://img.shields.io/badge/python-3.13.1+-red.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

[English](ReadMe.md)

快速开始

WeRSS 是 **Electron 桌面客户端**，内置 Python 后端，适合在个人电脑上订阅、阅读与导出公众号文章。

1. 从 [Releases](https://github.com/aitoearn/we-mp-rss/releases) 下载对应平台安装包（macOS 为 `.dmg`，Windows 为 `.exe` 安装程序）
2. 安装并启动 **WeRSS**
3. 默认账号登录：`admin` / `admin@123`
4. 按界面提示完成微信扫码授权，添加公众号订阅

自行构建安装包：

```bash
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pyinstaller
python scripts/build_electron.py
# macOS 产物：electron/dist/WeRSS-*-arm64.dmg
```

详细说明见 [桌面应用文档](docs/desktop-app.md)。

### 桌面版数据目录

| 系统 | 路径 |
|------|------|
| macOS | `~/Library/Application Support/WeRSS/we-mp-rss/` |
| Windows | `%APPDATA%/WeRSS/we-mp-rss/` |
| Linux | `~/.config/WeRSS/we-mp-rss/` |

目录内包含：`config.yaml`、SQLite 数据库（`data/db.db`）、导出记录、Playwright 浏览器缓存等。

### 自定义默认导出目录（桌面版）

编辑 `export_prefs.json`（位于上述数据目录）：

```json
{
  "defaultExportDir": "/你的/导出/目录",
  "lastExportDir": "/你的/导出/目录"
}
```

也可在 `config.yaml` 中设置 `export.default_dir`，或通过环境变量 `WERSS_EXPORT_DIR` 指定。

 <br/>
 <img src="https://github.com/user-attachments/assets/cbe924f2-d8b0-48b0-814e-7c06ccb1911c" height="60" />
    <img src="https://github.com/user-attachments/assets/6997a236-3df3-49d5-98a4-514f6d1a02c4" height="60" />
    <br />
    <br />
    <a href="https://github.com/RSSNext/Folo/stargazers"><img src="https://img.shields.io/github/stars/RSSNext/Follow?color=ffcb47&labelColor=black&style=flat-square&logo=github&label=Stars" /></a>
    <a href="https://github.com/RSSNext/Folo/graphs/contributors"><img src="https://img.shields.io/github/contributors/RSSNext/Folo?style=flat-square&logo=github&label=Contributors&labelColor=black" /></a>
    <a href="https://status.follow.is/" target="_blank"><img src="https://status.follow.is/api/badge/18/uptime?color=%2344CC10&labelColor=black&style=flat-square"/></a>
    <a href="https://github.com/RSSNext/Folo/releases"><img src="https://img.shields.io/github/downloads/RSSNext/Folo/total?color=369eff&labelColor=black&logo=github&style=flat-square&label=Downloads" /></a>
    <a href="https://x.com/intent/follow?screen_name=folo_is"><img src="https://img.shields.io/badge/Follow-blue?color=1d9bf0&logo=x&labelColor=black&style=flat-square" /></a>
    <a href="https://discord.gg/followapp" target="_blank"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Finvites%2Ffollowapp%3Fwith_counts%3Dtrue&query=approximate_member_count&color=5865F2&label=Discord&labelColor=black&logo=discord&logoColor=white&style=flat-square"/></a>
    <br />
一个用于订阅和管理微信公众号内容的桌面工具，提供 RSS 订阅与文章导出功能。<br/>
<strong>支持 macOS / Windows / Linux，开箱即用。</strong>
</div>

## 关于本项目

本项目基于开源项目 [rachelos/we-mp-rss](https://github.com/rachelos/we-mp-rss) 进行二次开发，在原有微信公众号 RSS 订阅与采集能力之上，新增了 Electron 桌面客户端、导出目录可配置、Markdown 图片本地化等功能。感谢原作者及社区贡献者的开源工作。

## 功能特性

- 微信公众号内容抓取和解析
- RSS订阅生成
- 用户友好的Web管理界面
- 定时自动更新内容
- 支持多种数据库（默认SQLite，可选MySQL）
- 支持多种抓取方式
- 支持多种RSS客户端
- 支持授权过期提醒
- 支持自定义通知渠道
- 支持自定义RSS标题、描述、封面
- 支持自定义RSS分页大小
- 支持导出 md/docx/pdf/json/csv 格式（桌面版支持自选文件夹、导出结果提示）
- Markdown 导出可本地化图片到 `_assets` 目录并打入 zip
- **桌面客户端（Electron）**：内置后端、本地数据、登录状态持久化
- 支持 API 接口调用/WebHook 调用
- 支持HTML内容过滤规则（全局规则和公众号专属规则）
- 支持多主题切换（13种主题：默认紫色、清新蓝色、自然绿色、活力橙色、玫瑰红、青碧色、樱花粉、靛青色、紫罗兰、咖啡棕、深海蓝、深色模式、护眼模式）
- 支持响应式分页（PC端点击翻页，移动端加载更多按钮）
- **级联系统**：支持父子节点架构，智能任务分发，扩展采集能力
- **环境异常统计**：自动统计微信公众号文章获取时的环境异常情况
- **Headers和Cookies认证**：消息任务支持自定义Headers和Cookies，用于需要认证的WebHook调用
- **配置缓存**：支持Redis、Memcached和内存缓存，提升配置读取性能

## 界面截图
- 登录界面  
<img src="docs/登录.png" alt="登录" width="80%"/><br/>
- 主界面  
<img src="docs/主界面.png" alt="主界面" width="80%"/><br/>
- 扫码授权  
<img src="docs/扫码授权.png" alt="扫码授权" width="80%"/><br/>
- 添加订阅  
<img src="docs/添加订阅.png" alt="添加订阅" width="80%"/><br/>

- 客户端应用<br/>
<img src="docs/folo.webp" alt="FOLO客户端应用" width="80%"/><br/>



## 系统架构

项目采用 **Electron + Python FastAPI + Vue 3** 架构：

```
桌面客户端（Electron）
  └─ 内嵌 Python 后端（FastAPI + 定时任务）
       └─ Vue 3 管理界面（static/）
```

- 后端：Python + FastAPI
- 前端：Vue 3 + Vite
- 桌面壳：Electron（`electron/`）
- 数据库：SQLite（默认）/ MySQL / PostgreSQL

<img src="docs/架构原理.png" alt="架构原理" width="80%"/>

更多项目原理，请参考 [项目文档](https://deepwiki.com/rachelos/we-mp-rss/3.5-notification-system) 与 [桌面应用文档](docs/desktop-app.md)。

## 安装与开发

### 桌面版开发

```bash
git clone https://github.com/aitoearn/we-mp-rss.git
cd we-mp-rss
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd electron && npm install && npm run dev
```

### 桌面版打包

```bash
source .venv/bin/activate
pip install pyinstaller
python scripts/build_electron.py              # 完整构建
python scripts/build_electron.py --skip-frontend # 仅后端 + Electron
```

### 源码开发（可选）

环境需求：Python >= 3.13.1，Node >= 20.18.3

1. 克隆项目
```bash
git clone https://github.com/rachelos/we-mp-rss.git
cd we-mp-rss
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 配置数据库
复制并修改配置文件：
```bash
cp config.example.yaml config.yaml
copy config.example.yaml config.yaml
```
3. 启动服务
```bash
python main.py -job True -init True
```

## 前端开发
1. 安装前端依赖
```bash
cd web_ui
yarn install
```

2. 启动前端服务
```bash
yarn dev
```
3. 访问前端页面
```
http://localhost:3000
```

# 环境变量配置

以下是 `config.yaml` 中支持的环境变量配置：

| 环境变量 | 默认值 | 描述 |
|----------|--------|------|
| `APP_NAME` | `we-mp-rss` | 应用名称 |
| `SERVER_NAME` | `we-mp-rss` | 服务名称 |
| `WEB_NAME` | `WeRSS微信公众号订阅助手` | 前端显示名称 |
| `WERSS_AUTH_WEB` | `False` | 通过web方式授权 |
| `BROWSER_TYPE` | `firefox` | 浏览器类型默认firefox |
| `SEND_CODE` | `False` | 过期通知中是否附带授权二维码（默认仅发送文字通知） |
| `CODE_TITLE` | `WeRSS授权二维码` | 二维码通知标题 |
| `ENABLE_JOB` | `True` | 是否启用定时任务 |
| `AUTO_RELOAD` | `False` | 代码修改自动重启服务 |
| `THREADS` | `2` | 最大线程数 |
| `DB` | `sqlite:///data/db.db` | 数据库连接字符串 |
| `DINGDING_WEBHOOK` | 空 | 钉钉通知Webhook地址 |
| `WECHAT_WEBHOOK` | 空 | 微信通知Webhook地址 |
| `FEISHU_WEBHOOK` | 空 | 飞书通知Webhook地址 |
| `CUSTOM_WEBHOOK` | 空 | 自定义通知Webhook地址 |
| `SECRET_KEY` | `we-mp-rss` | 密钥 |
| `USER_AGENT` | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36/WeRss` | 用户代理 |
| `SPAN_INTERVAL` | `10` | 定时任务执行间隔（秒） |
| `WEBHOOK.CONTENT_FORMAT` | `html` | 文章内容发送格式 |
| `PORT` | `8001` | API服务端口 |
| `DEBUG` | `False` | 调试模式 |
| `MAX_PAGE` | `5` | 最大采集页数 |
| `RSS_BASE_URL` | 空 | RSS域名地址 |
| `RSS_LOCAL` | `False` | 是否为本地RSS链接 |
| `RSS_TITLE` | 空 | RSS标题 |
| `RSS_DESCRIPTION` | 空 | RSS描述 |
| `RSS_COVER` | 空 | RSS封面 |
| `RSS_FULL_CONTEXT` | `True` | 是否显示全文 |
| `RSS_ADD_COVER` | `True` | 是否添加封面图片 |
| `RSS_CDATA` | `False` | 是否启用CDATA |
| `RSS_PAGE_SIZE` | `30` | RSS分页大小 |
| `TOKEN_EXPIRE_MINUTES` | `4320` | 登录会话有效时长（分钟） |
| `CACHE.DIR` | `./data/cache` | 缓存目录 |
| `ARTICLE.TRUE_DELETE` | `False` | 是否真实删除文章 |
| `GATHER.CONTENT` | `True` | 是否采集内容 |
| `GATHER.MODEL` | `app` | 采集模式 |
| `GATHER.CONTENT_AUTO_CHECK` | `False` | 是否自动检查未采集文章内容 |
| `GATHER.CONTENT_AUTO_INTERVAL` | `59` | 自动检查未采集文章内容的时间间隔（分钟） |
| `GATHER.CONTENT_MODE` | `web` | 内容修正模式 |
| `SAFE_HIDE_CONFIG` | `db,secret,token,notice.wechat,notice.feishu,notice.dingding` | 需要隐藏的配置信息 |
| `SAFE_LIC_KEY` | `RACHELOS` | 授权加密KEY |
| `LOG_FILE` | 空 | 日志文件路径 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `EXPORT_PDF` | `False` | 是否启用PDF导出功能 |
| `EXPORT_PDF_DIR` | `./data/pdf` | PDF导出目录 |
| `EXPORT_MARKDOWN` | `False` | 是否启用 markdown 导出功能 |
| `EXPORT_MARKDOWN_DIR` | `./data/markdown` | markdown 导出目录 |
| `WERSS_EXPORT_DIR` | 空 | 默认导出根目录（绝对路径，桌面版也可通过 export_prefs.json 配置） |

# 使用说明

1. 启动 WeRSS，使用 `admin` / `admin@123` 登录（首次登录后建议修改密码）。
2. 进入「微信状态」完成扫码授权。
3. 添加公众号订阅，等待定时任务或手动触发采集。
4. 在文章列表中阅读、收藏，或通过「导出」批量保存。

### 文章导出

在文章列表点击「导出」，可配置：

| 选项 | 说明 |
|------|------|
| 导出格式 | PDF、Markdown、Word、JSON、Excel 列表等，可多选 |
| 默认目录 | zip 保存到数据目录下的 `data/docs/{公众号ID}/`，可在「导出记录」下载 |
| 自选文件夹 | 桌面版可直接选本地目录（如 Obsidian 库），导出完成后可「在 Finder 中打开」 |
| 移除图片 | 勾选后不导出正文图片；**Markdown 不勾选时会下载图片到 `{文章名}_assets/`** |

导出完成后界面会提示结果；若 PDF 生成失败会给出具体原因（如 Playwright 浏览器未就绪、正文未采集等）。

## Access Key 认证

WeRSS 支持使用 Access Key (AK) 进行 API 认证，适用于程序化访问和自动化脚本。

### 创建 Access Key

1. 登录 WeRSS 管理界面
2. 进入"Access Key 管理"页面
3. 点击"创建 Access Key"按钮
4. 填写名称、描述、权限和过期时间
5. 创建成功后，妥善保存 Access Key 和 Secret Key（Secret Key 只显示一次）

### 使用 Access Key 调用 API

在请求头中添加 `Authorization` 字段，格式为 `AK-SK {access_key}:{secret_key}`：

```bash
curl -H "Authorization: AK-SK your_access_key:your_secret_key" \
     http://localhost:8001/api/feeds
```

#### Python 示例

```python
import requests

access_key = "your_access_key"
secret_key = "your_secret_key"
base_url = "http://localhost:8001"

headers = {
    "Authorization": f"AK-SK {access_key}:{secret_key}"
}

# 获取订阅列表
response = requests.get(f"{base_url}/api/feeds", headers=headers)
print(response.json())
```

#### JavaScript 示例

```javascript
const accessKey = "your_access_key";
const secretKey = "your_secret_key";
const baseUrl = "http://localhost:8001";

const headers = {
  "Authorization": `AK-SK ${accessKey}:${secretKey}`
};

// 获取订阅列表
fetch(`${baseUrl}/api/feeds`, { headers })
  .then(res => res.json())
  .then(data => console.log(data));
```

详细文档请参考：[AK 认证指南](docs/AK_Authentication_Guide.md)

## HTML 内容过滤规则

WeRSS 支持自定义 HTML 内容过滤规则，可以在采集文章内容时自动清理不需要的元素，如广告、推荐链接等。

### 功能特点

- **全局规则**：不指定公众号时，规则对所有公众号生效
- **公众号专属规则**：可以为特定公众号或多个公众号配置不同的过滤规则
- **优先级控制**：支持设置规则优先级，数值越大越先执行
- **多种过滤方式**：
  - 按 ID 移除元素
  - 按 CSS Class 移除元素
  - 按 CSS 选择器移除元素
  - 按属性过滤元素
  - 按正则表达式移除内容
  - 移除常见 HTML 元素（script、style、注释等）

### 使用方法

1. 登录管理界面，进入「过滤规则」页面
2. 点击「添加过滤规则」
3. 配置规则：
   - **选择公众号**：可选多个公众号，不选择则为全局规则
   - **规则名称**：便于识别的规则名称
   - **优先级**：数值越大优先级越高（0-100）
   - **过滤配置**：
     - 移除 ID 元素：每行一个 ID，如 `ad-banner`
     - 移除 Class 元素：每行一个 class，如 `ad-container`
     - CSS 选择器：如 `div.ad-wrapper`、`.recommend-list > li`
     - 属性过滤：如 `data-type="ad"`
     - 正则表达式：用于精确匹配和移除内容

### 示例配置

#### 全局广告过滤规则
```
规则名称：全局广告清理
公众号：不选择（全局规则）
优先级：10
移除 ID：ad-banner、footer-nav
移除 Class：ad-container、recommend-box
CSS 选择器：div.ad-wrapper、.recommend-list > li
移除常见 HTML 元素：开启
```

#### 特定公众号规则
```
规则名称：某公众号专属过滤
公众号：选择特定公众号
优先级：20（高于全局规则，会先执行）
移除 Class：custom-ad、special-banner
```

### API 接口

过滤规则支持完整的 REST API 操作：

```bash
# 获取过滤规则列表
GET /api/filter-rules

# 创建过滤规则
POST /api/filter-rules
{
  "mp_id": "[]",  // 空数组表示全局规则
  "rule_name": "全局广告过滤",
  "remove_ids": ["ad-banner"],
  "remove_classes": ["ad-container"],
  "priority": 10
}

# 更新过滤规则
PUT /api/filter-rules/{rule_id}

# 删除过滤规则
DELETE /api/filter-rules/{rule_id}
```

# 常见问题

- **如何修改数据库连接？**
  在 `config.yaml` 中修改 `db` 配置项，或通过环境变量 `DB` 覆盖。

- **如何启用钉钉通知？**
  在 `config.yaml` 中填写 `notice.dingding` 或通过环境变量 `DINGDING_WEBHOOK` 设置。

- **如何调整定时任务间隔？**
  修改 `config.yaml` 中的 `interval` 或通过环境变量 `SPAN_INTERVAL` 设置。

- **如何开启定时任务？**
  1、修改 `config.yaml` 中的 `ENABLE_JOB` 或通过环境变量 `ENABLE_JOB` 设置 为True。
  2、在UI界面的消息任务中，添加定时任务。
  
- **如何修改文章内容发送格式？**
  修改 `config.yaml` 中的 `WEBHOOK.CONTENT_FORMAT` 或通过环境变量 `WEBHOOK.CONTENT_FORMAT` 设置。

- **默认帐号、密码是多少？**
  - 默认帐号：admin
  - 默认密码：admin@123

- **桌面版导出文件在哪里？**
  - 默认目录：`数据目录/data/docs/{公众号ID}/` 或你在 `export_prefs.json` 中配置的 `defaultExportDir`
  - 自选文件夹：导出时选择的本地路径
  - 可在应用内「导出记录」查看并下载历史 zip

- **导出 zip 里为什么只有部分格式 / PDF 失败？**
  - 仅选 PDF 时，若 Playwright 浏览器未安装或文章正文未采集，可能无法生成文件；界面会提示失败原因
  - 建议同时勾选 JSON 便于排查，或先确认文章已补全正文

- **数据库连接串示例**
  - 调整环境变量DB为您的数据库连接字符串。
  - SQLite 连接示例: 
  ```
  sqlite:///data/db.db
  ```
  - PostgreSQL 连接示例: 
  ```
  postgresql://<username>:<password>@<host>/<database>
  ```
  - MySQL 连接示例:
  ```
  mysql+pymysql://<username>:<password>@<host>/<database>?charset=utf8mb4
  ```


[Star History Chart]: https://api.star-history.com/svg?repos=rachelos/we-mp-rss&type=Timeline