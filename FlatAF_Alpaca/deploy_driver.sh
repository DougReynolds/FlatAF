#!/bin/bash

#
# Author: Douglas Reynolds
# Project: FlatAF (ASCOM Alpaca Driver)
# Purpose: Packages the FlatAF_Alpaca driver into a deployable ZIP archive
# Website: https://astroaf.space
# License: See LICENSE.md (ASCOM and CC BY-NC 4.0)
# 

####################
# run command
# chmod +x deploy_driver.sh
# ./deploy_driver.sh
####################

set -e

PROJECT_ROOT="FlatAF_Alpaca"
STAGING_DIR="staging"

# === Get Git Version ===
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0-dev")

# === Write Version.json ===
echo "{\"version\": \"$VERSION\"}" > "./device/version.json"
echo "Injected firmware version: $VERSION"

# === Prepare Staging ===
rm -rf "$STAGING_DIR"
mkdir "$STAGING_DIR"

# === Copy project into staging (excluding junk) ===
rsync -av \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='.DS_Store' \
  --exclude='*.md' \
  --exclude='*.log' \
  --exclude='*.log.*' \
  --exclude='staging' \
  --exclude='deploy_driver.sh' \
  --exclude='update_version.sh' \
  --exclude='.gitignore' \
  --exclude='.venv' \
  "." "$STAGING_DIR/$PROJECT_ROOT/"

# === Create ZIP ===
cd "$STAGING_DIR"
DEPLOY_ZIP="FlatAF_Alpaca_Deploy_${VERSION}.zip"
zip -r "$DEPLOY_ZIP" "$PROJECT_ROOT"

# === Cleanup temp project copy ===
cd ..
rm -rf "$STAGING_DIR/$PROJECT_ROOT"

echo "Deployment ZIP created inside $STAGING_DIR/$DEPLOY_ZIP"