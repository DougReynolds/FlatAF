# FlatAF Alpaca Driver README
## Table of Contents
- [FlatAF Alpaca Driver README](#flataf-alpaca-driver-readme)
  - [Table of Contents](#table-of-contents)
  - [Disclaimer](#disclaimer)
  - [Driver Deployment Process](#driver-deployment-process)
  - [Updating the Driver to a New Version](#updating-the-driver-to-a-new-version)
    - [Updating the Driver (New Version or UUID)](#updating-the-driver-new-version-or-uuid)
  - [Minimum Python Setup Required on the Target Machine (Windows 11 Pro)](#minimum-python-setup-required-on-the-target-machine-windows-11-pro)
  - [Licensing](#licensing)

## Disclaimer
AstroAF makes no warranties or guarantees of any kind, express or implied. The scripts, applications, and processes included in the FlatAF ASCOM Alpaca project are provided "AS IS" and may be destructive to your file system or operating system if not used correctly. Users must exercise caution. If you do not fully understand the instructions or risks involved, STOP NOW or proceed entirely at your own risk.

## Driver Deployment Process
- **Package the Driver for Deployment**

  From your development machine, run:

  ```bash
  ./deploy_driver.sh
  ```

  This will:
  - Create a ZIP file inside the `staging/` folder.
  - Automatically include `version.json` based on Git tag.
  - Exclude unnecessary files like `.git`, `__pycache__`, logs, etc.

  Example output:
  ```
  staging/FlatAF_Alpaca_Deploy_v0.0.1-beta.zip
  ```

- **Copy the Deployment Package**

  Copy the deployment ZIP to your target machine, e.g.:
  ```
  C:\Astrophotography\Alpaca\
  ```

  Extract the ZIP to restore the full `FlatAF_Alpaca` project structure.

- **Set Up the Virtual Environment**

  - **Automated Setup**

    - Open PowerShell as Administrator
    - Navigate to your FlatAF driver folder
    - Execute:
      ```powershell
      powershell.exe -ExecutionPolicy Bypass -File .\register_task.ps1
      ```

      This will:
      - Create the virtual environment
      - Install Python dependencies
      - Register the driver for auto-start at login
      - Log out and back in to Windows to start the driver automatically.

  - **Manual Setup**

    On your target machine:

    - Open Command Prompt
    - Navigate to the driver folder:
      ```powershell
      cd C:\Users\YourName\Documents\FlatAF_Alpaca\device
      ```
    - Create and activate a virtual environment:
      ```powershell
      python -m venv alpaca-env
      alpaca-env\Scripts\activate
      ```
    - Install Python dependencies manually:
      ```powershell
      pip install -r requirements.txt
      ```
    - (Optional) Register the driver to auto-launch by running:
      ```powershell
      ./register_task.ps1
      ```
    - Log out and back in to Windows to start the driver.

## Updating the Driver to a New Version
When deploying a new version of the FlatAF Alpaca Driver to an existing setup (e.g., after a bug fix or version update), follow these steps:
- Stop the currently running driver (optional):

  If the driver was started manually, you can stop it with Ctrl+C in the running terminal. If it was launched via the scheduled task, you can stop it by logging out of Windows or using:

  ```powershell
  Stop-ScheduledTask -TaskName "FlatAF Alpaca Driver"
  ```

  Note: If Stop-ScheduledTask does not stop the task immediately, use Ctrl+C if the driver was started manually.

- Copy the updated driver files:

  On your development machine, locate the updated driver files under the device/ folder. Copy all updated files (except alpaca-env/ and other local virtualenv folders) to the driver directory on your target system:

  ```
  C:\Users\YourName\Documents\FlatAF_Alpaca\device
  ```

  Overwrite the existing files when prompted.

- (Optional) Reinstall dependencies if requirements.txt changed:

  If any changes were made to requirements.txt, activate the virtual environment and reinstall:

  ```powershell
  cd C:\Users\YourName\Documents\FlatAF_Alpaca\device
  .\alpaca-env\Scripts\activate
  pip install -r requirements.txt
  ```

- Restart the driver:

  To restart the driver using the scheduled task:

  ```powershell
  Start-ScheduledTask -TaskName "FlatAF Alpaca Driver"
  ```

  Alternatively, launch manually by activating the environment and running:

  ```powershell
  cd C:\Users\YourName\Documents\FlatAF_Alpaca\device
  .\alpaca-env\Scripts\activate
  python main.py
  ```

### Updating the Driver (New Version or UUID)
To update the driver after deploying a new version (or changing the DeviceID/UUID), follow these steps:
- Stop the Currently Running Driver  
  If the driver is running in a terminal window, press Ctrl+C.  
  Or stop the scheduled task manually with:  
  ```powershell
  Stop-ScheduledTask -TaskName "FlatAF Alpaca Driver"
  ```
- Example N.I.N.A.: Clear NINA’s Cached Driver Association  
  In NINA:  
  Go to Options → Equipment → Flat Panel

  Select “No Flat Panel”

  Click Connect to clear the internal device cache

- Update the Driver Files  
  If you’ve modified the driver (e.g., version update, code changes):  
  Update covercalibrator.py with the new DeviceID, e.g.:

  ```python
  DeviceID = 'your-new-uuid'
  ```

  Generate a new UUID using Python:

  ```python
  import uuid; print(uuid.uuid4())
  ```

  Copy your updated project files into the existing driver folder on your target machine (overwrite existing files)

- Restart the Updated Driver  
  Run:  
  ```powershell
  Start-ScheduledTask -TaskName "FlatAF Alpaca Driver"
  ```

- Example N.I.N.A.: Reconnect in NINA  
  Open NINA and go to Options → Equipment → Flat Panel

  The updated FlatAF driver should appear

  Select it and click Connect

- Confirm It’s Working  
  After completing the setup, confirm the FlatAF driver is responding by accessing the Alpaca Management Service.

  - Visit `http://<your-device-ip>:5555/management/v1/configureddevices`
  - Open **N.I.N.A. > Equipment > Flat Panel > Alpaca**, or another ASCOM-compatible application, enter the device IP, and test connectivity

## Minimum Python Setup Required on the Target Machine (Windows 11 Pro)
This driver is a Python-based ASCOM Alpaca CoverCalibrator driver. Follow these steps:
- Install Python  
  Download and install Python 3.11 or later:  
  https://www.python.org/downloads/windows/

  During installation:  
  Check “Add Python to PATH”

  (Optional) Install for all users

- Copy the Project  
  Copy your FlatAF Alpaca driver folder to your target machine:

  ```
  C:\Users\YourName\Documents\FlatAF_Alpaca\device
  ```

Notes  
- alpaca-env must be recreated on the target machine. It cannot simply be copied.

- The deploy_driver.sh script automates staging, version tagging, and packaging. Version tagging is automated from the `git tag <versio>` result and written to file during running `deploy.sh`.

- Always check your BaseURL inside covercalibrator_config.json after moving to a different network.

- The device web server version (/device/version.json) and driver version are independent but both should be tagged using Git.
  
- You **do not need** to delete the whole project
  
- File-level replacement is fine as long as you're editing the live environment
  
- If Python crashes or fails to start, run `python device/app.py` in a PowerShell window and check the logs

## Licensing

For license information, see the project [LICENSE.md](../LICENSE.md) file in this repository.
