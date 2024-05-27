# -*- mode: python ; coding: utf-8 -*-


setup = Analysis(
    ['index.py'],
    pathex=[],
    binaries=[],
    datas=[('dist/Wuthering Waves RPC.exe', '.'), ('assets/logo.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

setup_pyz = PYZ(setup.pure)

setup_exe = EXE(
    setup_pyz,
    setup.scripts,
    setup.binaries,
    setup.datas,
    [],
    uac_admin=True,
    name='Wuthering Waves RPC Setup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\logo.ico'],
)