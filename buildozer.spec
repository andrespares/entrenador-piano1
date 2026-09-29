[app]

# (str) Title of your application
title = Entrenador de Piano

# (str) Package name
package.name = entrenadorpiano

# (str) Package domain (needed for android packaging)
package.domain = org.entrenador

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# NOTA: Usamos kivy, mido y pyjnius para compatibilidad total con Android 16/33
requirements = python3==3.11.0, kivy==2.3.0, mido, pyjnius

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# Permisos para conectar dispositivos USB MIDI
android.permissions = INTERNET, USB_PERMISSION

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required. 24 es Android 7.0 (Soporte MIDI USB nativo completo)
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk apps
android.skip_update = False

# (bool) If True, then accept all SDK licenses
android.accept_sdk_license = True

# (str) The Android arch to build for (arm64-v8a para móviles modernos)
android.archs = arm64-v8a

# (bool) Enable Android Auto backup feature (Android API >= 23)
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1

