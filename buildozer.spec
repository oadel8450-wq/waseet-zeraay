
[app]

title = WASEET AL-KHAIR 3

package.name = waseetalkhair3
package.domain = org.adelgru

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf,json,db

version = 3.0.0

# Python and Kivy Requirements
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Android Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE

# Android SDK
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

# Android Architectures
android.archs = arm64-v8a,armeabi-v7a

# Accept Android SDK License
android.accept_sdk_license = True

# Python-for-Android
p4a.bootstrap = sdl2
p4a.branch = master

# Android Build Settings
android.enable_androidx = True

# Include application files
source.include_patterns = *.py,*.kv,*.png,*.jpg,*.jpeg,*.atlas,*.ttf,*.json,*.db


[buildozer]

log_level = 2
warn_on_root = 0
