# -----------------------------------------------------------------------------
# Author: Douglas Reynolds
# Project: FlatAF Alpaca Driver
# File: dynamic_discovery.py
# Description: Alpaca network discovery module for FlatAF CoverCalibrator
# -----------------------------------------------------------------------------
# dynamic_discovery.py

import socket
import json
import time
import logging

DISCOVERY_PORT = 32227
DISCOVERY_TIMEOUT = 3  # seconds
DISCOVERY_MAGIC = 0x4C504143  # 'ALPACA'

def discover_flataf():
    """
    Broadcasts an Alpaca discovery message and listens for a FlatAF device.
    Returns the device BaseURL if found, otherwise raises Exception.
    """
    discovery_message = {
        "AlpacaDiscovery": 1
    }

    sock = None
    try:
        # Set up UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(DISCOVERY_TIMEOUT)

        # Send discovery broadcast
        payload = json.dumps(discovery_message).encode('utf-8')
        sock.sendto(payload, ('<broadcast>', DISCOVERY_PORT))
        logging.info("[Discovery] Broadcast sent.")

        start_time = time.time()

        while time.time() - start_time < DISCOVERY_TIMEOUT:
            try:
                data, addr = sock.recvfrom(1024)
                response = json.loads(data.decode('utf-8'))

                # Match device based on Manufacturer + DeviceType
                if (response.get('AlpacaPort') and
                    response.get('Manufacturer', '').lower() == 'astroaf' and
                    response.get('DeviceType', '').lower() == 'covercalibrator'):

                    ip = addr[0]
                    port = response['AlpacaPort']
                    base_url = f"http://{ip}:{port}/api/v1/covercalibrator/0"
                    logging.info(f"[Discovery] FlatAF found at {base_url}")
                    return base_url

            except socket.timeout:
                break
            except Exception as e:
                logging.error(f"[Discovery] Error parsing discovery response: {e}", extra={"location": "dynamic_discovery.discover_flataf"})
                continue

    except Exception as e:
        logging.error(f"[Discovery] Error during broadcast: {e}", extra={"location": "dynamic_discovery.discover_flataf"})

    finally:
        if sock:
            sock.close()

    # No valid device found after timeout
    raise Exception("dynamic_discovery.discover_flataf: FlatAF device not found on the network after broadcast timeout. Ensure the device is powered on and connected to the same subnet.")
