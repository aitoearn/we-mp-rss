#!/usr/bin/env python3
"""构建前端并复制到 static/ 目录。"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    web_ui = root / "web_ui"
    static_dir = root / "static"

    print("安装前端依赖...")
    subprocess.run(
        ["npm", "install", "--legacy-peer-deps"],
        cwd=web_ui,
        check=True,
    )

    print("构建前端...")
    subprocess.run(["npm", "run", "build"], cwd=web_ui, check=True)

    dist_dir = web_ui / "dist"
    if not dist_dir.exists():
        print("错误: 前端构建产物不存在", file=sys.stderr)
        return 1

    print(f"复制构建产物到 {static_dir} ...")
    if static_dir.exists():
        shutil.rmtree(static_dir)
    shutil.copytree(dist_dir, static_dir)
    print("前端构建完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
