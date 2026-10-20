
[app]

title = Flowers & Love
package.name = flowersandlove
package.domain = org.flowersandlove

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

[android]

android.api = 35
android.minapi = 23
android.ndk = 27c
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

android.permissions =

p4a.branch = master

