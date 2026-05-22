import os
import site
from PyInstaller.utils.hooks import collect_data_files, copy_metadata
import sys
sys.path.append(os.path.abspath('.'))
from constants import APP_VERSION

base_path = os.path.abspath('.')

site_packages = os.environ.get('SUPERPICKY_SITE_PACKAGES', '').strip()
if not site_packages:
    sp = [p for p in site.getsitepackages() if os.path.isdir(p)]
    site_packages = sp[0] if sp else site.getusersitepackages()

ultralytics_datas = collect_data_files('ultralytics')
imageio_datas = collect_data_files('imageio')
rawpy_datas = collect_data_files('rawpy')
pillow_heif_datas = collect_data_files('pillow_heif')

all_datas = [
    (os.path.join(base_path, 'models'), 'models'),
    (os.path.join(base_path, 'exiftools_win'), 'exiftools_win'),
    (os.path.join(base_path, 'img'), 'img'),
    (os.path.join(base_path, 'locales'), 'locales'),
    (os.path.join(base_path, 'locales', 'en.lproj'), 'en.lproj'),
    (os.path.join(base_path, 'locales', 'zh-Hans.lproj'), 'zh-Hans.lproj'),
    (os.path.join(base_path, 'birdid/data'), 'birdid/data'),
    (os.path.join(base_path, 'SuperBirdIDPlugin.lrplugin'), 'SuperBirdIDPlugin.lrplugin'),
]

all_datas.extend(ultralytics_datas)
all_datas.extend(imageio_datas)
all_datas.extend(rawpy_datas)
all_datas.extend(pillow_heif_datas)
all_datas.extend(copy_metadata('ultralytics'))
all_datas.extend(copy_metadata('imageio'))
all_datas.extend(copy_metadata('rawpy'))
all_datas.extend(copy_metadata('pillow_heif'))

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=[],
    datas=all_datas,
    hiddenimports=[
        'PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
        'ultralytics', 'torch', 'torchvision', 'PIL', 'cv2', 'numpy', 'yaml',
        'matplotlib', 'matplotlib.backends.backend_agg',
        'timm', 'imageio', 'rawpy', 'imagehash', 'pywt', 'pillow_heif',
        'core', 'core.burst_detector', 'core.config_manager', 'core.exposure_detector',
        'core.file_manager', 'core.flight_detector', 'core.focus_point_detector',
        'core.keypoint_detector', 'core.photo_processor', 'core.rating_engine', 'core.stats_formatter',
        'multiprocessing', 'multiprocessing.spawn',
        'tools.update_checker', 'packaging', 'packaging.version',
        'birdid', 'birdid.bird_identifier', 'birdid.ebird_country_filter',
        'birdid_server', 'server_manager', 'flask', 'flask.json',
        'cryptography', 'cryptography.fernet',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyi_rth_cv2.py'] if os.path.exists('pyi_rth_cv2.py') else [],
    excludes=['PyQt5', 'PyQt6', 'tkinter'],
    runtime_tmpdir='',  # 👈 就是加这一行！根治缓存问题
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

_icon_ico = os.path.join(base_path, 'img', 'icon.ico')
_exe_icon = _icon_ico if (sys.platform == 'win32' and os.path.exists(_icon_ico)) else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SuperPicky',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon=_exe_icon,
    # --------------- 以下 3 行是【防旧版本核心】---------------
    append_pkg=False,        # 禁用缓存复用
    clean=True,              # 每次运行自动清旧缓存
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='SuperPicky',
)

app = BUNDLE(
    coll,
    name='SuperPicky.app',
    icon=None,
    bundle_identifier='com.jamesphotography.superpicky',
    info_plist={'CFBundleName':'SuperPicky','CFBundleDisplayName':'SuperPicky','CFBundleVersion':APP_VERSION,'CFBundleShortVersionString':APP_VERSION,'NSHighResolutionCapable':True},
)