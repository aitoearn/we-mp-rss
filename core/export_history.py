"""导出历史记录，支持默认目录与自选目录的导出文件追踪。"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from core.paths import get_data_dir, normalize_export_mp_id


def get_history_file() -> Path:
    path = get_data_dir() / "export_history.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_history() -> list[dict[str, Any]]:
    history_file = get_history_file()
    if not history_file.exists():
        return []
    try:
        data = json.loads(history_file.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def save_history(records: list[dict[str, Any]]) -> None:
    history_file = get_history_file()
    history_file.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def append_export_record(
    *,
    file_path: str,
    mp_id: Optional[str] = None,
    filename: Optional[str] = None,
    summary: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """登记一次成功的导出。"""
    resolved = str(Path(file_path).expanduser().resolve())
    if not os.path.isfile(resolved):
        raise FileNotFoundError(f"导出文件不存在: {resolved}")

    folder = normalize_export_mp_id(mp_id) or "_all"
    name = filename or os.path.basename(resolved)
    stat = os.stat(resolved)
    record = {
        "id": uuid.uuid4().hex,
        "filename": name,
        "mp_id": folder,
        "file_path": resolved,
        "size": stat.st_size,
        "created_time": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
        "modified_time": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "status": "success",
    }
    if summary:
        record["summary"] = summary

    records = load_history()
    records = [item for item in records if item.get("file_path") != resolved]
    records.insert(0, record)
    save_history(records[:200])
    return record


def save_last_export_result(result: dict[str, Any]) -> None:
    """保存最近一次导出任务结果，供前端轮询。"""
    path = get_data_dir() / "export_last_result.json"
    payload = {
        **result,
        "updated_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_last_export_result() -> Optional[dict[str, Any]]:
    path = get_data_dir() / "export_last_result.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


def remove_export_record(*, mp_id: Optional[str], filename: str) -> Optional[dict[str, Any]]:
    folder = normalize_export_mp_id(mp_id) or "_all"
    records = load_history()
    kept: list[dict[str, Any]] = []
    removed: Optional[dict[str, Any]] = None
    for item in records:
        same_folder = item.get("mp_id") == folder
        same_name = item.get("filename") == filename or item.get("path") == filename
        if removed is None and same_folder and same_name:
            removed = item
            continue
        kept.append(item)
    if removed is not None:
        save_history(kept)
    return removed


def find_export_record(
    *,
    mp_id: Optional[str] = None,
    filename: Optional[str] = None,
    record_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    records = load_history()
    for item in records:
        if record_id and item.get("id") == record_id:
            return item
        if filename is None:
            continue
        folder = normalize_export_mp_id(mp_id) or "_all"
        if item.get("mp_id") == folder and (
            item.get("filename") == filename or item.get("path") == filename
        ):
            return item
    return None
