from core.models import Article
from core.db import DB
from datetime import datetime, timezone
import json
import csv
import zipfile
import os
import shutil
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from core.print import print_success, print_error, print_warning
from jobs.notice import sys_notice
from core.paths import resolve_export_target_dir
from core.export_history import append_export_record, save_last_export_result


@dataclass
class ArticleExportResult:
    success: bool = False
    pdf_ok: bool = False
    pdf_error: Optional[str] = None
    md_ok: bool = False
    md_images: int = 0
    exported_labels: list[str] = field(default_factory=list)


@dataclass
class ExportStats:
    attempted: int = 0
    exported: int = 0
    pdf_ok: int = 0
    pdf_failed: list[dict[str, str]] = field(default_factory=list)
    md_ok: int = 0
    md_images: int = 0

    def to_summary(self) -> dict[str, Any]:
        return {
            "attempted": self.attempted,
            "exported": self.exported,
            "pdf_ok": self.pdf_ok,
            "pdf_failed_count": len(self.pdf_failed),
            "pdf_failed_titles": [item["title"] for item in self.pdf_failed[:20]],
            "pdf_failed_details": self.pdf_failed[:20],
            "md_ok": self.md_ok,
            "md_images": self.md_images,
        }

    def build_message(self, *, zip_created: bool, zip_path: str = "") -> str:
        parts: list[str] = []
        if zip_created:
            parts.append(f"导出完成，共成功 {self.exported} 篇文章")
            if zip_path:
                parts.append(f"文件：{os.path.basename(zip_path)}")
        else:
            parts.append("导出未生成文件")

        if self.pdf_failed:
            parts.append(f"PDF 失败 {len(self.pdf_failed)} 篇")
            preview = "、".join(item["title"][:20] for item in self.pdf_failed[:3])
            if preview:
                parts.append(f"失败示例：{preview}")
        if self.md_ok and self.md_images:
            parts.append(f"Markdown 已本地化 {self.md_images} 张图片")
        return "；".join(parts)


def _get_server_port() -> int:
    port = os.environ.get("PORT")
    if port:
        return int(port)
    from core.config import cfg

    return int(cfg.get("port", 8001))


def _create_export_staging_dir(target_dir: Path) -> Path:
    """为单次导出创建独立临时目录，避免把历史残留文件打进压缩包。"""
    staging_dir = target_dir / f".export_{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    staging_dir.mkdir(parents=True, exist_ok=True)
    return staging_dir


def _cleanup_staging_dir(staging_dir: Path) -> None:
    if staging_dir.exists():
        shutil.rmtree(staging_dir, ignore_errors=True)


def _pack_staging_to_zip(staging_dir: Path, zip_path: Path) -> None:
    """仅打包本次导出临时目录中的文件。"""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(staging_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, staging_dir)
                zipf.write(file_path, arc_name)


def process_single_article(
    art,
    add_title,
    remove_images,
    remove_links,
    export_md,
    export_docx,
    export_json,
    export_csv,
    export_pdf,
    docx_path,
    writer,
    server_port: int,
) -> ArticleExportResult:
    """
    处理单篇文章的导出逻辑。
    """
    from core.common.file_tools import sanitize_filename

    result = ArticleExportResult()
    if not (export_md or export_docx or export_json or export_csv or export_pdf):
        return result

    print(art.id, art.title, art.id)

    name = datetime.fromtimestamp(art.publish_time, tz=timezone.utc).strftime("%Y%m%d") + "_" + art.title
    filename = sanitize_filename(name) + ".docx"
    json_filename = sanitize_filename(name) + ".json"
    md_filename = sanitize_filename(name) + ".md"
    pdf_filename = sanitize_filename(name) + ".pdf"
    assets_folder = sanitize_filename(name) + "_assets"

    json_content = {
        "id": art.id,
        "url": art.url,
        "title": art.title,
        "pic_url": art.pic_url,
        "description": art.description,
        "status": art.status,
        "publish_time": art.publish_time,
    }

    try:
        html_content = art.content if hasattr(art, "content") and art.content else ""

        md_generated = False
        if export_md and html_content:
            try:
                from tools.mdtools.html2doc import html_to_markdown_file

                md_full_path = f"{docx_path}{md_filename}"
                assets_dir = Path(docx_path) / assets_folder
                config = {
                    "remove_images": remove_images,
                    "remove_links": remove_links,
                    "localize_images": not remove_images,
                    "assets_dir": str(assets_dir),
                    "assets_rel_prefix": assets_folder,
                    "server_port": server_port,
                }
                document_title = art.title if add_title else None
                success = html_to_markdown_file(html_content, md_full_path, document_title, config)
                if success:
                    print_success(f"Markdown文件已生成: {md_filename}")
                    md_generated = True
                    result.md_ok = True
                    if assets_dir.exists():
                        result.md_images = len([p for p in assets_dir.iterdir() if p.is_file()])
                        if result.md_images:
                            print_success(f"Markdown 图片已保存到 {assets_folder}/，共 {result.md_images} 张")
                else:
                    print_error(f"Markdown文件生成失败: {md_filename}")
            except ImportError as error:
                print_error(f"html2doc依赖缺失: {error}")
            except Exception as error:
                print_error(f"HTML转Markdown失败: {error}")

        pdf_generated = False
        if export_docx or export_pdf:
            pdf_full_path = f"{docx_path}{pdf_filename}"
            try:
                from tools.mdtools.pdf import url_to_pdf
                from core.config import cfg

                browser_type = cfg.get("gather.browser_type", "webkit")
                url = art.url if not html_content else f"http://127.0.0.1:{server_port}/views/print/{art.id}"
                pdf_ok = url_to_pdf(url, pdf_full_path, browser_type=str(browser_type))
                if not pdf_ok or not os.path.exists(pdf_full_path):
                    raise RuntimeError("PDF 文件未生成，请确认 Playwright 浏览器已安装且文章正文可访问")
                print_success(f"PDF文件已生成: {pdf_filename}")
                pdf_generated = True
                result.pdf_ok = True
            except ImportError as error:
                result.pdf_error = f"PDF 依赖缺失: {error}"
                print_error(result.pdf_error)
            except Exception as error:
                result.pdf_error = str(error)
                print_error(f"PDF转换失败: {error}")

        docx_generated = False
        if export_docx and pdf_generated:
            try:
                from tools.mdtools.pdf_extractor import pdf_to_docx

                pdf_full_path = f"{docx_path}{pdf_filename}"
                docx_full_path = f"{docx_path}{filename}"
                success = pdf_to_docx(pdf_full_path, docx_full_path)
                if success:
                    print_success(f"DOCX文件已生成: {filename}")
                    docx_generated = True
                else:
                    print_error(f"DOCX文件生成失败: {filename}")
            except ImportError as error:
                print_error(f"pdf2docx依赖缺失: {error}")
            except Exception as error:
                print_error(f"PDF转DOCX失败: {error}")

        json_generated = False
        if export_json:
            try:
                json_full_path = f"{docx_path}{json_filename}"
                with open(json_full_path, "w", encoding="utf-8") as handle:
                    handle.write(json.dumps(json_content, ensure_ascii=False, indent=2))
                json_generated = True
            except Exception as error:
                print_error(f"JSON文件保存失败: {error}")

        csv_generated = False
        if export_csv and writer:
            try:
                writer.writerow([
                    art.title,
                    art.url,
                    datetime.fromtimestamp(art.publish_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                ])
                csv_generated = True
            except Exception as error:
                print_error(f"CSV记录失败: {error}")

        if json_generated:
            result.exported_labels.append("JSON")
        if md_generated:
            result.exported_labels.append("MD")
        if docx_generated:
            result.exported_labels.append("DOCX")
        if pdf_generated:
            result.exported_labels.append("PDF")
        if csv_generated:
            result.exported_labels.append("CSV")

        if export_pdf and not pdf_generated:
            result.pdf_error = result.pdf_error or "PDF 生成失败"

        if result.exported_labels:
            print_success(f"文件已保存: {', '.join(result.exported_labels)} - {name}")
            result.success = True
        else:
            print_error(f"没有文件被成功导出: {name}")
        return result

    except Exception as error:
        print_error(f"保存文档失败: {error}")
        result.pdf_error = result.pdf_error or str(error)
        return result


def process_articles(
    session,
    mp_id=None,
    doc_id=None,
    page_size=10,
    page_count=1,
    add_title=True,
    document_id=None,
    remove_images=False,
    remove_links=False,
    export_md=True,
    export_docx=True,
    export_json=True,
    export_csv=True,
    export_pdf=True,
    docx_path="./data/docs/",
    writer=None,
) -> ExportStats:
    stats = ExportStats()
    server_port = _get_server_port()
    page_index = 0
    is_break = False
    while True:
        if is_break:
            break
        if page_count != 0 and page_index >= page_count:
            break

        query = session.query(Article).filter(Article.content != None).where(Article.status == 1)
        if mp_id:
            query = query.where(Article.mp_id.in_(mp_id.split(",")))
        if doc_id:
            query = query.where(Article.id.in_(doc_id))
            is_break = True

        query = query.order_by(Article.publish_time.desc(), Article.id.desc())
        if not is_break:
            query = query.offset(page_index * page_size).limit(page_size)
        page_index += 1
        arts = query.all()

        if not arts:
            break

        for art in arts:
            stats.attempted += 1
            item_result = process_single_article(
                art,
                add_title,
                remove_images,
                remove_links,
                export_md,
                export_docx,
                export_json,
                export_csv,
                export_pdf,
                docx_path,
                writer,
                server_port,
            )
            if item_result.success:
                stats.exported += 1
            if item_result.pdf_ok:
                stats.pdf_ok += 1
            elif export_pdf and item_result.pdf_error:
                stats.pdf_failed.append({
                    "title": art.title or art.id,
                    "reason": item_result.pdf_error,
                })
            if item_result.md_ok:
                stats.md_ok += 1
                stats.md_images += item_result.md_images

    return stats


def export_md_to_doc(
    mp_id: str = None,
    doc_id: list = None,
    page_size: int = 10,
    page_count: int = 1,
    add_title=True,
    remove_images: bool = True,
    remove_links: bool = False,
    export_md: bool = False,
    export_docx: bool = False,
    export_json: bool = False,
    export_csv: bool = False,
    export_pdf: bool = True,
    domain="",
    zip_filename=None,
    zip_file=True,
    export_dir: str = None,
):
    session = DB.get_session()
    if mp_id is None:
        raise ValueError("公众号ID不能为空")

    target_dir = resolve_export_target_dir(mp_id, export_dir)
    staging_dir = _create_export_staging_dir(target_dir)
    docx_path = str(staging_dir) + os.sep

    from core.paths import normalize_export_mp_id

    save_last_export_result({
        "mp_id": normalize_export_mp_id(mp_id) or "_all",
        "status": "running",
        "message": "导出任务进行中，请稍候…",
        "zip_path": "",
        "summary": {},
    })

    csv_file = None
    writer = None
    keep_staging = False
    try:
        if export_csv:
            csv_filename = f"{docx_path}articles.csv"
            csv_file = open(csv_filename, "w", newline="", encoding="utf-8")
            writer = csv.writer(csv_file)
            writer.writerow(["标题", "链接", "发布时间"])

        stats = process_articles(
            session=session,
            mp_id=mp_id,
            doc_id=doc_id,
            page_size=page_size,
            page_count=page_count,
            add_title=add_title,
            remove_images=remove_images,
            remove_links=remove_links,
            export_md=export_md,
            export_docx=export_docx,
            export_json=export_json,
            export_csv=export_csv,
            export_pdf=export_pdf,
            docx_path=docx_path,
            writer=writer,
        )

        if csv_file:
            csv_file.close()
            csv_file = None
            print_success(f"CSV 文件已保存为 {docx_path}articles.csv")

        zip_created = False
        final_zip_path = ""
        summary = stats.to_summary()

        if stats.exported > 0:
            if not zip_filename:
                zip_basename = f"exported_articles_{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}.zip"
            else:
                zip_basename = zip_filename if zip_filename.endswith(".zip") else f"{zip_filename}.zip"
            zip_full_path = str(target_dir / zip_basename)

            if zip_file is False:
                keep_staging = True
                exported_files = []
                for root, _, files in os.walk(staging_dir):
                    for file in files:
                        exported_files.append(os.path.join(root, file))
                _persist_export_result(
                    mp_id=mp_id,
                    status="success",
                    message=stats.build_message(zip_created=True),
                    zip_path="",
                    summary=summary,
                )
                return exported_files

            try:
                if os.path.exists(zip_full_path):
                    os.remove(zip_full_path)
                _pack_staging_to_zip(staging_dir, Path(zip_full_path))

                zip_created = True
                final_zip_path = zip_full_path
                print_success(f"所有文件已打包为: {zip_full_path}")

                try:
                    append_export_record(
                        file_path=zip_full_path,
                        mp_id=mp_id,
                        summary=summary,
                    )
                    print_success("导出记录已写入历史")
                except Exception as history_error:
                    print_error(f"写入导出记录失败: {history_error}")

                download_link = domain + zip_full_path
                print_success(f"转换完成 {download_link}")
                sys_notice(stats.build_message(zip_created=True, zip_path=zip_full_path))
            except Exception as error:
                print_error(f"打包文件失败: {error}")
                _persist_export_result(
                    mp_id=mp_id,
                    status="failed",
                    message=f"打包失败: {error}",
                    zip_path="",
                    summary=summary,
                )
                return stats

        message = stats.build_message(zip_created=zip_created, zip_path=final_zip_path)
        status = "success" if zip_created else "failed"
        if stats.pdf_failed and zip_created:
            status = "partial"
        elif stats.pdf_failed and not zip_created:
            status = "failed"
            if export_pdf and not export_md and not export_json and not export_csv and not export_docx:
                message = (
                    f"PDF 导出全部失败（{len(stats.pdf_failed)} 篇）。"
                    "请确认已安装 Playwright 浏览器，且文章正文已采集完成。"
                )

        _persist_export_result(
            mp_id=mp_id,
            status=status,
            message=message,
            zip_path=final_zip_path,
            summary=summary,
        )

        if stats.pdf_failed:
            print_warning(message)
            sys_notice(message, title="导出结果", tag="导出通知")

        print_success(f"导出完成，共处理 {stats.exported} 篇文章")
        return stats
    finally:
        if csv_file:
            csv_file.close()
        if not keep_staging:
            _cleanup_staging_dir(staging_dir)


def _persist_export_result(
    *,
    mp_id: Optional[str],
    status: str,
    message: str,
    zip_path: str,
    summary: dict[str, Any],
) -> None:
    from core.paths import normalize_export_mp_id

    save_last_export_result({
        "mp_id": normalize_export_mp_id(mp_id) or "_all",
        "status": status,
        "message": message,
        "zip_path": zip_path,
        "summary": summary,
    })
