"""Pure business-rule helpers: no database access, no UI."""

from __future__ import annotations

from datetime import date

from app.models import MaritalStatus, OptionType

RENEWAL_PERIOD_DAYS = 365
NOT_RENEWED_FLAG_DAYS = 180


def calculate_age(date_of_birth: date, as_of: date | None = None) -> int:
    """Return age in whole years as of `as_of` (default: today)."""
    as_of = as_of or date.today()
    years = as_of.year - date_of_birth.year
    had_birthday = (as_of.month, as_of.day) >= (date_of_birth.month, date_of_birth.day)
    return years if had_birthday else years - 1


def recommend_options(age: int, marital_status: MaritalStatus) -> list[OptionType]:
    """Suggest applicable options based on age and marital status (spec section A.3)."""
    if marital_status == MaritalStatus.SINGLE:
        if age >= 65:
            return [OptionType.RENTAL, OptionType.LIFE_RIGHT_SINGLE]
        return [OptionType.RENTAL]
    # married / partner
    if age >= 65:
        return [OptionType.LIFE_RIGHT_COUPLE, OptionType.RENTAL]
    return [OptionType.LIFE_RIGHT_COUPLE]


def estimate_wait_months(position: int, units_per_year: int) -> int | None:
    """Rough wait estimate: queue position divided by the configured turnover rate."""
    if units_per_year <= 0:
        return None
    years = position / units_per_year
    return max(1, round(years * 12))
