"""Public page: check waiting list position and estimated wait time."""

from __future__ import annotations

from nicegui import ui

from app import crud
from app.db import get_session
from app.logic import estimate_wait_months
from app.models import ApplicationStatus
from app.nav import add_nav


@ui.page("/status")
def status_page() -> None:
    add_nav()
    ui.label("Check Your Waiting List Status").classes("text-2xl font-bold")

    with ui.card().classes("w-full max-w-md"):
        code_input = ui.input("Your unique waiting-list code").classes("w-full")
        result = ui.column().classes("w-full gap-1")

        def check() -> None:
            result.clear()
            with get_session() as session:
                applicant = crud.get_applicant_by_code(session, code_input.value or "")
                if applicant is None:
                    with result:
                        ui.label("No application found with that code.").classes("text-red-600")
                    return
                if applicant.status != ApplicationStatus.ACTIVE:
                    with result:
                        ui.label("This application is no longer active on the waiting list.").classes(
                            "text-red-600"
                        )
                    return
                position = crud.get_queue_position(session, applicant.id)
                rate = crud.get_wait_rate(session, applicant.option_selected)

            with result:
                ui.label(f"Name: {applicant.name}")
                ui.label(f"Option: {applicant.option_selected.name.replace('_', ' ').title()}")
                ui.label(f"Application date: {applicant.application_date}")
                ui.label(f"Payment status: {'Paid' if applicant.paid else 'Pending'}")
                if position:
                    overall, in_option = position
                    ui.label(f"Overall position on waiting list: {overall}")
                    ui.label(f"Position for your chosen option: {in_option}")
                    months = estimate_wait_months(in_option, rate)
                    if months:
                        ui.label(f"Approximate estimated wait: ~{months} months").classes("font-semibold")
                    else:
                        ui.label("Approximate wait time not yet available — contact the office.")

        ui.button("Check status", on_click=check).classes("mt-2")
