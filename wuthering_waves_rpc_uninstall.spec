# -*- mode: python ; coding: utf-8 -*-


uninstall = Analysis(
    ['src/bin/uninstall.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

uninstall_pyz = PYZ(uninstall.pure)

uninstall_exe = EXE(
    uninstall_pyz,
    uninstall.scripts,
    uninstall.binaries,
    uninstall.datas,
    [],
    uac_admin=True,
    name='Uninstall Wuthering Waves RPC',
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

