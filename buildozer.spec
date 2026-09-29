[app]
title = Entrenador Piano
package.name = entrenadorpiano
package.domain = org.entrenador

source.dir = .
source.include_exts = py, png, jpg, kv, atlas

version = 1.0
requirements = python3, pygame, mido, python-rtmidi

orientation = landscape
fullscreen = 1

# API de Android
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# Permisos nativos de Android para el puerto USB OTG
android.permissions = INTERNET, USB_PERMISSION
android.hardware.usb.host = True

[buildozer]
log_level = 2
warn_on_root = 1
