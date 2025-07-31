"""
Device Test Suite for FlatAF MicroPython Modules

Author: Doug Reynolds (AstroAF)
Description:
  This script provides a test suite for FlatAF device modules excluding web_server.py.
  It validates behavior of boot, brightness, LED, ASCOM API, constants, and other components.

Run Instructions:
  Upload and execute on device via mpremote:
    mpremote fs cp device_tests.py :
    mpremote run device_tests.py
"""

def test_boot_creates_wifi_config():
    import os
    try:
        # Backup if exists
        if "wifi_config.json" in os.listdir():
            os.rename("wifi_config.json", "wifi_config_backup.json")
        if "wifi_config.json" in os.listdir():
            os.remove("wifi_config.json")  # remove if still there
        import boot
        return run_test("boot - boot.py creates wifi_config if missing", lambda: "wifi_config.json" in os.listdir())
    finally:
        if "wifi_config_backup.json" in os.listdir():
            os.rename("wifi_config_backup.json", "wifi_config.json")

def test_main_runs_clean():
    return run_test("main - main.py runs without exception", lambda: __import__("main"))

def test_discovery_responder_start_stop():
    import uasyncio
    import discovery_responder

    async def run_responder_once():
        task = uasyncio.create_task(discovery_responder.discovery_responder())
        await uasyncio.sleep(0.1)
        task.cancel()
        return True

    return run_test(
        "discovery_responder.discovery_responder - responds once",
        lambda: uasyncio.run(run_responder_once())
    )


import ascom_api
import brightness
import led
import constants
import main
import sys

import sys
import uio as io  # MicroPython-compatible I/O module

def run_test(name, func):
    try:
        func()
        print()
        print(f"[TEST] {name}: *****PASS*****")
        print()
        return True
    except Exception as e:
        print()
        print(f"[TEST] {name}: *****FAIL***** - {e}")
        print()
        return False

def test_calibrator_on():
    return run_test("ascom_api.turn_calibrator_on - Calibrator ON", lambda: ascom_api.turn_calibrator_on())

def test_set_brightness_50():
    return run_test("ascom_api.set_device_brightness - Set Brightness to 50%", lambda: ascom_api.set_device_brightness(32768))

def test_set_midrange_brightness():
    return run_test("ascom_api.set_device_brightness - Set Brightness to Midrange (20000)", lambda: ascom_api.set_device_brightness(20000))

def test_toggle_off():
    return run_test("ascom_api.toggle_device - Toggle device OFF", lambda: ascom_api.toggle_device())

def test_toggle_on():
    return run_test("ascom_api.toggle_device - Toggle device ON", lambda: ascom_api.toggle_device())

def test_get_status():
    return run_test("ascom_api.get_device_status - Get Device Status", lambda: ascom_api.get_device_status())

def test_get_max_brightness():
    return run_test("ascom_api.get_max_brightness - Get Max Brightness", lambda: ascom_api.get_max_brightness())

def test_turn_calibrator_off():
    return run_test("ascom_api.turn_calibrator_off - Turn Calibrator OFF", lambda: ascom_api.turn_calibrator_off())

def test_clamp_brightness_high():
    return run_test("ascom_api.set_device_brightness - Clamp Brightness Above Max", lambda: ascom_api.set_device_brightness(999))

def test_clamp_brightness_low():
    return run_test("ascom_api.set_device_brightness - Clamp Brightness Below Zero", lambda: ascom_api.set_device_brightness(0))

def test_get_brightness_value():
    import ujson
    def check():
        brightness = ujson.loads(ascom_api.get_device_status())["brightness"]
        print(f"[INFO] Brightness value returned: {brightness}")
    return run_test(
        "ascom_api.get_device_status - Get Brightness Value",
        check
    )

def test_toggle_led():
    return run_test("led.LED.toggle - Toggle LED", lambda: led.LED(pin_number=2).toggle())

def test_set_led_brightness():
    return run_test("led.LED.set_brightness - Set LED Brightness", lambda: led.LED(pin_number=2).set_brightness(128))

def test_led_active_low():
    return run_test("led.LED.toggle - LED active_low True Toggle", lambda: led.LED(pin_number=2, active_low=True).toggle())

def test_led_pwm_false():
    return run_test("led.LED.toggle - LED PWM False Toggle", lambda: led.LED(pin_number=2, pwm=False).toggle())

def test_brightness_rapid_access():
    def rapid_access():
        import ujson
        for _ in range(10):
            ascom_api.set_device_brightness(100)
            brightness = ujson.loads(ascom_api.get_device_status())["brightness"]
            print(f"[INFO] Brightness value during rapid access: {brightness}")
    return run_test("ascom_api.set_device_brightness/get_device_status - Brightness Rapid Access", rapid_access)

def test_main_boot():
    return run_test("main - Main.py Boot Test", lambda: main)

def test_constants_usage():
    return run_test("constants.MAX_BRIGHTNESS - Constants Usage Check", lambda: print(constants.MAX_BRIGHTNESS))

def run_all():
    tests = [
        test_calibrator_on,
        test_set_brightness_50,
        test_set_midrange_brightness,
        test_toggle_off,
        test_toggle_on,
        test_get_status,
        test_get_max_brightness,
        test_turn_calibrator_off,
        test_clamp_brightness_high,
        test_clamp_brightness_low,
        test_get_brightness_value,
        test_toggle_led,
        test_set_led_brightness,
        test_led_active_low,
        test_led_pwm_false,
        test_brightness_rapid_access,
        test_boot_creates_wifi_config,
        test_main_runs_clean,
        test_discovery_responder_start_stop,
        test_main_boot,
        test_constants_usage,
    ]
    results = [test() for test in tests]
    passed = sum(results)
    total = len(results)
    print(f"\n[TEST] === TEST SUMMARY: {passed} of {total} tests passed ===")
    return all(results)

if __name__ == "__main__":
    success = run_all()
    if not success:
        sys.exit(1)