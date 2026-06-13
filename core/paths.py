"""应用路径解析，兼容开发模式与 PyInstaller 打包模式。"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def get_bundle_dir() -> Path:
    """打包资源目录（static、public 等只读资源）。"""
    if is_frozen():
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def get_project_root() -> Path:
    """项目/后端运行根目录。"""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return get_bundle_dir()


def get_data_dir() -> Path:
    """可写数据目录（数据库、缓存、上传文件等）。"""
    override = os.environ.get("WERSS_DATA_DIR")
    if override:
        path = Path(override)
    else:
        path = get_project_root() / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_static_dir() -> str:
    return str(get_bundle_dir() / "static")


def get_public_dir() -> str:
    return str(get_bundle_dir() / "public")


def get_files_dir() -> str:
    files_dir = get_data_dir() / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    return str(files_dir)


def get_avatars_dir() -> str:
    avatar_dir = Path(get_files_dir()) / "avatars"
    avatar_dir.mkdir(parents=True, exist_ok=True)
    return str(avatar_dir)
