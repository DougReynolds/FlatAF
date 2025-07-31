#!/bin/bash

###################
# run command
# chmod +x deploy.sh
# ./deploy.sh
# OR
# ./deploy.sh --full-wipe
###################

PORT="/dev/tty.usbmodem101"

# Optional full wipe: use --full-wipe to erase filesystem before deployment
FULL_WIPE=false
if [[ "$1" == "--full-wipe" ]]; then
  FULL_WIPE=true
fi

# Files to deploy to the ESP32
FILES=(
  "boot.py"
  "web_server.py"
  "ascom_api.py"
  "led.py"
  "constants.py"
  "brightness.py"
  "button.py"
  "main.py"
  "astroAF_logo2.png"
  "version.json"
  "discovery_responder.py"
)

VERSION=$(git describe --tags --abbrev=0)
echo "{\"version\": \"$VERSION\"}" > version.json

if [ "$FULL_WIPE" = true ]; then
  echo "Wiping file system on $PORT..."
  mpremote connect $PORT fs rm :
else
  echo "Preserving existing files on $PORT..."
fi

# Backup wifi_config.json if it exists
echo "Checking for wifi_config.json..."
mpremote connect $PORT fs cat wifi_config.json > /tmp/wifi_config.json 2>/dev/null

echo "📦 Uploading files..."
for file in "${FILES[@]}"
do
    if [ -f "$file" ]; then
        echo "➕ Uploading $file"
        mpremote connect $PORT fs cp "$file" :
    else
        echo "Skipping missing file: $file"
    fi
done

# Restore wifi_config.json if it was backed up
if [ -f /tmp/wifi_config.json ]; then
    echo "Restoring wifi_config.json..."
    mpremote connect $PORT fs cp /tmp/wifi_config.json :wifi_config.json
    rm /tmp/wifi_config.json
fi

echo "Rebooting device..."
mpremote connect $PORT reset

echo "FlatAF deployment complete."
