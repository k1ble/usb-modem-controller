USB Modem Controller
A simple utility for managing USB modes on Android devices via ADB. 
It allows you to switch between USB tethering (RNDIS) and file transfer (MTP), reset the USB connection, and automatically restore the last selected mode when the device is reconnected.

Features
Switch to USB tethering mode (rndis)

Switch to file transfer mode (mtp)

Reset USB gadget (resetUsbGadget)

Automatically restore the last used mode on device connection

Minimize to system tray

Log events to logger.log

Requirements
Python 3.10 or later
ADB (Android Debug Bridge) available in PATH

Python packages:
pystray
Pillow

Usage
Connect your Android device via USB.
Enable USB debugging on the device.
run main.py

Platforms
Tested on Windows 11 with Poco M5.
Linux and macOS have not been tested. Theoretically it should work (ADB and Python are cross-platform), but no guarantees.
On Linux, pystray may require additional system libraries.


Also Apple devices (iPhone) are not supported. The utility relies on ADB, which is only available for Android.