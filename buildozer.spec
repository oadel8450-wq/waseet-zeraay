
[app]

title = WASEET AL-KHAIR 3

package.name = waseetalkhair3
package.domain = org.aldlgroup

source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,atlas,ttf,json,db

version = 3.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE

android.api = 35

android.minapi = 23

android.ndk_api = 23

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

p4a.bootstrap = sdl2

[buildozer]

log_level = 2

warn_on_root = 0
