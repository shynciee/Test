# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Screenshot.py'],
    pathex=[],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=[
        'keyboard',
        'pyautogui',
        'pyperclip',
        'PIL',
        'dotenv',
        'google.generativeai'
    ],
    hookspath=[],
    hooksconfig={},
    # Xóa dòng runtime_hooks đi vì nó có thể gây ra lỗi không cần thiết khi gỡ lỗi
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyApp_Debug', # Đổi tên để phân biệt với phiên bản cũ
    debug=True, # Bật chế độ debug
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # <<< THAY ĐỔI QUAN TRỌNG NHẤT >>>
    console=True, # Đặt là True để hiện cửa sổ dòng lệnh
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
    upx=True,
    upx_exclude=[],
    name='MyApp_Debug',
)
