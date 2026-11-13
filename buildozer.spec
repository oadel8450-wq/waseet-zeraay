
[app]

title = WASEET AL-KHAIR 3
package.name = waseetalkhair
package.domain = org.aldlgroup

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

version = 3.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

# Android configuration
android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 35
android.minapi = 23
android.ndk = 27c
android.ndk_api = 23

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

android.enable_androidx = True

# Android build settings
android.private_storage = True

android.allow_backup = True

android.copy_libs = 1

android.release_artifact = apk

# Java configuration
android.add_compile_options = -fPIC

# Application settings
android.entrypoint = org.kivy.android.PythonActivity

# Include project files
source.exclude_dirs = .git, .github, .buildozer, bin, __pycache__

# Build settings
p4a.branch = develop

[buildozer]

log_level = 2

warn_on_root = 1
