###########################
# Author: Douglas Reynolds
# Project: FlatAF Alpaca Driver
# Purpose: Auto-installs and registers the FlatAF Alpaca driver to run on user login
# Website: https://astroaf.space
# License: See LICENSE.md (ASCOM and CC BY-NC 4.0)
# Copyright (c) 2025 Douglas Reynolds AstroAF
###########################
# === register_task.ps1 ===
# FlatAF Alpaca Driver Auto-Installer for Windows

Write-Host "Starting FlatAF Alpaca Driver Setup..."

# === 1. Set Project Paths ===
$ProjectRoot = Get-Location
$VenvPath = "$ProjectRoot\alpaca-env"
$DevicePath = "$ProjectRoot\device"
$RequirementsPath = "$DevicePath\requirements.txt"

# === 2. Create Virtual Environment (if missing) ===
if (!(Test-Path $VenvPath)) {
    Write-Host "Creating Python virtual environment..."
    python -m venv alpaca-env
} else {
    Write-Host "Virtual environment already exists."
}

# === 3. Activate venv and Install Requirements ===
Write-Host "Installing Python dependencies..."

& "$VenvPath\Scripts\pip.exe" install -r "$RequirementsPath"

# === 4. Setup Scheduled Task ===
$TaskName = "FlatAF Alpaca Driver"

# Prepare action to activate venv and launch app.py
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -Command `"& '$VenvPath\Scripts\Activate.ps1'; cd '$DevicePath'; python app.py`""

# Trigger at user logon
$Trigger = New-ScheduledTaskTrigger -AtLogOn

# Settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden

# Delete existing task if it exists
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Write-Host "Removing old task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Register new task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -User $env:UserName

Write-Host "FlatAF Alpaca Driver is now set to start automatically on login."
Write-Host "Setup complete."
