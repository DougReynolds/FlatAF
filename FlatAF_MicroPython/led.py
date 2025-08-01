"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Controls LED brightness and behavior using PWM for the FlatAF device
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
"""

from machine import Pin, PWM # type: ignore
import time
from brightness import load_brightness, save_brightness

"""Class representing the FlatAF LED device."""
class LED:
    DEFAULT_PWM_FREQ = 1000  # Default frequency in Hz
    
    # Initialize the LED with optional PWM, resolution, and active low logic.
    #
    # Parameters:
    #     pin_number (int): The GPIO pin number used to control the LED.
    #     pwm (bool): Enable PWM for brightness control (default is True).
    #     resolution (int): Bit resolution for PWM duty cycle (default is 16).
    #     active_low (bool): If True, inverts LED logic (default is False).
    def __init__(self, pin_number, pwm=True, resolution=16, active_low=False):
        print(f"[INFO] Initializing LED on pin {pin_number}")
        # Default frequency in Hz
        self.pwm_freq = self.DEFAULT_PWM_FREQ
        self.pin_number = pin_number
        self.active_low = active_low
        self.brightness = 0
        self.pwm_enabled = pwm
        self.resolution = resolution
        self.max_value = ((1 << resolution) - 1)  // 2
        self.pin = Pin(pin_number, Pin.OUT)

        if pwm:
            self.pwm = PWM(Pin(pin_number))
        else:
            self.pwm = None
                        
    """Enable PWM on the configured pin."""
    def enable_pwm(self):
        self.pwm = PWM(self.pin)
        self.pwm.freq(self.pwm_freq)
        self.pwm_enabled = True

    """Set the LED brightness to a specified value within allowed range."""
    def set_brightness(self, value):
        print(f"[INFO] Set brightness to {value}")
        value = max(0, min(value, self.max_value))
        self.brightness = value

        if value == 0:
            # Turn off and disable PWM if brightness is 0
            if self.pwm_enabled:
                self.pwm.deinit()
                self.pwm_enabled = False
            self.pin.init(Pin.OUT)
            self.pin.value(0 if self.active_low else 1)
        else:
            # If not already using PWM, enable it
            if not self.pwm_enabled:
                self.enable_pwm()
            duty = self.max_value - value if self.active_low else value
            print(f"[INFO] PWM enabled with duty {duty}")
            self.pwm.duty_u16(duty)

    """Return the current brightness level of the LED."""
    def get_brightness(self):
        return self.brightness
    
    """Reinitialize PWM on the assigned pin."""
    def reinitialize_pwm(self):
        self.pwm = PWM(Pin(self.pin_number))
        self.pwm.freq(self.pwm_freq)

    """Toggle the LED on or off based on its current brightness."""
    def toggle(self):
        if self.brightness > 0:
            self.led_off()
            print(f"[INFO] LED toggled OFF")
        else:
            self.reinitialize_pwm()
            self.set_brightness(self.max_value)
            print(f"[INFO] LED toggled ON")
    
    """Turn off the LED and save the current brightness."""
    def led_off(self):
        save_brightness(self.get_brightness())
        self.set_brightness(0)
        self.pwm.deinit()
        pin = Pin(self.pin_number, Pin.OUT)
        pin.value(0)
        
    """Turn on the LED with the last saved brightness."""
    def led_on(self):
        restored_brightness = load_brightness()
        print(f"[INFO] LED ON with restored brightness {restored_brightness} on pin {self.pin_number}")
        self.set_brightness(restored_brightness)

    """Return the current status of the LED as 'ON' or 'OFF'."""
    def get_status(self):
        return "ON" if self.brightness > 0 else "OFF"

    """Fade the LED brightness smoothly to a target value."""
    def fade_to(self, target_brightness, step=400, delay=0.01):
        target_brightness = max(0, min(target_brightness, self.max_value))
        current = self.brightness
        direction = 1 if target_brightness > current else -1
        for val in range(current, target_brightness, direction * step):
            self.set_brightness(val)
            time.sleep(delay)
        self.set_brightness(target_brightness)
