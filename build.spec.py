# -*- mode: ruby -*-
from collections import defaultdict
import os
import sys

block_cipher = None

a = Analysis(
    ['jarvis_gui_installer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('jarvis', 'jarvis'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors', 
        'requests',
        'urllib',
        'urllib.request',
        'json',
        'asyncio',
        'logging',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Jarvis_Setup',
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
    icon=None,
)

coll = COLLECT(
    exe,
    [('venv/Lib/site-packages/*', 'venv/Lib/site-packages', '__pycache__')],
    name='dist',
)