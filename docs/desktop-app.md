# WeRSS 桌面应用

参考 [AutoGLM-GUI](https://github.com/suyiiyii/AutoGLM-GUI) 的 **Electron + Python FastAPI** 架构。

## 架构

```
Electron 主进程
  ├─ 开发模式: python main.py
  └─ 生产模式: resources/backend/werss-gui/werss-gui
       ↓
BrowserWindow → http://127.0.0.1:{port}
       ↓
FastAPI (web.py) + static/ 前端
```

## 环境要求

- Python >= 3.13.1
- Node.js >= 20
- PyInstaller（打包时需要）

## 开发模式

```bash
# 准备 Python 环境
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 启动桌面应用
cd electron
npm install
npm run dev
```

## 一键打包（第二阶段）

```bash
source .venv/bin/activate
pip install pyinstaller

# 完整构建：前端 + PyInstaller 后端 + Electron 安装包
python scripts/build_electron.py

# 仅重新打包后端与 Electron（跳过前端）
python scripts/build_electron.py --skip-frontend
```

构建产物：

| 步骤 | 输出 |
|------|------|
| 前端 | `static/` |
| PyInstaller | `resources/backend/werss-gui/` |
| Electron | `electron/dist/` |

### 分步构建

```bash
# 1. 构建前端
python scripts/build.py

# 2. 打包 Python 后端
cd scripts && pyinstaller werss.spec

# 3. 复制后端到 resources
mkdir -p ../resources/backend
cp -R dist/werss-gui ../resources/backend/

# 4. 构建 Electron
cd ../electron
npm install
npm run build:mac    # 或 build:win / build:linux
```

## 数据目录

桌面版数据存储在系统用户目录：

- macOS: `~/Library/Application Support/WeRSS/we-mp-rss/`
- Windows: `%APPDATA%/WeRSS/we-mp-rss/`
- Linux: `~/.config/WeRSS/we-mp-rss/`

包含：

- `config.yaml` — 应用配置
- `data/db.db` — SQLite 数据库
- `data/playwright-browsers/` — Playwright 浏览器（首次采集时下载）

## Playwright 说明

打包后的应用首次进行公众号采集时，可能需要联网下载 Playwright 浏览器到用户数据目录。如需预装，可在构建机器上执行：

```bash
PLAYWRIGHT_BROWSERS_PATH=./resources/playwright-browsers playwright install webkit
```

并将 `resources/playwright-browsers` 加入 `electron-builder.yml` 的 `extraResources`。

## 默认登录

- 用户名: `admin`
- 密码: `admin@123`
