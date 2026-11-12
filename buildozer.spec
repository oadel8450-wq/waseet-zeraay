[app]

title = WASEET AL-KHAIR
package.name = waseetalkhair
package.domain = com.adelomar

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,db
source.exclude_dirs = .git,.venv,venv,bin,__pycache__

version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 35
android.minapi = 23

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
