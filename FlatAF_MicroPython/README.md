# FlatAF Device (ESP32C6 MicroPython) README

## Disclaimer
AstroAF makes no warranties or guarantees of any kind, express or implied. The scripts, applications, and processes included in the FlatAF_MicroPython project are provided "AS IS" and may be destructive to your file system or operating system if not used correctly. Users must exercise caution. If you do not fully understand the instructions or risks involved, STOP NOW or proceed entirely at your own risk.

## Table of Contents
- [FlatAF Device (ESP32C6 MicroPython) README](#flataf-device-esp32c6-micropython-readme)
  - [Disclaimer](#disclaimer)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Features](#core-features)
  - [Basic Use Guide](#basic-use-guide)
  - [Deployment](#deployment)
    - [Prerequisites](#prerequisites)
    - [USB Deploy Script](#usb-deploy-script)
    - [Manual Upload (Optional)](#manual-upload-optional)
  - [Configuration](#configuration)
    - [Wi-Fi Setup](#wi-fi-setup)
    - [AP Mode Recovery](#ap-mode-recovery)
  - [API Reference](#api-reference)
  - [Troubleshooting](#troubleshooting)
  - [REPL Cheat Sheet](#repl-cheat-sheet)
    - [Connecting to FlatAF via REPL](#connecting-to-flataf-via-repl)
    - [File System Management with mpremote](#file-system-management-with-mpremote)
    - [Manual FlatAF Control via REPL](#manual-flataf-control-via-repl)
    - [REPL Useful Keyboard Shortcuts](#repl-useful-keyboard-shortcuts)
    - [FlatAF REPL Test Suite](#flataf-repl-test-suite)
  - [Notes](#notes)
  - [System Status](#system-status)
  - [Licensing](#licensing)

## Overview
FlatAF is a professional-grade astrophotography flat panel controller, powered by a Seeed Studio XIAO ESP32C6 running MicroPython.

## Core Features
- Dynamic LED brightness control (16-bit precision)
- Wi-Fi based control via ASCOM Alpaca driver
- Automatic fallback to AP Mode if Wi-Fi is unavailable
- Simple Web UI for initial setup and network configuration
- Persistent brightness storage and recovery
- Fully headless operation after configuration

## Basic Use Guide
- See [README.md](../README.md) in the main FlatAF project for user-facing behavior and operation details:
  - Button toggle and long-press behavior
  - USB vs battery power usage
  - Grove power switch function
  - Antenna positioning for optimal Wi-Fi
  - Battery use and charging best practices

## Deployment

### Prerequisites
- Seeed Studio XIAO ESP32C6 board flashed with MicroPython 1.25.0 or later
- USB-C cable for initial deployment
- mpremote installed (pip install mpremote)
- Git repository cloned with FlatAF device firmware

### USB Deploy Script
Connect device to your computer.

Run:
```bash
./deploy.sh
```

This will:
- Wipe the filesystem (excluding wifi_config.json unless --full-wipe is used)
- Upload all necessary firmware files
- Soft reboot the device

By default, `deploy.sh` preserves your `wifi_config.json` file, so your Wi-Fi credentials are not lost during normal deployments. To fully wipe the filesystem, including `wifi_config.json`, use the `--full-wipe` flag:
```bash
./deploy.sh --full-wipe
```

### Manual Upload (Optional)
It is often useful to manually upload a single file's changes without full deployment.

To upload manually:
```bash
mpremote connect /dev/tty.usbmodem101 fs cp boot.py :
mpremote connect /dev/tty.usbmodem101 fs cp web_server.py :
mpremote connect /dev/tty.usbmodem101 fs cp led.py :
...
```
Perform a soft-reboot to ensure that device firmware is updated.  See [REPL Useful Keyboard Shortcuts](#repl-useful-keyboard-shortcuts) for information on reboot.

## Configuration

### Wi-Fi Setup
`wifi_config.json` is created automatically in the AP process for configuring SSID and Password for the network configuration.  It is removed with a long button press, effectively resetting FlatAF to AP mode.

If `wifi_config.json` exists:
- Device attempts to connect to the saved network.

If `wifi_config.json` is missing or invalid:
- Device automatically starts in Access Point (AP) Mode with SSID FlatAF-Setup and password flataf123.

### AP Mode Recovery
Connect to the FlatAF-Setup Wi-Fi network.

Open a browser and navigate to:
``` 
http://192.168.4.1:5555/
```

Enter new Wi-Fi credentials.

Device will save the configuration, reboot, and attempt connection to the new network.

## API Reference

- `GET /api/v1/covercalibrator/0/connected`  
  Returns whether the device is currently connected.

- `PUT /api/v1/covercalibrator/0/connected`  
  Sets the device connection state.

- `GET /api/v1/covercalibrator/0/brightness`  
  Returns the current LED brightness (0–65535).

- `PUT /api/v1/covercalibrator/0/brightness`  
  Sets the LED brightness.

- `PUT /api/v1/covercalibrator/0/setbrightness?Brightness=####`  
  Alternate form to set brightness explicitly via query parameter.

- `PUT /api/v1/covercalibrator/0/toggle`  
  Toggles the LED between ON and OFF.

- `PUT /api/v1/covercalibrator/0/calibratoron`  
  Turns the LED on.

- `PUT /api/v1/covercalibrator/0/calibratoroff`  
  Turns the LED off.

- `GET /api/v1/covercalibrator/0/maxbrightness`  
  Returns the maximum allowed LED brightness.

- `GET /api/v1/covercalibrator/0/driverinfo`  
  Returns device driver info string.

- `GET /api/v1/covercalibrator/0/interfaceversion`  
  Returns the Alpaca interface version supported.

- `GET /api/version`  
  Returns the FlatAF firmware version (if served by MicroPython).

- `GET /management/apiversions`  
  Lists the supported management API versions.

- `GET /` or `GET /index`  
  Loads the web interface homepage (used for Wi-Fi setup).

- `GET /astroAF_logo2.png`  
  Loads the logo asset used in the Web UI.

## Troubleshooting
- Device doesn't show up on network  
  Connect via USB and check logs. Re-enter Wi-Fi config if necessary via AP mode.
- Cannot reach setup page in AP Mode  
  Confirm Wi-Fi SSID is FlatAF-Setup and manually visit `http://192.168.4.1:5555/`.
- LED not responding  
  Check wiring and power supply. Confirm GPIO pin assignment in firmware matches your board.

## REPL Cheat Sheet
This cheat sheet provides quick reference commands for connecting to the FlatAF device via REPL and manually controlling behavior without needing Wi-Fi or NINA.

### Connecting to FlatAF via REPL
List Available USB Devices
```bash
ls /dev/tty.usb*
```

Connect to Device via mpremote
```bash
mpremote connect /dev/tty.usbmodem101
```

Successful connection will show the `>>>` REPL prompt.

### File System Management with mpremote
```bash
mpremote connect /dev/tty.usbmodem101 fs ls
mpremote connect /dev/tty.usbmodem101 fs cp myfile.py :
mpremote connect /dev/tty.usbmodem101 fs rm myfile.py
```

From REPL:
```python
import os
print(os.listdir())
```

### Manual FlatAF Control via REPL
```python
import ascom_api
ascom_api.set_device_brightness(32768)
ascom_api.turn_calibrator_on()
ascom_api.turn_calibrator_off()
ascom_api.fade_to_brightness(20000)
ascom_api.toggle_device()
ascom_api.get_device_status()
ascom_api.get_max_brightness()
```

### REPL Useful Keyboard Shortcuts
- Ctrl-D  
  Soft reboot the device
- Ctrl-E  
  Enter multi-line paste mode
- Ctrl-X  
  Exit multi-line paste mode
- Ctrl-]  
  Exit REPL session (via mpremote)

Use multi-line paste mode for copying larger code blocks cleanly into REPL.

### FlatAF REPL Test Suite

The full automated test script is located at:
```bash
test/device_tests.py
```

To run the tests:
```bash
mpremote connect /dev/tty.usbmodem101 run test/device_tests.py
```

This script verifies core LED control functionality and outputs results directly to REPL.

The HTTP endpoint tests are located at:
```bash
test/postman
```
In this folder you will find two files, a postman environment and collection.  See the README contained within this directory for specific documentation.

## Notes
- These commands do not require Wi-Fi.
- Ideal for debugging without NINA.
- Manual REPL behavior mirrors API endpoint behavior.



## System Status
- NINA reconnects after device reboot.
- Disconnect command turns LED off.

## Licensing
See the [FlatAF main project license](../LICENSE.md) for full licensing details.
