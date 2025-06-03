# Release 0.1.1 (2025-06-03)

## New Features

- Added support for global Python installation (no virtual environment required)
- Improved Windows service installation and management
- Added automatic Python path detection
- Better error handling and logging

## Installation

### Prerequisites

- Python 3.7 or later installed globally
- Windows OS (required for pywinauto functionality)
- Administrator privileges for service installation

### Steps

1. Download the latest release ZIP file
2. Extract to your desired location
3. Open Command Prompt as Administrator
4. Run: `install.bat`
5. To install as a service: `service_install.bat`

## Changes from 0.1.0

- Removed virtual environment requirement
- Simplified installation process
- Added service uninstallation script
- Improved error messages and logging
- Better handling of service startup/shutdown

## Known Issues

- None

## Upgrade Notes

- If upgrading from 0.1.0, it's recommended to uninstall the old service first
- All configuration remains compatible with 0.1.0

## Files Changed

- `install.bat` - Updated for global Python installation
- `service_install.bat` - Improved service installation
- `service_uninstall.bat` - New script for service removal
- `main.py` - Minor updates and improvements
