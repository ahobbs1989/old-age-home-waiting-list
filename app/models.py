"""SQLModel table and input models for the waiting list system."""

from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class MaritalStatus(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    PARTNER = "partner"


class OptionType(str, Enum):
    RENTAL = "rental"
    LIFE_RIGHT_SINGLE = "life_right_single"
    LIFE_RIGHT_COUPLE = "life_right_couple"


class Urgency(str, Enum):
    ASAP = "asap"
    LONG_TERM = "long_term"


class ApplicationStatus(str, Enum):
    ACTIVE = "active"
    REMOVED = "removed"


class OfferResponse(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ApplicantBase(SQLModel):
    """Fields captured about the primary applicant and, if applicable, their spouse."""

    name: str
    id_number: str
    phone: str
    email: str
    address: str
    is_ethekwini: bool = False
    date_of_birth: date
    marital_status: MaritalStatus = MaritalStatus.SINGLE

    spouse_name: str | None = None
    spouse_id_number: str | None = None
    spouse_phone: str | None = None
    spouse_email: str | None = None

    option_selected: OptionType = OptionType.RENTAL
    unit_type_preference: str
    urgency: Urgency = Urgency.LONG_TERM


class Applicant(ApplicantBase, table=True):
    """A person on the waiting list, uniquely identified by `unique_code`."""

    id: int | None = Field(default=None, primary_key=True)
    unique_code: str | None = Field(default=None, unique=True, index=True)
    application_date: date
    status: ApplicationStatus = ApplicationStatus.ACTIVE
    paid: bool = False
    last_renewed_at: date | None = None
    renewal_due_at: date | None = None
    removed_at: date | None = None


class ApplicantCreate(ApplicantBase):
    """Input model for joining the waiting list."""


class ApplicantUpdate(SQLModel):
    """Input model for editing an applicant; all fields optional."""

    name: str | None = None
    id_number: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    is_ethekwini: bool | None = None
    date_of_birth: date | None = None
    marital_status: MaritalStatus | None = None
    spouse_name: str | None = None
    spouse_id_number: str | None = None
    spouse_phone: str | None = None
    spouse_email: str | None = None
    option_selected: OptionType | None = None
    unit_type_preference: str | None = None
    urgency: Urgency | None = None


class Offer(SQLModel, table=True):
    """A unit offered to an applicant, and their response."""

    id: int | None = Field(default=None, primary_key=True)
    applicant_id: int = Field(foreign_key="applicant.id", index=True)
    unit_number: str
    date_offered: date
    response: OfferResponse = OfferResponse.PENDING
    date_responded: date | None = None


class WaitEstimateConfig(SQLModel, table=True):
    """Admin-configured estimate of units becoming available per year, per option."""

    option_type: OptionType = Field(primary_key=True)
    units_per_year: int = 1


class AuditLogEntry(SQLModel, table=True):
    """Lightweight record of admin actions, for the 'keep deleted info' requirement."""

    id: int | None = Field(default=None, primary_key=True)
    applicant_code: str
    action: str
    detail: str = ""
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
