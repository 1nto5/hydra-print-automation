# Hydra Print Automation

A FastAPI-based automation service for AIP print operations.

## Features

- Automated AIP print operations with configurable workplace positions (1-4)
- Real-time status window for operation feedback
- Comprehensive logging
- Hot-reload enabled development server

## Prerequisites

- Python 3.7+
- Windows OS (required for pywinauto functionality)
- AIP application installed and configured

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd hydra-print-automation
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:

```bash
python main.py
```

2. The server will be available at `http://localhost:1995`

### API Endpoints

#### Run AIP Print Automation

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

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:1995/docs`
- ReDoc: `http://localhost:1995/redoc`

## Logging

Logs are written to `app.log` and also displayed in the console. The log file includes:

- API requests and responses
- Automation operations
- Error messages
- Window management events

## Development

The server runs with hot-reload enabled, so changes to the code will automatically restart the server.

## License

[Your License Here]
