#!/usr/bin/env python3
"""
WeRSS Electron 桌面应用一键构建脚本

步骤:
1. 检查环境
2. 构建前端 -> static/
3. PyInstaller 打包 Python 后端
4. electron-builder 生成安装包

用法:
    python scripts/build_electron.py
    python scripts/build_electron.py --skip-frontend
    python scripts/build_electron.py --skip-backend
    python scripts/build_electron.py --publish never
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


class Color:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"


def print_step(title: str, current: int, total: int) -> None:
    print(f"\n{Color.CYAN}{Color.BOLD}[{current}/{total}] {title}{Color.RESET}")
    print("=" * 60)


def print_success(message: str) -> None:
    print(f"{Color.GREEN}✓ {message}{Color.RESET}")


def print_error(message: str) -> None:
    print(f"{Color.RED}✗ {message}{Color.RESET}", file=sys.stderr)


def print_warning(message: str) -> None:
    print(f"{Color.YELLOW}⚠ {message}{Color.RESET}")


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    print(f"$ {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=False)
        return result.returncode == 0
    except FileNotFoundError:
        print_error(f"命令未找到: {cmd[0]}")
        return False


def check_command(cmd: str) -> bool:
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def resolve_python(root: Path) -> Path:
    candidates = [
        root / ".venv" / "bin" / "python",
        root / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return Path(sys.executable)


class ElectronBuilder:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.root = Path(__file__).resolve().parent.parent
        self.scripts_dir = self.root / "scripts"
        self.electron_dir = self.root / "electron"
        self.resources_dir = self.root / "resources"
        self.platform = platform.system().lower()

    def check_environment(self) -> bool:
        print_step("检查环境依赖", 4, 1)
        required = {
            "node": "Node.js",
            "npm": "npm",
        }
        missing = []
        for cmd, label in required.items():
            if check_command(cmd):
                print_success(f"{label} 已安装")
            else:
                print_error(f"{label} 未安装")
                missing.append(cmd)

        python_exe = resolve_python(self.root)
        if not python_exe.exists() and not check_command("python3"):
            missing.append("python")

        try:
            subprocess.run(
                [str(python_exe), "-m", "PyInstaller", "--version"],
                capture_output=True,
                check=True,
            )
            print_success("PyInstaller 已安装")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print_error("PyInstaller 未安装，请执行: pip install pyinstaller")
            missing.append("pyinstaller")

        if missing:
            return False
        return True

    def build_frontend(self) -> bool:
        print_step("构建前端", 4, 2)
        python_exe = resolve_python(self.root)
        return run_command([str(python_exe), str(self.scripts_dir / "build.py")])

    def build_backend(self) -> bool:
        print_step("打包 Python 后端", 4, 3)
        python_exe = resolve_python(self.root)

        dist_dir = self.scripts_dir / "dist" / "werss-gui"
        build_dir = self.scripts_dir / "build" / "werss-gui"
        for path in (dist_dir, build_dir):
            if path.exists():
                shutil.rmtree(path)
                print_success(f"已清理 {path}")

        if not run_command(
            [str(python_exe), "-m", "PyInstaller", "werss.spec"],
            cwd=self.scripts_dir,
        ):
            return False

        backend_resources = self.resources_dir / "backend" / "werss-gui"
        if backend_resources.exists():
            shutil.rmtree(backend_resources)
        if self.resources_dir.joinpath("backend").exists():
            # 兼容旧版扁平目录结构
            for child in self.resources_dir.joinpath("backend").iterdir():
                if child.name != "werss-gui":
                    if child.is_dir():
                        shutil.rmtree(child)
                    else:
                        child.unlink()
        shutil.copytree(dist_dir, backend_resources)
        print_success(f"后端已复制到 {backend_resources}")
        return True

    def build_electron(self) -> bool:
        print_step("构建 Electron 安装包", 4, 4)
        if not run_command(["npm", "install"], cwd=self.electron_dir):
            return False

        build_cmd = ["npm", "run", "build", "--", "--publish", self.args.publish]
        if not run_command(build_cmd, cwd=self.electron_dir):
            return False

        dist_dir = self.electron_dir / "dist"
        if dist_dir.exists():
            print_success(f"构建产物目录: {dist_dir}")
            for item in sorted(dist_dir.iterdir()):
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"  - {item.name} ({size_mb:.1f} MB)")
                elif not item.name.startswith("."):
                    print(f"  - {item.name}/")
        return True

    def build(self) -> bool:
        print(f"\n{Color.BOLD}WeRSS Electron 构建工具{Color.RESET}")
        print(f"平台: {self.platform}")
        print(f"项目目录: {self.root}\n")

        steps = [
            ("环境检查", self.check_environment),
            ("前端构建", self.build_frontend if not self.args.skip_frontend else lambda: (print_warning("跳过前端构建"), True)[1]),
            ("后端打包", self.build_backend if not self.args.skip_backend else lambda: (print_warning("跳过后端打包"), True)[1]),
            ("Electron 打包", self.build_electron),
        ]

        for name, func in steps:
            if not func():
                print_error(f"构建失败: {name}")
                return False

        print(f"\n{Color.GREEN}{Color.BOLD}✓ 全部构建完成{Color.RESET}\n")
        return True


def main() -> int:
    parser = argparse.ArgumentParser(description="WeRSS Electron 一键构建")
    parser.add_argument("--skip-frontend", action="store_true", help="跳过前端构建")
    parser.add_argument("--skip-backend", action="store_true", help="跳过后端 PyInstaller 打包")
    parser.add_argument(
        "--publish",
        choices=["never", "onTag", "always"],
        default="never",
        help="electron-builder 发布模式",
    )
    args = parser.parse_args()
    builder = ElectronBuilder(args)
    return 0 if builder.build() else 1


if __name__ == "__main__":
    raise SystemExit(main())
