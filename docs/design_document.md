
# eSim Toolchain Guardian – Design Document

## 1. Introduction

eSim Toolchain Guardian is a Python-based desktop application developed to simplify the management of development tools required for eSim workflows.

In electronic design and simulation projects, developers need tools such as Ngspice, KiCad, Python, and Git. Managing these tools manually can be difficult, especially when checking their installation status, versions, and dependencies.

This application provides a single graphical interface to monitor the development environment and manage supported tool installations.

## 2. Objectives

The main objectives are:

1. Automatically detect installed development tools.
2. Display tool versions and installation paths.
3. Identify missing tools and dependencies.
4. Check installed tool versions against configurable compatibility rules.
5. Support installation of selected tools.
6. Maintain installation history.
7. Provide a simple graphical user interface.
8. Maintain logs for application activities.

## 3. System Requirements

### Software Requirements

- Python 3.10 or later
- Ubuntu/Debian Linux recommended
- Tkinter
- SQLite
- Pytest
- APT package manager for supported installations

### Hardware Requirements

- Computer with at least 4 GB RAM
- Basic processor
- Sufficient disk space for Python and development tools

## 4. System Architecture

The application follows a modular architecture. Each module is responsible for a particular operation.

### Main Components

**1. User Interface – app.py**

- Provides the Tkinter graphical interface.
- Displays the dashboard.
- Provides access to different application sections.
- Shows scanner, dependency, compatibility, installation, and history results.

**2. Environment Scanner – scanner.py**

- Detects available development tools.
- Checks installation paths.
- Retrieves installed tool versions.
- Collects operating system information.

**3. Dependency Engine – dependency_engine.py**

- Loads dependency profiles from JSON configuration.
- Checks whether required tools are installed.
- Identifies missing dependencies.
- Calculates dependency health percentage.

**4. Compatibility Checker – compatibility.py**

- Extracts version numbers.
- Compares installed versions with minimum required versions.
- Classifies tools as compatible, incompatible, missing, or unknown.

**5. Installation Manager – installer.py**

- Supports Ngspice and KiCad installation through APT.
- Checks whether a tool is already installed.
- Executes supported installation commands.
- Records installation results.

**6. Database Manager – database.py**

- Uses SQLite to store installation records.
- Maintains tool names, IDs, statuses, messages, and timestamps.
- Retrieves previous installation history.

**7. Logger – logger.py**

- Records important application events.
- Maintains log files.
- Helps in identifying application and installation issues.

## 5. Application Workflow

The application follows this general workflow:

1. The user opens the application.
2. The dashboard displays the system and tool information.
3. The scanner checks the available development tools.
4. The dependency engine analyzes required dependencies.
5. The compatibility checker compares installed versions with configured rules.
6. The user can open the installation manager to install supported missing tools.
7. Installation results are stored in the SQLite database.
8. The user can view previous installation records.

## 6. Dependency Analysis

The application uses JSON-based dependency profiles.

Currently configured workflows include:

- eSim Circuit Simulation
- eSim PCB Design
- Development Environment

Each workflow contains a list of required tools.

The dependency engine checks the installation status of each required tool.

### Dependency Health Calculation

The dependency health score is calculated using:

Dependency Health (%) = (Number of Healthy Workflows / Total Workflows) × 100

A workflow is considered healthy when all its required tools are installed.

For example, if all three configured workflows are healthy:

Dependency Health = (3 / 3) × 100 = 100%

## 7. Compatibility Checking

The compatibility module compares the installed version of a tool with its configured minimum version.

For example:

- Python minimum version: 3.10
- Git minimum version: 2.30
- Ngspice minimum version: 40
- KiCad minimum version: 7.0

These values are configurable prototype policies.

The module identifies four possible statuses:

- Compatible
- Incompatible
- Missing
- Unknown

## 8. Tool Installation Management

The installation manager currently supports:

- Ngspice
- KiCad

It uses the Ubuntu/Debian APT package manager.

Example installation commands:

```bash
sudo apt-get install -y ngspice
sudo apt-get install -y kicad
```

Before installation, the application checks whether the selected tool is already installed.

If the tool is already available, unnecessary reinstallation is avoided.

Installation attempts and their results are recorded in the database.

Note: Installation may require administrator privileges.

## 9. Database Design

The application uses SQLite for storing installation history.

Database file:

`data/installation_history.db`

The installation history contains the following fields:

| Field | Description |
|---|---|
| id | Unique record ID |
| tool_id | Tool identifier |
| tool_name | Name of the tool |
| status | Installation result |
| message | Additional information |
| timestamp | Date and time of the operation |

This information helps users review previous installation activities.

## 10. Logging System

The application maintains logs in:

`logs/toolchain_guardian.log`

The logger records important events and helps with debugging and monitoring application activities.

## 11. Configuration Files

The application uses JSON files to maintain configurable information.

- `config/tools.json`: Development tool definitions.
- `config/dependency_map.json`: Workflow dependency information.
- `config/compatibility.json`: Minimum and recommended tool versions.

This approach makes it easier to modify tool definitions and policies.

## 12. Testing

Automated testing is performed using Pytest.

The project currently contains four test modules:

1. `test_scanner.py`
2. `test_compatibility.py`
3. `test_dependency_engine.py`
4. `test_database.py`

### Test Results

| Module | Tests Passed |
|---|---:|
| Environment Scanner | 3 |
| Compatibility Checker | 4 |
| Dependency Engine | 4 |
| Database | 3 |
| Total | 14 |

All 14 automated tests passed successfully.

Compilation was also checked using:

`python -m compileall guardian`

No compilation errors were reported.

## 13. Current Limitations

1. The installation manager currently supports Ubuntu/Debian APT-based installations only.
2. Automatic update and upgrade checking is not yet implemented.
3. Compatibility rules are configurable prototype policies and are not official eSim compatibility guarantees.
4. Additional tools and operating systems can be supported in future versions.

## 14. Future Enhancements

1. Add automatic tool update and upgrade checking.
2. Add Windows installation support.
3. Support more electronic design and simulation tools.
4. Generate environment and dependency reports.
5. Add improved installation progress and error handling.
6. Provide more detailed dependency recommendations.

## 15. Conclusion

eSim Toolchain Guardian provides a centralized way to monitor and manage important development tools used in eSim workflows.

It combines environment scanning, dependency analysis, compatibility checking, tool installation, logging, and installation history in a single desktop application.

The modular design makes the application easier to maintain and extend with additional features in the future.
