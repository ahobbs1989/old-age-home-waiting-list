"""All database operations. Functions take a Session as their first argument."""

from __future__ import annotations

from datetime import date, timedelta

from sqlmodel import Session, or_, select

from app.logic import NOT_RENEWED_FLAG_DAYS, RENEWAL_PERIOD_DAYS
from app.models import (
    Applicant,
    ApplicantCreate,
    ApplicantUpdate,
    ApplicationStatus,
    AuditLogEntry,
    Offer,
    OfferResponse,
    OptionType,
    WaitEstimateConfig,
)


def log_action(session: Session, applicant_code: str, action: str, detail: str = "") -> AuditLogEntry:
    """Record an admin action against an applicant code for future reference."""
    entry = AuditLogEntry(applicant_code=applicant_code, action=action, detail=detail)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def create_applicant(session: Session, data: ApplicantCreate) -> Applicant:
    """Create a new waiting-list applicant and assign their unique code."""
    applicant = Applicant(**data.model_dump(), application_date=date.today())
    session.add(applicant)
    session.commit()
    session.refresh(applicant)
    applicant.unique_code = f"WL-{applicant.id:06d}"
    session.add(applicant)
    session.commit()
    session.refresh(applicant)
    log_action(session, applicant.unique_code, "joined")
    return applicant


def get_applicant(session: Session, applicant_id: int) -> Applicant | None:
    """Fetch an applicant by primary key."""
    return session.get(Applicant, applicant_id)


def get_applicant_by_code(session: Session, unique_code: str) -> Applicant | None:
    """Fetch an applicant by their unique waiting-list code."""
    statement = select(Applicant).where(Applicant.unique_code == unique_code.strip().upper())
    return session.exec(statement).first()


def search_applicants(session: Session, query: str, include_removed: bool = False) -> list[Applicant]:
    """Search applicants by code, name, email, or phone (admin search function)."""
    like = f"%{query.strip()}%"
    statement = select(Applicant).where(
        or_(
            Applicant.unique_code.ilike(like),
            Applicant.name.ilike(like),
            Applicant.email.ilike(like),
            Applicant.phone.ilike(like),
        )
    )
    if not include_removed:
        statement = statement.where(Applicant.status == ApplicationStatus.ACTIVE)
    return list(session.exec(statement.order_by(Applicant.application_date)))


def list_applicants(
    session: Session,
    status: ApplicationStatus | None = ApplicationStatus.ACTIVE,
    option_type: OptionType | None = None,
) -> list[Applicant]:
    """List applicants, optionally filtered by status and/or option, ordered by application date."""
    statement = select(Applicant)
    if status is not None:
        statement = statement.where(Applicant.status == status)
    if option_type is not None:
        statement = statement.where(Applicant.option_selected == option_type)
    return list(session.exec(statement.order_by(Applicant.application_date)))


def update_applicant(session: Session, applicant_id: int, data: ApplicantUpdate) -> Applicant | None:
    """Update an applicant's details. Only fields set on `data` are changed."""
    applicant = session.get(Applicant, applicant_id)
    if applicant is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(applicant, key, value)
    session.add(applicant)
    session.commit()
    session.refresh(applicant)
    log_action(session, applicant.unique_code, "updated_details")
    return applicant


def renew_applicant(session: Session, applicant_id: int) -> Applicant | None:
    """Renew an applicant's waiting-list registration, resetting payment status."""
    applicant = session.get(Applicant, applicant_id)
    if applicant is None:
        return None
    today = date.today()
    applicant.last_renewed_at = today
    applicant.renewal_due_at = today + timedelta(days=RENEWAL_PERIOD_DAYS)
    applicant.paid = False
    session.add(applicant)
    session.commit()
    session.refresh(applicant)
    log_action(session, applicant.unique_code, "renewed")
    return applicant


def mark_paid(session: Session, applicant_id: int) -> Applicant | None:
    """Mark an applicant's current application or renewal as paid."""
    applicant = session.get(Applicant, applicant_id)
    if applicant is None:
        return None
    applicant.paid = True
    if applicant.renewal_due_at is None:
        applicant.renewal_due_at = applicant.application_date + timedelta(days=RENEWAL_PERIOD_DAYS)
    session.add(applicant)
    session.commit()
    session.refresh(applicant)
    log_action(session, applicant.unique_code, "payment_confirmed")
    return applicant


def remove_applicant(session: Session, applicant_id: int) -> Applicant | None:
    """Soft-delete an applicant: flag as removed but keep the record for future queries."""
    applicant = session.get(Applicant, applicant_id)
    if applicant is None:
        return None
    applicant.status = ApplicationStatus.REMOVED
    applicant.removed_at = date.today()
    session.add(applicant)
    session.commit()
    session.refresh(applicant)
    log_action(session, applicant.unique_code, "removed")
    return applicant


def list_due_for_renewal(session: Session, as_of: date | None = None) -> list[Applicant]:
    """List active applicants who have not renewed more than 6 months past their due date."""
    as_of = as_of or date.today()
    cutoff = as_of - timedelta(days=NOT_RENEWED_FLAG_DAYS)
    statement = (
        select(Applicant)
        .where(Applicant.status == ApplicationStatus.ACTIVE)
        .where(Applicant.renewal_due_at.is_not(None))
        .where(Applicant.renewal_due_at < cutoff)
        .order_by(Applicant.renewal_due_at)
    )
    return list(session.exec(statement))


def get_queue_position(session: Session, applicant_id: int) -> tuple[int, int] | None:
    """Return (overall position, position within chosen option) among active applicants, 1-based."""
    applicant = session.get(Applicant, applicant_id)
    if applicant is None or applicant.status != ApplicationStatus.ACTIVE:
        return None
    active = list_applicants(session, status=ApplicationStatus.ACTIVE)
    overall = next(i for i, a in enumerate(active, start=1) if a.id == applicant.id)
    same_option = [a for a in active if a.option_selected == applicant.option_selected]
    in_option = next(i for i, a in enumerate(same_option, start=1) if a.id == applicant.id)
    return overall, in_option


def create_offer(
    session: Session, applicant_id: int, unit_number: str, date_offered: date | None = None
) -> Offer:
    """Record that a unit has been offered to an applicant."""
    offer = Offer(
        applicant_id=applicant_id,
        unit_number=unit_number,
        date_offered=date_offered or date.today(),
    )
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def list_offers(session: Session, applicant_id: int) -> list[Offer]:
    """List all offers made to an applicant, most recent first."""
    statement = select(Offer).where(Offer.applicant_id == applicant_id).order_by(Offer.date_offered.desc())
    return list(session.exec(statement))


def respond_offer(session: Session, offer_id: int, accepted: bool) -> Offer | None:
    """Record an applicant's acceptance or rejection of an offer."""
    offer = session.get(Offer, offer_id)
    if offer is None:
        return None
    offer.response = OfferResponse.ACCEPTED if accepted else OfferResponse.REJECTED
    offer.date_responded = date.today()
    session.add(offer)
    session.commit()
    session.refresh(offer)
    return offer


def generate_availability_report(
    session: Session, option_type: OptionType, unit_type: str | None = None
) -> list[Applicant]:
    """List active applicants for a given option (and optional unit type), in application order."""
    statement = (
        select(Applicant)
        .where(Applicant.status == ApplicationStatus.ACTIVE)
        .where(Applicant.option_selected == option_type)
    )
    if unit_type:
        statement = statement.where(Applicant.unit_type_preference == unit_type)
    return list(session.exec(statement.order_by(Applicant.application_date)))


def get_wait_rate(session: Session, option_type: OptionType) -> int:
    """Return the configured units-per-year estimate for an option (default 1)."""
    config = session.get(WaitEstimateConfig, option_type)
    return config.units_per_year if config else 1


def set_wait_rate(session: Session, option_type: OptionType, units_per_year: int) -> WaitEstimateConfig:
    """Set the admin-configured units-per-year estimate for an option."""
    config = session.get(WaitEstimateConfig, option_type)
    if config is None:
        config = WaitEstimateConfig(option_type=option_type, units_per_year=units_per_year)
    else:
        config.units_per_year = units_per_year
    session.add(config)
    session.commit()
    session.refresh(config)
    return config
