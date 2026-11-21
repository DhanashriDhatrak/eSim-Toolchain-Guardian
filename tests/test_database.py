
from guardian.database import (
    initialize_database,
    record_installation,
    get_installation_history
)


def test_initialize_database():

    initialize_database()

    history = get_installation_history()

    assert isinstance(history, list)


def test_record_installation():

    initialize_database()

    record_installation(
        "test_tool",
        "Test Tool",
        "Success",
        "Automated database test"
    )

    history = get_installation_history()

    assert len(history) > 0

    latest = history[0]

    assert latest["tool_id"] == "test_tool"
    assert latest["tool_name"] == "Test Tool"
    assert latest["status"] == "Success"


def test_installation_history_fields():

    history = get_installation_history()

    if history:

        record = history[0]

        required_fields = [
            "id",
            "tool_id",
            "tool_name",
            "status",
            "message",
            "timestamp"
        ]

        for field in required_fields:

            assert field in record
