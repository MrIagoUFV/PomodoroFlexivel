# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\iagol\\OneDrive\\Documentos\\Projetos\\PomodoroWidget\\app\\pomodoro-timer\\src\\pomodoro_timer.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\iagol\\OneDrive\\Documentos\\Projetos\\PomodoroWidget\\app\\pomodoro-timer\\assets', 'assets')],
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
    name='Pomodoro Timer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\iagol\\OneDrive\\Documentos\\Projetos\\PomodoroWidget\\app\\pomodoro-timer\\assets\\icon.ico'],
)
