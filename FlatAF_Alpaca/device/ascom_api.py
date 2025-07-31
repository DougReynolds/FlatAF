"""Module for ASCOM Alpaca driver operations."""

##############################
# Author: Doug Reynolds
# Project: FlatAF Alpaca Driver
# File: ascom_api.py
# Description: Client interface for communicating with the ASCOM Alpaca driver.
##############################


import requests # type: ignore

"""Client interface for communicating with the ASCOM Alpaca driver."""
class ASCOMDeviceClient:
    """Gets the device connection status."""
    def get_connection_status(self, client_id=0, client_transaction_id=1234):
        url = f"{self.base_url}/connected"
        params = {
            "ClientID": client_id,
            "ClientTransactionID": client_transaction_id
        }
        try:
            response = requests.get(url, params=params, timeout=2)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Failed to get connection status: {e}")
            return {
                "ClientTransactionID": client_transaction_id,
                "ServerTransactionID": -1,
                "ErrorNumber": 1,
                "ErrorMessage": f"Failed to get connection status: {e}"
            }

    """Sets the device connection state."""
    def set_device_connected(self, state, client_transaction_id=1234):
        url = f"{self.base_url}/connected"
        payload = {
            "Connected": state,
            "ClientTransactionID": client_transaction_id
        }
        try:
            response = requests.put(url, json=payload, timeout=2)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Failed to set device connection: {e}")
            return {
                "ClientTransactionID": client_transaction_id,
                "ServerTransactionID": -1,
                "ErrorNumber": 1,
                "ErrorMessage": f"Failed to set device connection: {e}"
            }

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
