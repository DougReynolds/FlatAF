"""Module for ASCOM Alpaca driver operations."""

# -----------------------------------------------------------------------------
# setup.py - FlatAF Alpaca Driver Setup
#
# Author: Douglas Reynolds
# Project: FlatAF - Open Source Flat Panel for Astrophotography
# Website: https://astroaf.space
# -----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# setup.py - Device setup endpoints.
#
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# GitHub: https://github.com/ASCOMInitiative/AlpycaDevice
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022-2024 Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 27-Dec-2022   rbd V0.1 Initial edit. Simply say no GUI.
# 30-Dec-2022   rbd V0.1 Device number captured and sent to responder
#
from covercalibrator import CovercalibratorMetadata
from falcon import Request, Response # type: ignore
from shr import PropertyResponse, DeviceMetadata, log_request

class devsetup:
    def on_get(self, req: Request, resp: Response, devnum: int):
        version = CovercalibratorMetadata.Version
        html = f"""
        <html>
        <head><title>FlatAF Setup</title></head>
        <body>
            <img src="/resources/images/astroAF_logo2.png" alt="AstroAF" width="200"/>
            <h1>Welcome to FlatAF</h1>
            <p>Thanks for using the FlatAF flat panel!</p>
            <p><a href="https://astroaf.space" target="_blank">Visit astroaf.space</a></p>
            <p><a href="https://youtube.com/@astroaf" target="_blank">Watch on YouTube</a></p>
            <p style="margin-top:20px; font-size:0.9em; color:#888;">Driver Version: {version}</p>
        </body>
        </html>
        """
        resp.content_type = "text/html"
        resp.text = html

