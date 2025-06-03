# Hydra Print Automation

A FastAPI-based automation service for AIP print operations.

## Features

- Automated AIP print operations
- Real-time status window for operation feedback
- Error logging
- Automatic startup on Windows login

## Prerequisites

- Windows
- Python 3.7 or later
- AIP application installed and configured

## Installation

1. Download the latest release ZIP from the [Releases page](https://github.com/1nto5/hydra-print-automation/releases)
2. Extract the contents to your preferred folder
3. On a computer with internet access:
   ```batch
   python download_packages.py
   ```
   This will download all required dependencies into the `deps` folder.
4. Transfer the entire folder (including `deps`) to the HYDRA Shuttle PC
5. On the HYDRA Shuttle PC, run:
   ```batch
   install.bat
   ```
6. To enable automatic startup on login, run:
   ```batch
   manage_startup.bat
   ```
7. Follow the prompts to add the application to Windows Startup

## API Endpoints

```bash
POST /run-aip-print-automation
Content-Type: application/json

{
    "identifier": "your_identifier",
    "quantity": "1",
    "workplace_position": 1
}
```

Response:

```json
{
  "status": "started"
}
```

## Logging

Logs are written to `app.log` and also displayed in the console. The log file includes only error messages:

- Automation errors
- Window management errors
- System errors
