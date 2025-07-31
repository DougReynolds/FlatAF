"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Responds to Alpaca discovery broadcasts with device identity info
Website: https://astroaf.space
License: MIT
"""
import uasyncio as asyncio # type: ignore
import usocket as socket # type: ignore
import json
from constants import ALPACA_PORT

DISCOVERY_PORT = 32227


async def discovery_responder():
    """
    Asynchronously listens for Alpaca discovery broadcasts on the local network
    and sends a response containing device information if a valid request is received.
    """
    print("[INFO] [Discovery Responder] Starting...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(('0.0.0.0', DISCOVERY_PORT))
        sock.setblocking(False)

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                message = data.decode('utf-8')

                if "AlpacaDiscovery" in message:

                    response = {
                        "AlpacaPort": ALPACA_PORT,
                        "Manufacturer": "AstroAF",
                        "DeviceType": "CoverCalibrator",
                        "DeviceName": "FlatAF"
                    }

                    payload = json.dumps(response).encode('utf-8')
                    sock.sendto(payload, addr)

            except (OSError, Exception):
                await asyncio.sleep(0.1)

    except Exception as e:
        print(f"[ERROR] location = discovery_responder.py.discovery_responder: {e}")

    finally:
        sock.close()
