"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Defines the brightness file name used for writing and retrieving brightness config data,
         and sets default and maximum brightness constants for LED control
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
"""
BRIGHTNESS_FILE = "brightness.dat"
DEFAULT_BRIGHTNESS = 32767
# Step size used when adjusting brightness smoothly
DEFAULT_STEP_SIZE_16 = 400
MAX_BRIGHTNESS = 65534

# Default port for Alpaca API communication
ALPACA_PORT = 5555