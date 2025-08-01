"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Main application entry point that initializes hardware, handles button logic, and starts web and discovery services
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
Copyright (c) 2025 Douglas Reynolds AstroAF
"""


# main.py
import uasyncio as asyncio # type: ignore
import time
import constants
import brightness
import os
import machine # type: ignore

from ascom_api import led_device as led
from button import Button
from led import LED
import web_server
from discovery_responder import discovery_responder

"""
Handles long button press by performing a factory reset.
Deletes the Wi-Fi configuration file and resets the device.
"""
def handle_long_press():
    print("[INFO] Factory reset triggered.")
    try:
        os.remove("wifi_config.json")
        print("[INFO] wifi_config.json deleted.")
    except Exception as e:
        print(f"[ERROR] location = main.py.handle_long_press: Error deleting config: {e}")
    machine.reset()

# Initialize hardware
button = Button(pin_number=0, on_press=led.toggle, on_long_press=handle_long_press, debounce_time=0.05)

BRIGHTNESS_FILE = constants.BRIGHTNESS_FILE

"""Function to load brightness."""
def load_brightness():
    last_saved_brightness = brightness.load_brightness()
    return last_saved_brightness

"""Function to save brightness."""
def save_brightness(value):
    brightness.save_brightness(value)

"""Asynchronous loop that polls the button every 50 ms
and toggles the LED if pressed.
"""
async def main_loop():
    while True:
        if button.check_press():
            led.toggle()
            print("Button pressed. LED status:", led.get_status())
        await asyncio.sleep(0.05)

"""
Launches the discovery responder and web server, then starts the main loop.
"""
async def run_all():
    # Start Discovery Responder
    asyncio.create_task(discovery_responder())
    
    """
    1) Start the async web server on port ALPACA_PORT
    2) Run the main hardware loop concurrently
    """
    await web_server.start_server(port=constants.ALPACA_PORT)
    led.led_off()
    await main_loop()

"""Main function that starts the event loop."""
def main():
    # Wi-Fi is already connected by boot.py, so we just run the event loop
    asyncio.run(run_all())

if __name__ == "__main__":
    main()
