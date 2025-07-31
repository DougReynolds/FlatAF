"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Run functional tests for the LED class behavior and control
Website: https://astroaf.space
License: MIT
"""
import time
from led import LED
import constants

def run_tests():
    print("Starting LED tests...")

    # Create an LED instance in PWM mode (active_high)
    led = LED(pin_number=16, freq=5000, resolution=16, active_low=False)
    
    # Test 1: Initialization
    print("Test 1: Initialization")
    print("Initial brightness:", led.get_brightness())
    print("Initial status:", led.get_status())
    time.sleep(2)

    # Test 2: on() method
    print("Test 2: on() method")
    led.on()
    time.sleep(1)
    print("After on(): brightness:", led.get_brightness())
    print("After on(): status:", led.get_status())
    time.sleep(2)

    # Test 3: off() method
    print("Test 3: off() method")
    led.off()
    time.sleep(1)
    print("After off(): brightness:", led.get_brightness())
    print("After off(): status:", led.get_status())
    time.sleep(2)

    # Test 4: toggle() method
    print("Test 4: toggle() method")
    led.toggle()
    time.sleep(1)
    print("After toggle(): brightness:", led.get_brightness())
    print("After toggle(): status:", led.get_status())
    time.sleep(2)
    led.toggle()
    time.sleep(1)
    print("After second toggle(): brightness:", led.get_brightness())
    print("After second toggle(): status:", led.get_status())
    time.sleep(2)

    # Test 5: set_brightness() method
    print("Test 5: set_brightness(32768)")
    led.set_brightness(32768)
    time.sleep(1)
    print("After set_brightness(32768): brightness:", led.get_brightness())
    print("After set_brightness(32768): status:", led.get_status())
    time.sleep(2)

    # Test 6: fade_to() method (fade up)
    print("Test 6: fade_to(50000)")
    led.fade_to(50000)
    time.sleep(1)
    print("After fade_to(50000): brightness:", led.get_brightness())
    print("After fade_to(50000): status:", led.get_status())
    time.sleep(2)

    # Test 7: fade_to() method (fade down)
    print("Test 7: fade_to(0)")
    led.fade_to(0)
    time.sleep(1)
    print("After fade_to(0): brightness:", led.get_brightness())
    print("After fade_to(0): status:", led.get_status())
    time.sleep(2)

    print("LED tests completed.")

if __name__ == '__main__':
    run_tests()
