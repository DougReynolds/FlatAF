#!/bin/bash

###################
# run command
# chmod +x flataf_test.sh
# ./flataf_test.sh
###################

# Soft reboot the device before running tests
mpremote connect /dev/tty.usbmodem101 reset
sleep 2

# Structured test suite
TESTS=(
  "Calibrator ON (default max brightness)|ascom_api.turn_calibrator_on()"
  "Set Brightness to 50%|ascom_api.set_device_brightness(32768)"
  "Fade to brightness 20000|ascom_api.fade_to_brightness(20000)"
  "Toggle device OFF|ascom_api.toggle_device()"
  "Toggle device ON|ascom_api.toggle_device()"
  "Get Device Status|ascom_api.get_device_status()"
  "Get Max Brightness|ascom_api.get_max_brightness()"
  "Turn Calibrator OFF|ascom_api.turn_calibrator_off()"
  "Clamp Brightness Above Max|import brightness; brightness.set_brightness(999)"
  "Clamp Brightness Below Zero|import brightness; brightness.set_brightness(0)"
  "Get Brightness Value|import brightness; print(brightness.get_brightness())"
  "Toggle LED|import led; led.toggle()"
  "Set LED Brightness|import led; led.set_brightness(128)"
  "LED active_low True Toggle|import led; led_obj = led.LED(pin_number=2, active_low=True); led_obj.toggle()"
  "LED PWM False Toggle|import led; led_obj = led.LED(pin_number=2, pwm=False); led_obj.toggle()"
  "Brightness Rapid Access|import brightness; [brightness.set_brightness(100) or brightness.get_brightness() for _ in range(10)]"
  "Main.py Boot Test|import main"
  "Constants Usage Check|import constants; print(constants.MAX_BRIGHTNESS)"
)

echo "Starting FlatAF Automated Test Suite..."
for TEST_CASE in "${TESTS[@]}"; do
  IFS='|' read -r NAME CODE <<< "$TEST_CASE"
  echo -n "Running test: $NAME... "
  OUTPUT=$(mpremote connect /dev/tty.usbmodem101 exec "import ascom_api; $CODE" 2>&1)
  if [ $? -eq 0 ]; then
    echo "PASS"
  else
    echo "FAIL"
    echo "Error: $OUTPUT"
  fi
  sleep 2
done

echo "FlatAF Automated Test Suite Complete."