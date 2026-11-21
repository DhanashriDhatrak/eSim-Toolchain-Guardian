https://github.com/DhanashriDhatrak/eSim-Toolchain-Guardian.git
# eSim Toolchain Guardian

eSim Toolchain Guardian is a Python-based desktop application designed to manage and monitor the development tools required for eSim workflows.

It provides a graphical interface to scan installed tools, check their versions, analyze dependencies, verify compatibility, and manage supported tool installations.

## Features

### 1. Environment Scanner
- Detects installed development tools.
- Displays tool names, versions, and installation paths.
- Identifies missing tools.
- Displays system information.

### 2. Dependency Analysis
- Checks dependencies required by different eSim workflows.
- Identifies missing dependencies.
- Calculates dependency health percentage.
- Displays workflow health status.

### 3. Compatibility Checker
- Checks installed tool versions against configurable minimum versions.
- Identifies compatible and incompatible tools.
- Uses configurable compatibility rules.

### 4. Installation Manager
- Supports Ngspice and KiCad installation on Ubuntu/Debian systems using APT.
- Avoids reinstalling tools that are already installed.
- Records installation attempts and results.

### 5. Installation History
- Stores installation records in an SQLite database.
- Displays tool names, status, messages, and timestamps.

### 6. Logging
- Maintains application logs.
- Records important application and installation events.

## Technologies Used

- Python 3
- Tkinter
- SQLite
- JSON
- Pytest
- Linux / Ubuntu

## Project Structure

```text
eSim-Toolchain-Guardian/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── guardian/
│   ├── __init__.py
│   ├── app.py
│   ├── scanner.py
│   ├── dependency_engine.py
│   ├── compatibility.py
│   ├── installer.py
│   ├── database.py
│   └── logger.py
│
├── config/
│   ├── tools.json
│   ├── dependency_map.json
│   └── compatibility.json
│
├── data/
├── logs/
│
├── tests/
│   ├── test_scanner.py
│   ├── test_compatibility.py
│   ├── test_dependency_engine.py
│   └── test_database.py
│
└── docs/
    └── design_document.md
```

## Requirements

- Python 3.10 or later
- Ubuntu/Debian recommended for the installation manager
- Tkinter support
- pip
- sudo privileges for installing system packages

## Installation and Setup

### 1. Clone the repository

```bash
git clone <https://github.com/DhanashriDhatrak/eSim-Toolchain-Guardian.git>
cd eSim-Toolchain-Guardian
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

## Running Tests

Run all automated tests using:

```bash
python -m pytest -v
```

Current test result:

- Total tests: 14
- Passed: 14
- Failed: 0

Check Python compilation using:

```bash
python -m compileall guardian
```

## Configuration

The application uses JSON configuration files:

- `tools.json`: Tool definitions and scanning information.
- `dependency_map.json`: Dependencies required by different workflows.
- `compatibility.json`: Minimum and recommended tool versions.

These files allow tool and dependency policies to be modified without changing the main application logic.

## Platform Support and Limitations

- Environment scanning and compatibility checking are designed to detect tools available in the system environment.
- The current installation manager uses APT and is intended for Ubuntu/Debian systems.
- Installation of system packages may require sudo privileges.
- Compatibility values are configurable prototype policies, not official eSim compatibility guarantees.
- Automatic tool update and upgrade functionality is not currently implemented.

## Future Enhancements

- Automatic update and upgrade checking.
- Windows installation support.
- More development tool integrations.
- Exportable environment and dependency reports.
- Improved installation progress monitoring.

## Author

Developed as an internship project to simplify eSim development environment management.
