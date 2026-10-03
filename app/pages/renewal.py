"""Public page: renew, update, or withdraw from the waiting list."""

from __future__ import annotations

from datetime import date

from nicegui import ui

from app import crud
from app.db import get_session
from app.models import ApplicantUpdate, MaritalStatus, OptionType, Urgency
from app.nav import add_nav
from app.pages.join import BANKING_DETAILS


@ui.page("/renew")
def renewal_page() -> None:
    add_nav()
    ui.label("Renew / Update Your Application").classes("text-2xl font-bold")

    state: dict = {"applicant_id": None}

    with ui.card().classes("w-full max-w-2xl"):
        code_input = ui.input("Your unique waiting-list code").classes("w-full")
        lookup_error = ui.label("").classes("text-red-600")
        form_area = ui.column().classes("w-full gap-2")
        form_area.set_visibility(False)

        def load() -> None:
            form_area.clear()
            lookup_error.text = ""
            with get_session() as session:
                applicant = crud.get_applicant_by_code(session, code_input.value or "")
            if applicant is None:
                lookup_error.text = "No application found with that code."
                form_area.set_visibility(False)
                return
            state["applicant_id"] = applicant.id

            with form_area:
                ui.label(f"Welcome back, {applicant.name}").classes("font-semibold")
                name = ui.input("Full name", value=applicant.name).classes("w-full")
                phone = ui.input("Phone", value=applicant.phone).classes("w-full")
                email = ui.input("Email", value=applicant.email).classes("w-full")
                address = ui.input("Address", value=applicant.address).classes("w-full")
                marital = ui.select(
                    {s.value: s.name.title() for s in MaritalStatus},
                    value=applicant.marital_status.value,
                    label="Marital status",
                ).classes("w-full")
                option = ui.select(
                    {o.value: o.name.replace("_", " ").title() for o in OptionType},
                    value=applicant.option_selected.value,
                    label="Option applying for",
                ).classes("w-full")
                unit_type = ui.input("Unit type preference", value=applicant.unit_type_preference).classes(
                    "w-full"
                )
                urgency = ui.select(
                    {u.value: u.name.replace("_", " ").title() for u in Urgency},
                    value=applicant.urgency.value,
                    label="Moving-in status",
                ).classes("w-full")

                outcome = ui.column().classes("w-full gap-1")

                def save_changes() -> None:
                    update = ApplicantUpdate(
                        name=name.value,
                        phone=phone.value,
                        email=email.value,
                        address=address.value,
                        marital_status=MaritalStatus(marital.value),
                        option_selected=OptionType(option.value),
                        unit_type_preference=unit_type.value,
                        urgency=Urgency(urgency.value),
                    )
                    with get_session() as session:
                        crud.update_applicant(session, state["applicant_id"], update)
                        crud.renew_applicant(session, state["applicant_id"])
                    outcome.clear()
                    with outcome:
                        ui.label(
                            f"Renewed as of {date.today()}. Please pay the renewal fee via EFT:"
                        ).classes("font-semibold text-green-700")
                        for label, value in BANKING_DETAILS.items():
                            ui.label(f"{label}: {value}")
                    ui.notify("Renewal submitted", color="positive")

                def renew_no_changes() -> None:
                    with get_session() as session:
                        crud.renew_applicant(session, state["applicant_id"])
                    outcome.clear()
                    with outcome:
                        ui.label(
                            f"Renewed as of {date.today()} with no changes. Please pay via EFT:"
                        ).classes("font-semibold text-green-700")
                        for label, value in BANKING_DETAILS.items():
                            ui.label(f"{label}: {value}")
                    ui.notify("Renewal submitted", color="positive")

                def remove_me() -> None:
                    def confirm() -> None:
                        with get_session() as session:
                            crud.remove_applicant(session, state["applicant_id"])
                        dialog.close()
                        outcome.clear()
                        with outcome:
                            ui.label("You have been removed from the waiting list.").classes("font-semibold")
                        ui.notify("Removed from waiting list")

                    with ui.dialog() as dialog, ui.card():
                        ui.label("Are you sure you want to be removed from the waiting list?")
                        with ui.row():
                            ui.button("Cancel", on_click=dialog.close)
                            ui.button("Yes, remove me", on_click=confirm, color="red")
                    dialog.open()

                with ui.row().classes("gap-2 mt-2"):
                    ui.button("No changes — renew", on_click=renew_no_changes)
                    ui.button("Update details & renew", on_click=save_changes, color="primary")
                    ui.button("Remove me from the list", on_click=remove_me, color="red")

            form_area.set_visibility(True)

        ui.button("Look up my application", on_click=load).classes("mt-2")
