

from guardian.compatibility import (
    extract_version,
    compare_versions,
    analyze_compatibility
)

from guardian.scanner import scan_environment


def test_extract_version():

    assert extract_version("Python 3.12.3") == (3, 12, 3)
    assert extract_version("git version 2.43.0") == (2, 43, 0)
    assert extract_version("ngspice-42") == (42,)


def test_compare_versions():

    assert compare_versions("3.12.3", "3.10") == "Compatible"
    assert compare_versions("2.43.0", "2.30") == "Compatible"
    assert compare_versions("3.8.0", "3.10") == "Incompatible"


def test_analyze_compatibility():

    scan_result = scan_environment()

    result = analyze_compatibility(scan_result)

    assert isinstance(result, dict)
    assert "results" in result
    assert "total" in result
    assert "compatible" in result
    assert "incompatible" in result
    assert "missing" in result
    assert "unknown" in result

    assert result["total"] == len(result["results"])


def test_compatibility_status_values():

    scan_result = scan_environment()

    result = analyze_compatibility(scan_result)

    valid_statuses = [
        "Compatible",
        "Incompatible",
        "Missing",
        "Unknown"
    ]

    for tool in result["results"]:

        assert tool["status"] in valid_statuses
