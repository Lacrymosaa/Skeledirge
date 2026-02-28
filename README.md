# Skeledirge: Auto-Spicetify Patcher

**Skeledirge** is a lightweight Python-based automation tool designed to keep your Spotify client patched with **Spicetify**. It monitors the Spotify executable for updates and automatically reapplies the Spicetify patch whenever the application is updated by the system, ensuring your themes and extensions never break.

---

## 🛠️ How It Works

The core logic of `skeledirge.py` functions as a proactive watchdog for your Spotify installation:

* **Dynamic Pathing**: It locates the Spotify installation within the user's `%APPDATA%` folder, making it compatible with any standard Windows installation (non-Microsoft Store version).
* **File Signature Tracking**: The script calculates a unique signature based on the `Spotify.exe` file size and modification timestamp.
* **Persistent Database**: It maintains a local JSON database (`last_update.json`) inside a dedicated `AutoSpicetify` folder to track the last known patched version.
* **Automated Recovery**: If a mismatch is detected (indicating Spotify has updated), the script triggers a PowerShell routine to reinstall the Spicetify CLI and reapply the backup.



---

## 🚀 Installation & Deployment

The project includes a `SetBoot.bat` utility to ensure the patcher runs seamlessly in the background:

1. **Startup Integration**: The batch script identifies the Windows Startup folder (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`).
2. **Binary Deployment**: It copies the compiled `AutoSpicetify.exe` into the startup directory.
3. **First-Run Config**: It automatically launches the program after copying to initialize the first patch and create the database.
4. **Persistence**: Once installed, the program runs automatically every time you boot your PC.

---

## 📋 Requirements

* **Spotify**: Standard Desktop version (the Microsoft Store version is not supported due to file permission restrictions).
* **OS**: Windows 10/11.
* **Permissions**: Execution of PowerShell scripts must be enabled for the Spicetify commands to run correctly.

---

> **Note**: This tool was developed by **Lacrymosaa** to automate the maintenance of a modded Spotify experience.
