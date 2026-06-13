# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置 - WeRSS 桌面版后端打包

用法:
    cd scripts
    pyinstaller werss.spec

输出:
    scripts/dist/werss-gui/
"""

from pathlib import Path

ROOT_DIR = Path(SPECPATH).parent

block_cipher = None

hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.loops.asyncio',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.websockets.websockets_impl',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi.responses',
    'fastapi.staticfiles',
    'starlette.responses',
    'starlette.routing',
    'sqlalchemy.sql.default_comparator',
    'passlib.handlers.bcrypt',
    'playwright',
    'playwright.async_api',
    'playwright.sync_api',
    'greenlet',
    'apscheduler.schedulers.background',
    'apscheduler.triggers.cron',
    'apscheduler.triggers.interval',
    'PIL._tkinter_finder',
    'multipart',
    'email.mime.multipart',
    'email.mime.text',
]

a = Analysis(
    [str(ROOT_DIR / 'desktop' / '__main__.py')],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=[
        (str(ROOT_DIR / 'static'), 'static'),
        (str(ROOT_DIR / 'public'), 'public'),
        (str(ROOT_DIR / 'config.example.yaml'), '.'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [('X utf8_mode=1', None, 'OPTION')],
    exclude_binaries=True,
    name='werss-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='werss-gui',
)
