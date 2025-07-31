#!/bin/bash

# Author: Douglas Reynolds
# Project: FlatAF_Alpaca (ASCOM Alpaca CoverCalibrator Driver)
# Purpose: Updates FlatAF_Alpaca project version in version.json
# Website: https://astroaf.space
# License: MIT

# === update_version.sh ===
# Updates FlatAF_Alpaca project version in version.json

###################
# run command
# chmod +x update_version.sh
# ./update_version.sh
###################

set -e

# === Get Git Version ===
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0-dev")

# === Write Version.json ===
echo "{\"version\": \"$VERSION\"}" > "./device/version.json"
echo "Injected firmware version: $VERSION"