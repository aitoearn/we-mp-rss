#!/usr/bin/env python3
"""
WeRSS Electron 桌面应用构建脚本（第二阶段占位）

当前阶段仅支持开发模式：
    cd electron && npm install && npm run dev

后续将补充：
1. 前端构建（web_ui -> static）
2. PyInstaller 打包 Python 后端
3. electron-builder 生成安装包

用法（占位）：
    python scripts/build_electron.py
"""

from __future__ import annotations

import sys


def main() -> int:
    print("WeRSS 桌面应用打包脚本尚未实现。")
    print("请先使用开发模式：")
    print("  cd electron")
    print("  npm install")
    print("  npm run dev")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
