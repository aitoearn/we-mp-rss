# WeRSS 桌面应用

参考 [AutoGLM-GUI](https://github.com/suyiiyii/AutoGLM-GUI) 的 **Electron + Python FastAPI** 架构：Electron 负责窗口与进程生命周期，Python 后端提供 API 与前端静态资源。

## 架构

```
Electron 主进程 (electron/main.js)
  ├─ 启动 Python 后端 (main.py)
  ├─ 等待端口就绪
  └─ BrowserWindow 加载 http://127.0.0.1:{port}

Python 后端 (main.py + web.py)
  ├─ FastAPI API (/api/v1/wx/*)
  ├─ RSS (/rss, /feed)
  └─ 前端 SPA (static/)
```

## 环境要求

- **Python** >= 3.13.1（推荐项目根目录 `.venv`）
- **Node.js** >= 20
- 已安装后端依赖：`pip install -r requirements.txt`
- 首次运行会从 `config.example.yaml` 复制配置到用户数据目录

## 开发模式（当前可用）

```bash
# 1. 准备 Python 环境（若尚未完成）
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. 启动桌面应用
cd electron
npm install
npm run dev
```

应用会自动：

1. 在系统用户目录创建数据文件夹（macOS: `~/Library/Application Support/WeRSS/we-mp-rss/`）
2. 启动 `python main.py -job True -init True/False`
3. 打开桌面窗口并加载 WeRSS 管理界面

默认登录：`admin` / `admin@123`

## 自定义 Python 路径

若未使用 `.venv`，可指定解释器：

```bash
export WERSS_PYTHON=/path/to/python3.13
cd electron && npm run dev
```

## 与浏览器模式的区别

| 项目 | 浏览器模式 | 桌面模式 |
|------|-----------|---------|
| 启动方式 | `python main.py -job True -init True` | `cd electron && npm run dev` |
| 数据目录 | 项目内 `./data/` | 系统用户数据目录 |
| 配置文件 | 项目内 `config.yaml` | 用户数据目录内 `config.yaml` |
| 端口 | 默认 8001 | 自动从 8001 起查找可用端口 |

## 第二阶段：安装包打包（计划中）

将补充：

- `scripts/build_electron.py`：PyInstaller + electron-builder 一键构建
- macOS `.dmg` / Windows `.exe` / Linux `.AppImage`

当前 `electron/electron-builder.yml` 与 `scripts/build_electron.py` 为占位文件。
