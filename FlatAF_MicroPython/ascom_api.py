"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Implements Alpaca-compliant API endpoints for FlatAF device control
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
"""
import json
from led import LED
from constants import MAX_BRIGHTNESS
from brightness import load_brightness

# Shared LED instance for Alpaca API; initialized with PWM control
led_device = LED(pin_number=16, pwm=True, resolution=16, active_low=False)

def handle_apiversions():
    try:
        response = {
            "Value": [1, 2],
            "ClientTransactionID": 0,
            "ServerTransactionID": 999,
            "ErrorNumber": 0,
            "ErrorMessage": ""
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.handle_apiversions: " + str(e)
        }
    return json.dumps(response)
        
def get_max_brightness():
    """
    Returns the maximum brightness supported by the device.
    """
    try:
        response = {
            "success": True,
            "max_brightness": MAX_BRIGHTNESS
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.get_max_brightness: " + str(e)
        }
    return json.dumps(response)

def get_device_status():
    """
    Returns the current LED status and brightness as a JSON response.
    """
    try:
        response = {
            "success": True,
            "status": led_device.get_status(),
            "brightness": led_device.get_brightness()
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.get_device_status: " + str(e)
        }
    return json.dumps(response)

def set_device_brightness(value):
    """Sets the device brightness to the specified integer value (0 to MAX_BRIGHTNESS)."""
    try:
        value = int(value)
        if not (0 <= value <= MAX_BRIGHTNESS):
            raise ValueError(f"Brightness value out of range (0-{MAX_BRIGHTNESS})")
        led_device.set_brightness(value)
        response = {
            "success": True,
            "brightness": led_device.get_brightness()
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.set_device_brightness: " + str(e)
        }
    return json.dumps(response)

def toggle_device():
    """Toggles the LED ON/OFF state and returns the updated status."""
    try:
        led_device.toggle()
        response = {
            "success": True,
            "status": led_device.get_status()
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.toggle_device: " + str(e)
        }
    return json.dumps(response)

def turn_calibrator_on():
    """Turns the LED ON using the last known (or default) brightness."""
    try:
        response = {
            "success": True,
            "status": led_device.get_status()
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.turn_calibrator_on: " + str(e)
        }
    return json.dumps(response)

def turn_calibrator_off():
    """Turns the LED OFF by setting brightness to 0."""
    try:
        led_device.led_off()
        response = {
            "success": True,
            "status": led_device.get_status()
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.turn_calibrator_off: " + str(e)
        }
    return json.dumps(response)

def fade_to_brightness(value):
    """
    Fades the LED to the specified brightness level using PWM smoothing.
    Does not persist intermediate brightness values.
    """
    try:
        value = int(value)
        if not (0 <= value <= MAX_BRIGHTNESS):
            raise ValueError(f"Brightness value out of range (0-{MAX_BRIGHTNESS})")
        led_device.fade_to(value)
        response = {
            "success": True,
            "brightness": led_device.get_brightness()
        }
    except Exception as e:
        response = {
            "success": False,
            "error": "location = ascom_api.py.fade_to_brightness: " + str(e)
        }
    return json.dumps(response)
