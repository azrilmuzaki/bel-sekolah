# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('api-ms-win-core-path-l1-1-0.dll', '.')],
    datas=[('jam1.mp3', '.'), ('jam2.mp3', '.'), ('jam3.mp3', '.'), ('jam4.mp3', '.'), ('jam5.mp3', '.'), ('jam6.mp3', '.'), ('jam7.mp3', '.'), ('istirahat1.mp3', '.'), ('istirahat2.mp3', '.'), ('pulang.mp3', '.'), ('api-ms-win-core-path-l1-1-0.dll', '.')],
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
    name='Bel Sekolah',
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
