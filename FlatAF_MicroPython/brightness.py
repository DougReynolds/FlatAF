"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Handles loading and saving of panel brightness from flash memory
Website: https://astroaf.space
License: MIT
"""
import constants

BRIGHTNESS_FILE = constants.BRIGHTNESS_FILE
last_saved_brightness = None  # Global to keep track of last saved brightness

def load_brightness():
    """Load brightness from flash file."""
    try:
        with open(BRIGHTNESS_FILE, "rb") as f:
            data = f.read()
            if len(data) >= 2:
                value = int.from_bytes(data[0:2], "big")
                print(f"[INFO] location = brightness.py.load_brightness: Loaded brightness value: {value}")
                return value
    except Exception as e:
        print(f"[ERROR] location = brightness.py.load_brightness: {e}")
    return constants.DEFAULT_BRIGHTNESS

def save_brightness(value):
    """Save brightness ensuring value stays within the allowed range (0–MAX_BRIGHTNESS)."""
    global last_saved_brightness
    try:
        # Clamp brightness value from 0 to MAX_BRIGHTNESS
        value = max(0, min(constants.MAX_BRIGHTNESS, value))
        with open(BRIGHTNESS_FILE, "wb") as f:
            f.write(value.to_bytes(2, "big"))
        last_saved_brightness = value
        print(f"[INFO] location = brightness.py.save_brightness: Brightness saved: {value}")
    except Exception as e:
        print(f"[ERROR] location = brightness.py.save_brightness: {e}")
