
"""Qualifying date calculator for MatdarMitra."""

from datetime import date

QUALIFYING_DATES = [
    (1, 1),
    (4, 1),
    (7, 1),
    (10, 1)
]


def add_years(dob, years):
    """Add years and handle February 29 birthdays."""
    try:
        return dob.replace(year=dob.year + years)
    except ValueError:
        return dob.replace(year=dob.year + years, day=28)


def get_next_qualifying_date(eighteenth_birthday):
    """Return first qualifying date on or after 18th birthday."""

    for year in range(
        eighteenth_birthday.year,
        eighteenth_birthday.year + 2
    ):
        for month, day in QUALIFYING_DATES:
            qualifying_date = date(year, month, day)

            if qualifying_date >= eighteenth_birthday:
                return qualifying_date

    raise ValueError("Unable to calculate qualifying date")


def qualifying_date_calculator(dob, today=None):
    """
    Calculate 18th birthday and next ECI qualifying date.

    DOB format: YYYY-MM-DD
    """

    try:
        birth_date = date.fromisoformat(dob)
    except (ValueError, TypeError):
        raise ValueError("DOB must be in YYYY-MM-DD format")

    today = today or date.today()

    if birth_date > today:
        raise ValueError("Date of birth cannot be in the future")

    seventeenth_birthday = add_years(birth_date, 17)
    eighteenth_birthday = add_years(birth_date, 18)

    qualifying_date = get_next_qualifying_date(
        eighteenth_birthday
    )

    age_17_reached = today >= seventeenth_birthday

    advance_candidate = (
        age_17_reached and today < qualifying_date
    )

    return {
        "date_of_birth": birth_date.isoformat(),
        "turns_17_on": seventeenth_birthday.isoformat(),
        "turns_18_on": eighteenth_birthday.isoformat(),
        "next_qualifying_date": qualifying_date.isoformat(),
        "can_apply_in_advance": advance_candidate,
        "advance_application_status": (
            "Potentially eligible. Confirm that the ECI advance "
            "application window is open."
            if advance_candidate
            else "Not yet eligible for advance application."
        ),
        "can_apply_now": today >= qualifying_date,
        "note": (
            "Final enrollment depends on citizenship, ordinary "
            "residence, other eligibility conditions and ECI verification."
        )
    }


if __name__ == "__main__":
    result = qualifying_date_calculator("2009-12-15")

    for key, value in result.items():
        print(f"{key}: {value}")
