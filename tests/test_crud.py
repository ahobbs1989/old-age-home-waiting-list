"""Tests for app/crud.py against an in-memory SQLite session."""

from datetime import date, timedelta

from app import crud
from app.models import ApplicantCreate, ApplicantUpdate, MaritalStatus, OptionType, Urgency


def make_applicant_data(**overrides) -> ApplicantCreate:
    data = dict(
        name="Jane Smith",
        id_number="8001015800080",
        phone="0831234567",
        email="jane@example.com",
        address="1 Main Rd, Durban",
        is_ethekwini=True,
        date_of_birth=date(1980, 1, 1),
        marital_status=MaritalStatus.SINGLE,
        option_selected=OptionType.RENTAL,
        unit_type_preference="1 bed 1 bath",
        urgency=Urgency.LONG_TERM,
    )
    data.update(overrides)
    return ApplicantCreate(**data)


def test_create_applicant_assigns_unique_code(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    assert applicant.id is not None
    assert applicant.unique_code == f"WL-{applicant.id:06d}"
    assert applicant.application_date == date.today()


def test_get_applicant_by_code_roundtrip(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    found = crud.get_applicant_by_code(session, applicant.unique_code)
    assert found is not None
    assert found.id == applicant.id


def test_get_applicant_by_code_missing_returns_none(session):
    assert crud.get_applicant_by_code(session, "WL-999999") is None


def test_search_applicants_by_name_and_code(session):
    crud.create_applicant(session, make_applicant_data(name="Jane Smith", email="jane@example.com"))
    other = crud.create_applicant(session, make_applicant_data(name="Bob Jones", email="bob@example.com"))

    by_name = crud.search_applicants(session, "Jane")
    assert [a.name for a in by_name] == ["Jane Smith"]

    by_code = crud.search_applicants(session, other.unique_code)
    assert [a.id for a in by_code] == [other.id]


def test_update_applicant_changes_only_given_fields(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    updated = crud.update_applicant(session, applicant.id, ApplicantUpdate(phone="0829999999"))
    assert updated.phone == "0829999999"
    assert updated.name == applicant.name


def test_update_applicant_missing_returns_none(session):
    assert crud.update_applicant(session, 999, ApplicantUpdate(phone="x")) is None


def test_renew_applicant_resets_payment_and_due_date(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    crud.mark_paid(session, applicant.id)
    renewed = crud.renew_applicant(session, applicant.id)
    assert renewed.paid is False
    assert renewed.last_renewed_at == date.today()
    assert renewed.renewal_due_at == date.today() + timedelta(days=365)


def test_mark_paid_sets_flag(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    assert applicant.paid is False
    paid = crud.mark_paid(session, applicant.id)
    assert paid.paid is True


def test_remove_applicant_sets_status_and_excluded_from_default_search(session):
    applicant = crud.create_applicant(session, make_applicant_data(name="Removable"))
    crud.remove_applicant(session, applicant.id)
    results = crud.search_applicants(session, "Removable")
    assert results == []
    results_with_removed = crud.search_applicants(session, "Removable", include_removed=True)
    assert len(results_with_removed) == 1
    assert results_with_removed[0].status.value == "removed"


def test_list_due_for_renewal_flags_old_due_dates(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    applicant.renewal_due_at = date.today() - timedelta(days=200)
    session.add(applicant)
    session.commit()

    due = crud.list_due_for_renewal(session)
    assert [a.id for a in due] == [applicant.id]


def test_list_due_for_renewal_excludes_recent_due_dates(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    applicant.renewal_due_at = date.today() - timedelta(days=10)
    session.add(applicant)
    session.commit()

    assert crud.list_due_for_renewal(session) == []


def test_get_queue_position_orders_by_application_date(session):
    first = crud.create_applicant(session, make_applicant_data(email="first@example.com"))
    second = crud.create_applicant(session, make_applicant_data(email="second@example.com"))

    assert crud.get_queue_position(session, first.id) == (1, 1)
    assert crud.get_queue_position(session, second.id) == (2, 2)


def test_get_queue_position_for_removed_applicant_is_none(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    crud.remove_applicant(session, applicant.id)
    assert crud.get_queue_position(session, applicant.id) is None


def test_offer_create_and_respond(session):
    applicant = crud.create_applicant(session, make_applicant_data())
    offer = crud.create_offer(session, applicant.id, "A101")
    assert offer.response.value == "pending"

    responded = crud.respond_offer(session, offer.id, True)
    assert responded.response.value == "accepted"
    assert responded.date_responded == date.today()


def test_respond_offer_missing_returns_none(session):
    assert crud.respond_offer(session, 999, True) is None


def test_generate_availability_report_filters_by_option_and_unit_type(session):
    crud.create_applicant(
        session,
        make_applicant_data(
            email="a@example.com", option_selected=OptionType.RENTAL, unit_type_preference="1 bed"
        ),
    )
    crud.create_applicant(
        session,
        make_applicant_data(
            email="b@example.com", option_selected=OptionType.LIFE_RIGHT_COUPLE, unit_type_preference="2 bed"
        ),
    )

    rental_report = crud.generate_availability_report(session, OptionType.RENTAL)
    assert len(rental_report) == 1
    assert rental_report[0].email == "a@example.com"

    filtered = crud.generate_availability_report(session, OptionType.RENTAL, unit_type="2 bed")
    assert filtered == []


def test_wait_rate_defaults_and_can_be_set(session):
    assert crud.get_wait_rate(session, OptionType.RENTAL) == 1
    crud.set_wait_rate(session, OptionType.RENTAL, 5)
    assert crud.get_wait_rate(session, OptionType.RENTAL) == 5
