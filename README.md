# Hydra Print Automation

A FastAPI-based automation service for AIP print operations.

## Features

- Automated AIP print operations with configurable workplace positions (1-4)
- Real-time status window for operation feedback
- Error logging
- Hot-reload enabled development server
- Windows service for automatic startup

## Prerequisites

- Python 3.7+
- Windows OS (required for pywinauto functionality)
- AIP application installed and configured
- Git installed on development machine
- Administrator privileges on Hydra Shuttle for service installation

## Installation

### Option 1: Download Latest Release

1. Go to the [Releases page](https://github.com/1nto5/hydra-print-automation/releases)
2. Download the latest release ZIP file (e.g., `hydra-print-automation-v0.1.zip`)
3. Extract the ZIP file to your desired location
4. Download dependencies:

```batch
python download_packages.py
```

5. Follow the deployment steps below

### Option 2: Using Git Clone

1. Clone the repository:

```batch
git clone https://github.com/1nto5/hydra-print-automation.git
cd hydra-print-automation
```

2. Checkout the desired release:

```batch
git checkout v0.1
```

3. Download dependencies:

```batch
python download_packages.py
```

## Deployment Workflow

### 1. Development Machine Setup

1. Clone the repository:

```batch
git clone https://github.com/your-org/hydra-print-automation.git
cd hydra-print-automation
```

2. Prepare dependencies for offline installation:

```batch
python download_packages.py
```

This will create a `deps` directory with all required packages.

### 2. Deployment to Hydra Shuttle

1. Copy the entire project directory to Hydra Shuttle:

   - Copy the following files and directories:
     - `main.py`
     - `requirements.txt`
     - `deps/` directory
     - `install.bat`
     - `service_install.bat`

2. On Hydra Shuttle, run the installation script:

```batch
install.bat
```

### 3. Windows Service Setup

1. Install as Windows Service (requires Administrator privileges):

```batch
service_install.bat
```

The service will be installed with the following properties:

- Service Name: `HydraPrintAutomation`
- Display Name: `Hydra Print Automation Service`
- Startup Type: Automatic
- Description: "Automates AIP print operations for Hydra system"

2. Service Management:
   - Start service: `net start HydraPrintAutomation`
   - Stop service: `net stop HydraPrintAutomation`
   - Check status: `sc query HydraPrintAutomation`

## Manual Operation (Alternative to Service)

If you prefer to run the application manually:

1. Start the server:

```batch
python main.py
```

2. The server will be available at `http://localhost:5000`

## API Endpoints

### Run AIP Print Automation

```bash
POST /run-aip-print-automation
Content-Type: application/json

{
    "identifier": "your_identifier",
    "workplace_position": 1   # Optional, range 1-4, default: 1
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
- Service errors

## Development

The server runs with hot-reload enabled, so changes to the code will automatically restart the server.
