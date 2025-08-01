"""
Author: Douglas Reynolds
Project: FlatAF (MicroPython ESP32 Firmware)
Purpose: Runs onboard HTTP API for ASCOM-compatible brightness and status control
Website: https://astroaf.space
License: See LICENSE.md (CC BY-NC 4.0)
Copyright (c) 2025 Douglas Reynolds AstroAF
"""

import uasyncio as asyncio # type: ignore
import json
import time
import machine # type: ignore
from ascom_api import (
    get_device_status,
    set_device_brightness,
    fade_to_brightness,
    toggle_device,
    get_max_brightness,
    turn_calibrator_off,
    turn_calibrator_on,
    handle_apiversions
)
from constants import ALPACA_PORT

# Store connection state
connection_state = {"value": False}

async def handle_http(reader, writer):
    body = ""
    request_line = await reader.readline()
    headers = {}
    content_length = 0
    while True:
        line = await reader.readline()
        if not line or line == b"\r\n":
            break
        decoded = line.decode().strip()
        if ":" in decoded:
            key, value = decoded.split(":", 1)
            headers[key.strip().lower()] = value.strip()
            if key.strip().lower() == "content-length":
                try:
                    content_length = int(value.strip())
                except Exception as e:
                    print(f"[ERROR] location=web_server.py: handle_http Content-Length parse - {e}")

    request_line_str = request_line.decode().strip()
    parts = request_line_str.split()
    if len(parts) < 2:
        response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        await writer.awrite(response)
        await writer.aclose()
        return

    method = parts[0]
    path = parts[1]

    # Prepare default
    json_body = {}

    if method == "PUT" and content_length > 0:
        try:
            raw_body = await reader.read(content_length)
            json_body = json.loads(raw_body.decode())
            print(f"[DEBUG] Parsed JSON body: {json_body}")
        except Exception as e:
            print(f"[ERROR] location=web_server.py: handle_http JSON parse - {e}")
            json_body = {}

    global connection_state

    # === ASCOM API Versions ===
    if path.startswith("/management/apiversions") and method == "GET":
        body = handle_apiversions()
            
    # === Connected ===
    elif path.startswith("/api/v1/covercalibrator/0/connected"):
        if method == "GET":
            await asyncio.sleep(0.1)
            body = json.dumps({
                "Value": connection_state["value"],
                "ErrorNumber": 0,
                "ErrorMessage": ""
            })
        elif method == "PUT":
            try:
                new_state = json_body.get("Connected")
                client_transaction_id = json_body.get("ClientTransactionID", 0)
                if isinstance(new_state, bool):
                    if not new_state:
                        await asyncio.sleep(1.0)
                        turn_calibrator_off()
                    else:
                        turn_calibrator_on()
                    connection_state["value"] = new_state
                else:
                    raise ValueError("'Connected' must be boolean")
                body = json.dumps({
                    "Success": True,
                    "Connected": connection_state["value"],
                    "ClientTransactionID": client_transaction_id,
                    "ServerTransactionID": 999
                })
            except Exception as e:
                print(f"[ERROR] location=web_server.py: handle_http set connected - {e}")
                body = json.dumps({
                    "Success": False,
                    "ClientTransactionID": 0,
                    "ServerTransactionID": 999,
                    "ErrorMessage": "Exception occurred"
                })
        else:
            body = ""
            response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
            await writer.awrite(response)
            await writer.aclose()
            return
        
    # === Max Brightness ===
    elif path.startswith("/api/v1/covercalibrator/0/maxbrightness") and method == "GET":
        body = get_max_brightness()

    # === Driver Info ===
    elif path == "/api/v1/covercalibrator/0/driverinfo" and method == "GET":
        body = json.dumps({"Value": "FlatAF CoverCalibrator", "ErrorNumber": 0, "ErrorMessage": ""})

    # === Interface Version ===
    elif path == "/api/v1/covercalibrator/0/interfaceversion" and method == "GET":
        body = json.dumps({"Value": 2, "ErrorNumber": 0, "ErrorMessage": ""})

    # === Brightness Info ===
    elif path == "/api/v1/covercalibrator/0/brightness" and method == "GET":
        body = get_device_status()

    # === Set Brightness (Instant) ===
    elif path.startswith("/api/v1/covercalibrator/0/setbrightness") and method == "PUT":
        try:
            brightness_val = json_body.get("Brightness")
            if brightness_val is None:
                raise Exception("Missing 'Brightness' parameter in JSON body.")
            brightness = int(brightness_val)
            print(f"[DEVICE DEBUG] Setting brightness to {brightness}")
            body = set_device_brightness(brightness)
            print("[DEVICE DEBUG] Completed set_device_brightness")
        except Exception as e:
            print(f"[ERROR] location=web_server.py: set_brightness - {e}")
            body = json.dumps({"success": False, "error": "Exception occurred"})

    # === Fade to Brightness ===
    # elif path.startswith("/api/v1/covercalibrator/0/fadebrightness") and method == "PUT":
    #     try:
    #         media = req.get_media()  # This returns a dict of the parsed JSON payload
    #         brightness_val = media.get("Brightness")
    #         if brightness_val is None:
    #             raise Exception("Missing 'Brightness' parameter in JSON body.")
    #         brightness = int(brightness_val)
    #         print(f"[DEVICE DEBUG] Fading to {brightness}")
    #         fade_to_brightness(brightness)
    #         body = json.dumps({"success": True, "message": "Fade operation initiated"})
    #         resp.text = body
    #     except Exception as e:
    #         body = json.dumps({"success": False, "error": str(e)})
    #         resp.text = body
            
    # === Toggle Device On/Off ===
    elif path == "/api/v1/covercalibrator/0/toggle" and method == "PUT":
        try:
            body = toggle_device()
        except Exception as e:
            print(f"[ERROR] location=web_server.py: toggle_device - {e}")
            body = json.dumps({"success": False, "error": "Exception occurred"})

        response = (
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}"
        )
        await writer.awrite(response)
        await writer.aclose()
        return
    
    # === Toggle Device On ===
    elif path == "/api/v1/covercalibrator/0/calibratoron" and method == "PUT":
        try:
            body = turn_calibrator_on()
        except Exception as e:
            print(f"[ERROR] location=web_server.py: turn_calibrator_on - {e}")
            body = json.dumps({"success": False, "error": "Exception occurred"})

        response = (
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}"
        )
        await writer.awrite(response)
        await writer.aclose()
        return
    
    # === Toggle Device Off ===
    elif path == "/api/v1/covercalibrator/0/calibratoroff" and method == "PUT":
        try:
            body = turn_calibrator_off()
        except Exception as e:
            print(f"[ERROR] location=web_server.py: turn_calibrator_off - {e}")
            body = json.dumps({"success": False, "error": "Exception occurred"})

        response = (
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}"
        )
        await writer.awrite(response)
        await writer.aclose()
        return
    
    elif path == "/setup/wifi" and method == "POST":
        content = await reader.read(512)
        body = content.decode().split("\r\n\r\n", 1)[-1]
        params = {}
        for pair in body.split("&"):
            if "=" in pair:
                k, v = pair.split("=")
                params[k] = v.replace("+", " ")  # Handle spaces

        ssid = params.get("ssid")
        password = params.get("password")

        if ssid and password:
            try:
                with open("wifi_config.json", "w") as f:
                    json.dump({"ssid": ssid, "password": password}, f)
                print(f"[DEBUG] Saved Wi-Fi config for {ssid}")
                body = """
                <html>
                <head><title>Wi-Fi Config Saved</title></head>
                <body>
                    <h1>Wi-Fi Configuration Saved</h1>
                    <p>The device will reboot and attempt to connect to:</p>
                    <ul>
                        <li><strong>SSID:</strong> {}</li>
                    </ul>
                    <p>Please wait a few moments and then re-discover your device on the network.</p>
                </body>
                </html>
                """.format(ssid)
                await asyncio.sleep(2)
                machine.reset()
            except Exception as e:
                print(f"[ERROR] location=web_server.py: setup_wifi - {e}")
                body = "<html><body><h1>Error</h1><p>Exception occurred</p></body></html>"
        else:
            body = "<html><body><h1>Missing SSID or Password</h1></body></html>"
            
        content_bytes = body.encode("utf-8")
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(content_bytes)}\r\n"
            "Connection: close\r\n\r\n"
        )
        
        await writer.awrite(headers)
        await writer.awrite(content_bytes)
        await writer.aclose()
        return
    
    # === FlatAF Setup Static HTML ===
    elif path==("/setup") and method == "GET":
        html = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                "<title>FlatAF Setup</title>\n"
                "<style>\n"
                "body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }\n"
                "img { width: 200px; margin-bottom: 20px; }\n"
                "form { margin-top: 20px; }\n"
                "input[type=text], input[type=password] { padding: 8px; margin: 5px; width: 200px; }\n"
                "input[type=submit] { padding: 10px 20px; margin-top: 10px; }\n"
                ".small { font-size: 0.8em; color: #888; margin-top: 20px; }\n"
                ".password-container { position: relative; display: inline-block; }\n"
                ".password-container input { padding-right: 40px; }\n"
                ".toggle-eye { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; width: 20px; height: 20px; fill: #888; }\n"
                "</style>\n"
                "</head>\n"
                "<body>\n"
                "<img src='astroAF_logo2.png' alt='AstroAF Logo'/>\n"
                "<h1>Welcome to FlatAF</h1>\n"
                "<p>Thanks for using the FlatAF flat panel!</p>\n"
                "<p><a href='https://astroaf.space' target='_blank'>Visit astroaf.space</a></p>\n"
                "<p><a href='https://youtube.com/@astroaf' target='_blank'>Watch on YouTube</a></p>\n"
                "<h2>Wi-Fi Setup</h2>\n"
                "<form method='POST' action='/setup/wifi'>\n"
                "<input type='text' name='ssid' placeholder='Wi-Fi SSID'/><br>\n"
                "<div class='password-container'>\n"
                "<input type='password' id='password' name='password' placeholder='Wi-Fi Password'/>\n"
                "<svg class='toggle-eye' onclick='togglePassword()' viewBox='0 0 24 24'>\n"
                "<path id='eye-icon' d='M12 5c-7 0-11 7-11 7s4 7 11 7 11-7 11-7-4-7-11-7zm0 12c-2.8 0-5-2.2-5-5s2.2-5 5-5 5 2.2 5 5-2.2 5-5 5zm0-8c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3z'/>\n"
                "</svg>\n"
                "</div><br>\n"
                "<input type='submit' value='Save Wi-Fi'>\n"
                "</form>\n"
                "<div class='small'>\n"
                "<p><strong>Firmware Version:</strong> <span id='fw-version'>Loading...</span></p>\n"
                "</div>\n"
                "<script>\n"
                "function togglePassword() {\n"
                "  const input = document.getElementById('password');\n"
                "  const icon = document.getElementById('eye-icon');\n"
                "  const isHidden = input.type === 'password';\n"
                "  input.type = isHidden ? 'text' : 'password';\n"
                "  icon.setAttribute('d', isHidden ? 'M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12zm11 3a3 3 0 100-6 3 3 0 000 6z' : 'M12 5c-7 0-11 7-11 7s4 7 11 7 11-7 11-7-4-7-11-7zm0 12c-2.8 0-5-2.2-5-5s2.2-5 5-5 5 2.2 5 5-2.2 5-5 5zm0-8c-1.7 0-3 1.3-3 3s1.3 3 3 3 3-1.3 3-3-1.3-3-3-3z');\n"
                "}\n"
                "fetch('/api/version')\n"
                ".then(r => r.json())\n"
                ".then(d => { document.getElementById('fw-version').innerText = d.version; })\n"
                ".catch(e => { document.getElementById('fw-version').innerText = 'Unknown'; });\n"
                "</script>\n"
                "</body>\n"
                "</html>\n"
            )
        content_bytes = html.encode("utf-8")
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(content_bytes)}\r\n"
            "Connection: close\r\n\r\n"
        )
        await writer.awrite(headers)
        await writer.awrite(content_bytes)
        await writer.aclose()
        return
    
    # === Handling the logo image path for setup screen ===
    elif path == "/astroAF_logo2.png" and method == "GET":
        try:
            with open("astroAF_logo2.png", "rb") as f:
                image_data = f.read()
            response = (
                "HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n"
                f"Content-Length: {len(image_data)}\r\nConnection: close\r\n\r\n"
            )
            await writer.awrite(response)
            await writer.awrite(image_data)
            await writer.aclose()
            return
        except Exception as e:
            print(f"[ERROR] location=web_server.py: get_logo_image - {e}")
            error_response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
            await writer.awrite(error_response)
            await writer.aclose()
            return
        
    # === Respond to / or /index with plain text ===
    elif path in ["/", "/index"] and method == "GET":
        response_code = 200
        response_body = b"FlatAF is online and responding."
        content_type = "text/plain"
        
    elif path == "/api/version" and method == "GET":
        try:
            with open("version.json", "r") as f:
                version_info = json.load(f)
            body = json.dumps({"success": True, "version": version_info.get("version", "unknown")})
        except Exception as e:
            print(f"[ERROR] location=web_server.py: get_version - {e}")
            body = json.dumps({"success": False, "error": "Exception occurred"})
        response = (
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}"
        )
        await writer.awrite(response)
        await writer.aclose()
        return

    else:
        response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        await writer.awrite(response)
        await writer.aclose()
        return

    # Send response
    response = (
        "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}"
    )
    await writer.awrite(response)
    await writer.aclose()
    return


async def start_server(port=ALPACA_PORT):
    try:
        with open("version.json", "r") as f:
            version_info = json.load(f)
        version = version_info.get("version", "unknown")
    except Exception as e:
        print(f"[ERROR] location=web_server.py: start_server - {e}")
        version = "unknown"
    server = await asyncio.start_server(handle_http, "0.0.0.0", port)
    print(f"[Web Server] Running version {version} on port {port}...")
    return server
