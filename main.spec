# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

# Incluir todos os arquivos da pasta recursos (ico, png, gif etc.)
recursos = [
    ('recursos\\*.ico', 'recursos'),
    ('recursos\\*.png', 'recursos'),
    ('recursos\\*.gif', 'recursos'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=recursos,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
