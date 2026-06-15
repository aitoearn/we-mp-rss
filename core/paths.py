"""应用路径解析，兼容开发模式与 PyInstaller 打包模式。"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional


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


def get_wx_qrcode_path() -> Path:
    """微信登录二维码本地文件路径（可写，位于 files 目录供 /files 静态服务访问）。"""
    path = Path(get_files_dir()) / "wx_qrcode.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_wx_qrcode_web_path() -> str:
    """微信登录二维码的 HTTP 访问路径（相对站点根路径）。"""
    return "files/wx_qrcode.png"


def get_wx_login_lock_path() -> Path:
    """微信扫码登录锁文件路径。"""
    return get_data_dir() / "wx_login.lock"


def normalize_export_mp_id(mp_id: Optional[str] = None) -> str:
    """导出目录使用的公众号 ID，空值表示导出全部文章。"""
    if mp_id is None:
        return ""
    value = str(mp_id).strip()
    return value


def get_export_docs_dir() -> Path:
    """文章导出根目录（可写）。"""
    path = get_data_dir() / "docs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_export_mp_dir(mp_id: Optional[str] = None) -> Path:
    """指定公众号（或全部）的导出目录。"""
    folder = normalize_export_mp_id(mp_id) or "_all"
    path = get_export_docs_dir() / folder
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_configured_export_root() -> Optional[Path]:
    """读取用户配置的导出根目录（环境变量或 config.yaml）。"""
    configured = os.environ.get("WERSS_EXPORT_DIR") or ""
    if not configured:
        try:
            from core.config import cfg

            configured = cfg.get("export.default_dir", "") or ""
        except Exception:
            configured = ""
    if not configured or not str(configured).strip():
        return None
    path = Path(str(configured).strip()).expanduser()
    if not path.is_absolute():
        return None
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def resolve_export_target_dir(mp_id: Optional[str] = None, export_dir: Optional[str] = None) -> Path:
    """解析导出目标目录，优先使用用户指定的绝对路径。"""
    if export_dir and str(export_dir).strip():
        path = Path(str(export_dir).strip()).expanduser()
        if not path.is_absolute():
            raise ValueError("导出目录必须是绝对路径")
        path = path.resolve()
        path.mkdir(parents=True, exist_ok=True)
        if not os.access(path, os.W_OK):
            raise ValueError(f"导出目录不可写: {path}")
        return path
    configured_root = get_configured_export_root()
    if configured_root is not None:
        folder = normalize_export_mp_id(mp_id) or "_all"
        path = configured_root / folder
        path.mkdir(parents=True, exist_ok=True)
        return path
    return get_export_mp_dir(mp_id)
