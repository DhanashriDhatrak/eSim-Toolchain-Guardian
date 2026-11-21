
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_compatibility_rules():
    path = ROOT / "config" / "compatibility.json"

    with open(path, "r") as file:
        return json.load(file)["rules"]


def extract_version(version_text):
    if not version_text:
        return None

    # Special handling for Ngspice, e.g. ngspice-42
    ngspice_match = re.search(
        r"ngspice[- ](\d+(?:\.\d+)*)",
        version_text,
        re.IGNORECASE
    )

    if ngspice_match:
        version_text = ngspice_match.group(1)

    else:
        # Support versions such as 3.12.3, 2.43.0 and 42
        match = re.search(
            r"\d+(?:\.\d+)*",
            version_text
        )

        if not match:
            return None

        version_text = match.group(0)

    return tuple(
        int(part)
        for part in version_text.split(".")
    )


def compare_versions(installed, minimum):
    installed_version = extract_version(installed)
    minimum_version = extract_version(minimum)

    if installed_version is None:
        return "Unknown"

    if minimum_version is None:
        return "Invalid Rule"

    length = max(
        len(installed_version),
        len(minimum_version)
    )

    installed_version += (0,) * (
        length - len(installed_version)
    )

    minimum_version += (0,) * (
        length - len(minimum_version)
    )

    if installed_version < minimum_version:
        return "Incompatible"

    return "Compatible"


def analyze_compatibility(scan_result):
    rules = load_compatibility_rules()

    tools = {
        tool["id"]: tool
        for tool in scan_result["tools"]
    }

    results = []

    for rule in rules:
        tool_id = rule["tool_id"]
        tool = tools.get(tool_id)

        if not tool or tool["status"] != "Installed":
            status = "Missing"
            installed_version = "Not installed"

        else:
            installed_version = tool["version"]

            status = compare_versions(
                installed_version,
                rule["minimum_version"]
            )

        results.append({
            "tool_id": tool_id,
            "installed_version": installed_version,
            "minimum_version": rule["minimum_version"],
            "recommended_version": rule["recommended_version"],
            "purpose": rule["purpose"],
            "status": status
        })

    compatible = sum(
        item["status"] == "Compatible"
        for item in results
    )

    return {
        "results": results,
        "total": len(results),
        "compatible": compatible,
        "incompatible": sum(
            item["status"] == "Incompatible"
            for item in results
        ),
        "missing": sum(
            item["status"] == "Missing"
            for item in results
        ),
        "unknown": sum(
            item["status"] in ("Unknown", "Invalid Rule")
            for item in results
        )
    }
