"""导出时下载并本地化文章图片。"""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Optional
from urllib.parse import quote, unquote, urlparse

import requests
from bs4 import BeautifulSoup

from core.print import print_error, print_warning

_WECHAT_IMAGE_HOSTS = ("mmbiz.qpic.cn", "mmbiz.qlogo.cn", "mmecoa.qpic.cn")
_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://mp.weixin.qq.com/",
}


def _guess_extension(content_type: str, url: str) -> str:
    mapping = {
        "jpeg": ".jpg",
        "jpg": ".jpg",
        "png": ".png",
        "gif": ".gif",
        "webp": ".webp",
        "svg": ".svg",
    }
    lowered = (content_type or "").lower()
    for key, ext in mapping.items():
        if key in lowered:
            return ext
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
        if path.endswith(ext):
            return ext
    return ".jpg"


def resolve_download_url(raw_url: str, *, server_port: Optional[int] = None) -> Optional[str]:
    """将 img src 解析为可下载的 HTTP URL。"""
    if not raw_url or not str(raw_url).strip():
        return None
    url = str(raw_url).strip()
    if url.startswith("data:"):
        return None

    if url.startswith("/static/res/logo/") or url.startswith("/api/v1/res/logo/"):
        encoded = url.split("/logo/", 1)[-1]
        decoded = unquote(encoded)
        if decoded.startswith(("http://", "https://")):
            url = decoded
        elif server_port:
            return f"http://127.0.0.1:{server_port}{url if url.startswith('/') else '/' + url}"

    if url.startswith("//"):
        url = "https:" + url

    if url.startswith("/") and server_port:
        return f"http://127.0.0.1:{server_port}{url}"

    parsed = urlparse(url)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return url
    return None


def download_image_to_file(
    raw_url: str,
    dest_path: Path,
    *,
    server_port: Optional[int] = None,
    timeout: int = 25,
) -> bool:
    """下载图片到指定路径。"""
    download_url = resolve_download_url(raw_url, server_port=server_port)
    if not download_url:
        return False

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    candidates = [download_url]
    parsed = urlparse(download_url)
    if parsed.netloc in _WECHAT_IMAGE_HOSTS and server_port:
        proxy_path = f"/static/res/logo/{quote(download_url, safe='')}"
        candidates.insert(0, f"http://127.0.0.1:{server_port}{proxy_path}")

    last_error: Optional[Exception] = None
    for candidate in candidates:
        try:
            response = requests.get(candidate, stream=True, timeout=timeout, headers=_DEFAULT_HEADERS)
            response.raise_for_status()
            ext = _guess_extension(response.headers.get("Content-Type", ""), candidate)
            final_path = dest_path if dest_path.suffix else dest_path.with_suffix(ext)
            with open(final_path, "wb") as handle:
                for chunk in response.iter_content(8192):
                    if chunk:
                        handle.write(chunk)
            if final_path.stat().st_size <= 0:
                final_path.unlink(missing_ok=True)
                continue
            if final_path != dest_path and dest_path.exists():
                dest_path.unlink(missing_ok=True)
            return True
        except Exception as error:
            last_error = error
            continue

    print_warning(f"图片下载失败: {raw_url} ({last_error})")
    return False


def _pick_img_src(img_tag) -> Optional[str]:
    for attr in ("src", "data-src", "data-original", "data-lazy-src"):
        value = img_tag.get(attr)
        if value and str(value).strip() and not str(value).startswith("data:"):
            return str(value).strip()
    return None


def localize_html_images(
    html_content: str,
    assets_dir: Path,
    *,
    assets_rel_prefix: str,
    server_port: Optional[int] = None,
) -> tuple[str, int]:
    """
    下载 HTML 中的图片到 assets_dir，并将 src 改写为相对路径。

    Returns:
        (处理后的 HTML, 成功下载的图片数量)
    """
    if not html_content or not html_content.strip():
        return html_content, 0

    soup = BeautifulSoup(html_content, "html.parser")
    assets_dir.mkdir(parents=True, exist_ok=True)
    rel_prefix = assets_rel_prefix.rstrip("/")
    downloaded = 0
    used_names: set[str] = set()

    for index, img in enumerate(soup.find_all("img"), start=1):
        raw_src = _pick_img_src(img)
        if not raw_src:
            continue

        digest = hashlib.sha256(raw_src.encode("utf-8")).hexdigest()[:16]
        filename = f"img_{index:03d}_{digest}"
        dest_path = assets_dir / filename
        if not download_image_to_file(raw_src, dest_path, server_port=server_port):
            continue

        saved_files = list(assets_dir.glob(f"{filename}*"))
        if not saved_files:
            continue
        saved_name = saved_files[0].name
        if saved_name in used_names:
            continue
        used_names.add(saved_name)

        rel_path = f"{rel_prefix}/{saved_name}"
        img["src"] = rel_path
        for attr in ("data-src", "data-original", "data-lazy-src", "data-type", "data-ratio", "data-w"):
            if img.has_attr(attr):
                del img[attr]
        downloaded += 1

    # 处理 background-image 中的微信图片 URL
    bg_pattern = re.compile(r"url\(['\"]?(https?://[^)'\"]+)['\"]?\)", re.IGNORECASE)
    for element in soup.find_all(style=True):
        style = element.get("style", "")
        if "url(" not in style.lower():
            continue

        def _replace_bg(match: re.Match) -> str:
            nonlocal downloaded
            bg_url = match.group(1)
            digest = hashlib.sha256(bg_url.encode("utf-8")).hexdigest()[:16]
            filename = f"bg_{digest}"
            dest_path = assets_dir / filename
            if not download_image_to_file(bg_url, dest_path, server_port=server_port):
                return match.group(0)
            saved_files = list(assets_dir.glob(f"{filename}*"))
            if not saved_files:
                return match.group(0)
            rel_path = f"{rel_prefix}/{saved_files[0].name}"
            downloaded += 1
            return f"url('{rel_path}')"

        element["style"] = bg_pattern.sub(_replace_bg, style)

    return str(soup), downloaded
