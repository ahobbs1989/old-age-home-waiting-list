"""Tests for app/logic.py pure helpers."""

from datetime import date

from app.logic import calculate_age, estimate_wait_months, recommend_options
from app.models import MaritalStatus, OptionType


def test_calculate_age_before_birthday_this_year():
    assert calculate_age(date(1960, 12, 31), as_of=date(2026, 1, 1)) == 65


def test_calculate_age_after_birthday_this_year():
    assert calculate_age(date(1960, 1, 1), as_of=date(2026, 1, 1)) == 66


def test_recommend_options_single_over_65_includes_rental_and_life_right():
    options = recommend_options(70, MaritalStatus.SINGLE)
    assert OptionType.RENTAL in options
    assert OptionType.LIFE_RIGHT_SINGLE in options


def test_recommend_options_single_under_65_is_rental_only():
    assert recommend_options(50, MaritalStatus.SINGLE) == [OptionType.RENTAL]


def test_recommend_options_couple_recommends_life_right_couple():
    options = recommend_options(70, MaritalStatus.MARRIED)
    assert OptionType.LIFE_RIGHT_COUPLE in options


def test_estimate_wait_months_zero_rate_returns_none():
    assert estimate_wait_months(10, 0) is None


def test_estimate_wait_months_computes_months():
    assert estimate_wait_months(12, 12) == 12
