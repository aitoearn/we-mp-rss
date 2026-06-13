"""
WeRSS 桌面版后端 CLI 入口（PyInstaller 打包入口）

用法:
    werss-gui --port 8001 --config /path/to/config.yaml --job True --init False
"""

from __future__ import annotations

import argparse
import os
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WeRSS 桌面版后端服务")
    parser.add_argument("--port", type=int, required=True, help="HTTP 监听端口")
    parser.add_argument("--config", required=True, help="config.yaml 绝对路径")
    parser.add_argument("--data-dir", required=True, help="数据目录绝对路径")
    parser.add_argument("--job", default="True", help="是否启动定时任务")
    parser.add_argument("--init", dest="init_db", default="False", help="是否初始化数据库")
    return parser.parse_args()


def configure_runtime(args: argparse.Namespace) -> None:
    """在导入 main 模块前配置运行环境。"""
    os.environ["PORT"] = str(args.port)
    os.environ["WERSS_DATA_DIR"] = args.data_dir
    os.environ["WERSS_DESKTOP"] = "1"

    db_path = os.path.join(args.data_dir, "db.db").replace("\\", "/")
    os.environ["DB"] = f"sqlite:///{db_path}"

    if getattr(sys, "frozen", False):
        os.environ["WERSS_BUNDLE_DIR"] = sys._MEIPASS

    playwright_dir = os.path.join(args.data_dir, "playwright-browsers")
    os.makedirs(playwright_dir, exist_ok=True)
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", playwright_dir)

    sys.argv = [
        "werss-gui",
        "-config",
        args.config,
        "-job",
        args.job,
        "-init",
        args.init_db,
    ]


def main() -> None:
    args = parse_args()
    os.makedirs(args.data_dir, exist_ok=True)
    configure_runtime(args)

    from main import run

    run()


if __name__ == "__main__":
    main()
