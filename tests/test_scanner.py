
from guardian.scanner import get_system_info, scan_environment


def test_get_system_info():

    result = get_system_info()

    assert isinstance(result, dict)
    assert "os" in result
    assert "release" in result
    assert "architecture" in result
    assert "python" in result


def test_scan_environment():

    result = scan_environment()

    assert isinstance(result, dict)
    assert "system" in result
    assert "tools" in result

    assert isinstance(result["tools"], list)


def test_scanned_tools_have_required_fields():

    result = scan_environment()

    for tool in result["tools"]:

        assert "id" in tool
        assert "name" in tool
        assert "status" in tool
        assert "version" in tool
        assert "path" in tool

        assert tool["status"] in [
            "Installed",
            "Missing",
            "Needs inspection"
        ]
