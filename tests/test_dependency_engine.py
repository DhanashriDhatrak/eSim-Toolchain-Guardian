
from guardian.scanner import scan_environment
from guardian.dependency_engine import (
    analyze_dependencies,
    load_dependency_profiles
)


def test_load_dependency_profiles():

    profiles = load_dependency_profiles()

    assert isinstance(profiles, list)
    assert len(profiles) > 0

    for profile in profiles:

        assert "id" in profile
        assert "name" in profile
        assert "requires" in profile


def test_analyze_dependencies():

    scan_result = scan_environment()

    result = analyze_dependencies(scan_result)

    assert isinstance(result, dict)
    assert "installed_count" in result
    assert "missing_count" in result
    assert "missing_tools" in result
    assert "profiles" in result
    assert "health_score" in result


def test_dependency_health_score():

    scan_result = scan_environment()

    result = analyze_dependencies(scan_result)

    assert 0 <= result["health_score"] <= 100


def test_dependency_profiles_have_valid_health():

    scan_result = scan_environment()

    result = analyze_dependencies(scan_result)

    valid_health = [
        "Healthy",
        "Unhealthy"
    ]

    for profile in result["profiles"]:

        assert profile["health"] in valid_health
