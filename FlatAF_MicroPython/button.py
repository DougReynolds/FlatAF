"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Handles button press and long-press detection logic for user input
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
"""
import machine # type: ignore
import time

"""
Class representing a physical button on a GPIO pin.

This class provides detection of short and long presses using edge detection and
customizable debounce and duration thresholds.
"""

class Button:
    """
    Initialize the Button instance.

    Args:
        pin_number (int): GPIO pin number to which the button is connected.
        on_press (callable, optional): Callback to execute on short press. Defaults to None.
        on_long_press (callable, optional): Callback to execute on long press. Defaults to None.
        debounce_time (float, optional): Debounce delay in seconds. Defaults to 0.05.
        long_press_duration (float, optional): Duration in seconds to qualify as a long press. Defaults to 5.0.

    Note:
        The button is assumed to be active-low (pressed = 0) with an internal pull-up.
    """
    def __init__(
        self, pin_number,
        on_press=None,
        on_long_press=None,
        debounce_time=0.05,
        long_press_duration=5.0
        ):
        self.button = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_time = debounce_time
        self.last_state = self.button.value()
        self.on_press = on_press
        self.on_long_press = on_long_press
        self.long_press_duration = long_press_duration
        self._press_time = None

    def check_press(self):
        current_state = self.button.value()
        now = time.time()

        # Detect falling edge (button press)
        if self.last_state == 1 and current_state == 0:
            self._press_start = now
            self._pressed = True
            print("[INFO] Button press detected (falling edge)")

        # Detect rising edge (button release)
        elif self.last_state == 0 and current_state == 1:
            print("[INFO] Button release detected (rising edge)")
            if self._pressed:
                press_duration = now - self._press_start
                print(f"[INFO] Button press duration: {press_duration:.2f}s")
                if press_duration >= self.long_press_duration:
                    print("[INFO] Long press detected")
                    if self.on_long_press:
                        self.on_long_press()
                else:
                    print("[INFO] Short press detected")
                    if self.on_press:
                        self.on_press()
                self._pressed = False

        self.last_state = current_state


    def wait_for_press(self):
        """Block until the button is pressed."""
        print("[INFO] Waiting for button press...")
        while self.button.value() == 1:
            time.sleep(self.debounce_time)
