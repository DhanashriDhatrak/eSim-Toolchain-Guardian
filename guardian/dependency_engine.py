
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_dependency_profiles():
    config_path = ROOT / "config" / "dependency_map.json"

    with open(config_path, "r") as file:
        data = json.load(file)

    return data["profiles"]


def analyze_dependencies(scan_result):

    profiles = load_dependency_profiles()

    tools = {
        tool["id"]: tool
        for tool in scan_result["tools"]
    }

    installed = []
    missing = []

    for tool_id, tool in tools.items():
        if tool["status"] == "Installed":
            installed.append(tool_id)
        else:
            missing.append(tool_id)

    profile_results = []

    for profile in profiles:

        required = profile["requires"]

        missing_dependencies = [
            dependency
            for dependency in required
            if dependency not in tools
            or tools[dependency]["status"] != "Installed"
        ]

        health = (
            "Healthy"
            if not missing_dependencies
            else "At Risk"
        )

        profile_results.append({
            "id": profile["id"],
            "name": profile["name"],
            "description": profile["description"],
            "health": health,
            "required": required,
            "missing": missing_dependencies
        })

    affected = [
        profile
        for profile in profile_results
        if profile["health"] == "At Risk"
    ]

    total = len(profile_results)
    healthy = total - len(affected)

    health_score = (
        round(healthy / total * 100)
        if total else 100
    )

    return {
        "installed_count": len(installed),
        "missing_count": len(missing),
        "missing_tools": missing,
        "profiles": profile_results,
        "affected_profiles": affected,
        "health_score": health_score
    }
