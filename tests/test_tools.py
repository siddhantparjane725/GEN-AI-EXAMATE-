
from datetime import date

import pytest

from app.tools import qualifying_date_calculator


def test_next_qualifying_date():
    result = qualifying_date_calculator(
        "2009-12-15",
        today=date(2026, 11, 17)
    )
    assert result["turns_18_on"] == "2027-12-15"
    assert result["next_qualifying_date"] == "2028-01-01"


def test_birthday_on_qualifying_date():
    result = qualifying_date_calculator(
        "2008-01-01",
        today=date(2026, 1, 1)
    )
    assert result["turns_18_on"] == "2026-01-01"
    assert result["next_qualifying_date"] == "2026-01-01"
    assert result["can_apply_now"] is True


def test_birthday_after_qualifying_date():
    result = qualifying_date_calculator(
        "2008-01-02",
        today=date(2026, 1, 2)
    )
    assert result["next_qualifying_date"] == "2026-04-01"


def test_future_dob_rejected():
    with pytest.raises(ValueError):
        qualifying_date_calculator(
            "2030-01-01",
            today=date(2026, 1, 1)
        )


def test_invalid_dob_rejected():
    with pytest.raises(ValueError):
        qualifying_date_calculator(
            "15-12-2009",
            today=date(2026, 1, 1)
        )
