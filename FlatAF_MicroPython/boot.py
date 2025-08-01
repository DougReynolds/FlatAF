"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Initializes external antenna, connects to Wi-Fi or starts AP mode, and ensures brightness file exists
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
"""
# boot.py -- run on boot-up
import os
import constants
import network
import time
import json
from machine import Pin # type: ignore

# External antenna enable logic
Pin(3, Pin.OUT).value(0)   # GPIO3 to LOW
Pin(14, Pin.OUT).value(1)  # GPIO14 to HIGH

files = os.listdir()

def load_wifi_config():
    try:
        with open("wifi_config.json", "r") as f:
            creds = json.load(f)
            return creds.get("ssid"), creds.get("password")
    except Exception as e:
        print("Wi-Fi config not found or invalid:", e)
        return None, None

def start_ap_mode():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="FlatAF-Setup", password="flataf123", authmode=network.AUTH_WPA_WPA2_PSK)
    print("[INFO] Access Point started:", ap.ifconfig())

# --- Run Wi-Fi STA mode ---
ssid, password = load_wifi_config()

if ssid and password:
    try:
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        print("[INFO] Activating STA:", sta.active())

        try:
            sta.connect(ssid, password)
            max_wait = 20
            wait_count = 0
            while not sta.isconnected() and wait_count < max_wait:
                time.sleep(0.5)
                wait_count += 1

            if sta.isconnected():
                print("[INFO] Connected:", sta.ifconfig())
            else:
                raise OSError("[ERROR] location = boot.py.sta.connect: Failed to connect after timeout")

        except Exception as e:
            print(f"[ERROR] location = boot.py.sta.connect: {e}")
            try:
                import os
                os.remove("wifi_config.json")
                print("[INFO] Deleted wifi_config.json to allow reconfiguration")
            except Exception as delete_error:
                print(f"[WARN] location = boot.py.os.remove: {delete_error}")
            start_ap_mode()
    except Exception as e:
        print(f"[FATAL] location = boot.py.network.WLAN: {e}")
        start_ap_mode()
else:
    print("No Wi-Fi config. Starting AP mode...")
    start_ap_mode()

# Create default brightness file if it doesn't exist
if constants.BRIGHTNESS_FILE not in files:
    print("[INFO] Brightness file not found. Creating default file...")
    try:
        with open(constants.BRIGHTNESS_FILE, "wb") as f:
            f.write(constants.DEFAULT_BRIGHTNESS.to_bytes(2, "big"))
        print("[INFO] Default brightness saved:", constants.DEFAULT_BRIGHTNESS)
    except Exception as e:
        print(f"[ERROR] location = boot.py.brightness.init: {e}")
else:
    print("[INFO] Brightness file exists.")
