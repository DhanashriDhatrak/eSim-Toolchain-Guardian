
import json
import platform
import shutil
import subprocess
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_tools():
    config_path = ROOT / "config" / "tools.json"

    with open(config_path, "r") as file:
        return json.load(file)["tools"]


def get_system_info():
    return {
        "os": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version()
    }


def extract_version(output):
    """Extract a readable version from command output."""

    # Handle Ngspice output such as ngspice-42
    ngspice_match = re.search(
        r"ngspice[- ](\d+(?:\.\d+)*)",
        output,
        re.IGNORECASE
    )

    if ngspice_match:
        return f"ngspice-{ngspice_match.group(1)}"

    # Handle normal version formats
    version_match = re.search(
        r"\d+(?:\.\d+)+",
        output
    )

    if version_match:
        return version_match.group(0)

    return None


def scan_tool(tool):
    executable = tool["executable"]
    executable_path = shutil.which(executable)

    if not executable_path:
        return {
            "id": tool["id"],
            "name": tool["name"],
            "status": "Missing",
            "version": "Not installed",
            "path": "Not found"
        }

    try:
        result = subprocess.run(
            [executable_path] + tool["version_args"],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout + "\n" + result.stderr

        version = extract_version(output)

        if result.returncode == 0 and version:
            status = "Installed"
        else:
            version = "Version check failed"
            status = "Needs inspection"

    except subprocess.TimeoutExpired:
        version = "Check timed out"
        status = "Needs inspection"

    except OSError:
        version = "Execution failed"
        status = "Needs inspection"

    return {
        "id": tool["id"],
        "name": tool["name"],
        "status": status,
        "version": version,
        "path": executable_path
    }


def scan_environment():
    tools = load_tools()

    results = [
        scan_tool(tool)
        for tool in tools
    ]

    return {
        "system": get_system_info(),
        "tools": results
    }
