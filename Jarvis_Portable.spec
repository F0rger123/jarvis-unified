# Jarvis_Portable.spec - PyInstaller spec for single-file exe
# Run: pyinstaller Jarvis_Portable.spec

block_cipher = None

a = Analysis(
    ['jarvis/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('jarvis/.env.example', 'jarvis'),
        ('jarvis/ui/web_ui.py', 'jarvis/ui'),
        ('jarvis/core/jarvis.py', 'jarvis/core'),
        ('jarvis/memory', 'jarvis/memory'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'requests',
        'urllib3',
        'google_generativeai',
        'google.api_core',
        'asyncio',
        'logging',
        'json',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter','matplotlib','pandas','numpy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Jarvis_Portable',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window!
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Collect all files into one folder
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='dist',
)