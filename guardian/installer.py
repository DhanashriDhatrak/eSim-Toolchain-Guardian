
import shutil
import subprocess

from guardian.database import record_installation
from guardian.logger import log_event


AVAILABLE_TOOLS = {
    "ngspice": {
        "name": "Ngspice",
        "package": "ngspice",
        "executable": "ngspice"
    },
    "kicad": {
        "name": "KiCad",
        "package": "kicad",
        "executable": "kicad-cli"
    }
}


def get_installation_status(tool_id):
    if tool_id not in AVAILABLE_TOOLS:
        return {
            "success": False,
            "message": "Unsupported tool."
        }

    tool = AVAILABLE_TOOLS[tool_id]
    executable_path = shutil.which(tool["executable"])

    if executable_path:
        return {
            "success": True,
            "installed": True,
            "path": executable_path,
            "message": f'{tool["name"]} is already installed.'
        }

    return {
        "success": True,
        "installed": False,
        "path": None,
        "message": f'{tool["name"]} is not installed.'
    }


def finish_installation(tool_id, success, message, status=None):
    tool = AVAILABLE_TOOLS.get(tool_id, {})
    tool_name = tool.get("name", tool_id)

    if status is None:
        status = "Success" if success else "Failed"

    try:
        record_installation(
            tool_id,
            tool_name,
            status,
            message
        )

        log_event(
            f"{tool_name} | {status} | {message}",
            "info" if success else "error"
        )

    except Exception as error:
        log_event(
            f"Could not save installation history: {error}",
            "error"
        )

    return {
        "success": success,
        "message": message
    }


def install_tool(tool_id):
    """Install a supported tool using Ubuntu/Debian apt."""

    if tool_id not in AVAILABLE_TOOLS:
        return finish_installation(
            tool_id,
            False,
            "Unsupported tool."
        )

    if shutil.which("apt-get") is None:
        return finish_installation(
            tool_id,
            False,
            "This installer currently supports Ubuntu/Debian only."
        )

    tool = AVAILABLE_TOOLS[tool_id]

    # Avoid reinstalling an existing tool.
    current_status = get_installation_status(tool_id)

    if current_status.get("installed"):
        return finish_installation(
            tool_id,
            True,
            current_status["message"],
            "Already installed"
        )

    command = [
        "sudo",
        "-n",
        "apt-get",
        "install",
        "-y",
        tool["package"]
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=1800
        )

        if result.returncode == 0:
            executable_path = shutil.which(tool["executable"])

            if executable_path:
                return finish_installation(
                    tool_id,
                    True,
                    f'{tool["name"]} installation completed successfully.'
                )

            return finish_installation(
                tool_id,
                False,
                "Package installation finished, but executable was not found."
            )

        error_message = (
            result.stderr.strip()
            or result.stdout.strip()
            or "Installation failed."
        )

        if "password" in error_message.lower() or "sudo" in error_message.lower():
            error_message += " Run sudo -v in your terminal and retry."

        return finish_installation(
            tool_id,
            False,
            error_message
        )

    except subprocess.TimeoutExpired:
        return finish_installation(
            tool_id,
            False,
            "Installation timed out."
        )

    except Exception as error:
        return finish_installation(
            tool_id,
            False,
            str(error)
        )
