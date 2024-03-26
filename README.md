# Project Zomboid Server Manager README

This README provides setup instructions for the Project Zomboid Server Manager, a comprehensive Python-based application
designed to streamline the management of a dedicated Project Zomboid server. This document covers the installation of a
Python virtual environment, package installation, configuration settings, and launching the manager script
through `systemctl`.

## Prerequisites

Before you begin, ensure you have Python 3.6 or newer and `pip` installed on your system. You will also need `systemctl`
for managing the application as a service, typically available on Linux distributions.

## Installation

### Setting Up a Python Virtual Environment

1. Navigate to the project's root directory.
2. Execute `python3 -m venv venv` to create a new virtual environment named `venv`.
3. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On Unix or macOS: `source venv/bin/activate`

### Installing Required Packages

With the virtual environment activated, install the necessary packages using:

```bash
pip install -r requirements.txt
```

*Note: If `requirements.txt` is missing, you will need to manually install dependencies as needed.*

## Configuration (`config.yml`)

The `config.yml` file contains essential configurations for the server manager. Below are the variables you need to
configure:

- `server`:
    - `port`: Port number for the Project Zomboid server manager.
    - `host`: Host IP address for the server manager, usually `"0.0.0.0"` for listening on all interfaces.
- `rcon`:
    - `port`: Remote console port for Project Zomboid Server.
    - `password`: Password for RCON access.
    - `host`: Host IP address for RCON, typically `"127.0.0.1"` for local access.
- `auth`:
    - `username`: Username for administrative access to the server manager.
    - `password`: Password for administrative access.
    - `secret`: Secret key used for encryption or session management.
- `pz`:
    - `server_path`: Path to the Project Zomboid server files.
    - `log_filename`: Filename for the server log.
    - `pz_exe_path`: Path to the Project Zomboid executable.
    - `password`: Server password for player access.
    - `monitoring`: Enable or disable server monitoring (`True` or `False`).
- `steam`:
    - `apikey`: Steam API key for mod management and server updates.
    - `cache_folder`: Folder for caching downloaded mods.
    - `steamcmd_path`: Path to the SteamCMD directory.
    - `appid`: Steam application ID for Project Zomboid (108600).
- `discord`:
    - `apikey`: Your Discord bot token.
    - `channel`: The Discord channel ID where the bot will send messages or listen for commands.
    - `enable`: Enable or disable Discord integration (False or True).

Ensure to modify these variables according to your server setup requirements.

## Running the Server Manager

To manage the server via `systemctl`, create a service file:

1. Create `pzserver.service` in `/etc/systemd/system/`.
2. Fill it with:

```ini
[Unit]
Description=Project Zomboid Server Manager
After=network.target

[Service]
User=<username>
Group=<groupname>
WorkingDirectory=<path to project>
ExecStart=<path to python interpreter> main.py

[Install]
WantedBy=multi-user.target
```

Replace placeholders with appropriate values for your setup.

3. Reload the systemd manager configuration: `sudo systemctl daemon-reload`
4. Start the service: `sudo systemctl start pzserver`
5. Enable automatic startup on boot: `sudo systemctl enable pzserver`

---

This README aims to guide you through setting up and configuring the Project Zomboid Server Manager. For further
customization and troubleshooting, refer to the specific Python script documentation within the project.
