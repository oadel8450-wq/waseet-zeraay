
[app]

title = WASEET AL-KHAIR 3

package.name = waseetalkhair3
package.domain = com.adelomar

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,db,txt,json
source.exclude_dirs = .git,.venv,venv,bin,__pycache__

version = 3.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b

android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.private_storage = True

android.gradle_dependencies =

android.enable_androidx = True

android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

[buildozer]

log_level = 2

warn_on_root = 1
