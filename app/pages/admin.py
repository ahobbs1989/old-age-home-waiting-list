"""Admin / office page: search, edit, reports, offers, and settings."""

from __future__ import annotations

from datetime import date

from nicegui import app, ui

from app import crud
from app.config import ADMIN_PASSWORD
from app.db import get_session
from app.models import (
    Applicant,
    ApplicantUpdate,
    MaritalStatus,
    OptionType,
    Urgency,
)
from app.nav import add_nav

OPTION_LABELS = {o.value: o.name.replace("_", " ").title() for o in OptionType}


def _applicant_row(a: Applicant) -> dict:
    return {
        "id": a.id,
        "code": a.unique_code,
        "name": a.name,
        "phone": a.phone,
        "email": a.email,
        "option": OPTION_LABELS[a.option_selected.value],
        "unit_type": a.unit_type_preference,
        "application_date": str(a.application_date),
        "paid": "Yes" if a.paid else "No",
        "status": a.status.value,
    }


@ui.page("/admin")
def admin_page() -> None:
    add_nav()
    ui.label("Admin").classes("text-2xl font-bold")
    container = ui.column().classes("w-full")

    def render_login() -> None:
        container.clear()
        with container, ui.card().classes("max-w-sm"):
            ui.label("Admin login").classes("text-lg font-semibold")
            password = ui.input("Password", password=True, password_toggle_button=True).classes("w-full")
            error = ui.label("").classes("text-red-600")

            def try_login() -> None:
                if password.value == ADMIN_PASSWORD:
                    app.storage.user["is_admin"] = True
                    render_dashboard()
                else:
                    error.text = "Incorrect password."

            password.on("keydown.enter", lambda: try_login())
            ui.button("Log in", on_click=try_login).classes("mt-2")

    def render_dashboard() -> None:
        container.clear()
        with container:
            with ui.row().classes("w-full justify-between items-center"):
                ui.label("Waiting list administration").classes("text-lg font-semibold")

                def log_out() -> None:
                    app.storage.user["is_admin"] = False
                    render_login()

                ui.button("Log out", on_click=log_out).props("flat")

            with ui.tabs().classes("w-full") as tabs:
                search_tab = ui.tab("Search")
                reports_tab = ui.tab("Reports")
                renewal_tab = ui.tab("Renewal follow-up")
                settings_tab = ui.tab("Wait-time settings")
            with ui.tab_panels(tabs, value=search_tab).classes("w-full"):
                with ui.tab_panel(search_tab):
                    build_search_panel()
                with ui.tab_panel(reports_tab):
                    build_reports_panel()
                with ui.tab_panel(renewal_tab):
                    build_renewal_panel()
                with ui.tab_panel(settings_tab):
                    build_settings_panel()

    def build_search_panel() -> None:
        query_input = ui.input("Search by code, name, email, or phone").classes("w-full max-w-md")
        include_removed = ui.checkbox("Include removed applicants")
        columns = [
            {"name": "code", "label": "Code", "field": "code"},
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "phone", "label": "Phone", "field": "phone"},
            {"name": "email", "label": "Email", "field": "email"},
            {"name": "option", "label": "Option", "field": "option"},
            {"name": "unit_type", "label": "Unit type", "field": "unit_type"},
            {"name": "application_date", "label": "Applied", "field": "application_date"},
            {"name": "paid", "label": "Paid", "field": "paid"},
            {"name": "status", "label": "Status", "field": "status"},
        ]
        table = (
            ui.table(columns=columns, rows=[], row_key="id")
            .classes("w-full")
            .on("rowClick", lambda e: open_edit_dialog(e.args[1]["id"]))
        )

        def search() -> None:
            with get_session() as session:
                results = crud.search_applicants(session, query_input.value or "", include_removed.value)
            table.rows = [_applicant_row(a) for a in results]
            table.update()

        query_input.on("keydown.enter", lambda: search())
        ui.button("Search", on_click=search).classes("mt-2")

        def open_edit_dialog(applicant_id: int) -> None:
            with get_session() as session:
                applicant = crud.get_applicant(session, applicant_id)
            if applicant is None:
                return

            with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl"):
                ui.label(f"{applicant.name} ({applicant.unique_code})").classes("text-lg font-bold")
                name = ui.input("Name", value=applicant.name).classes("w-full")
                phone = ui.input("Phone", value=applicant.phone).classes("w-full")
                email = ui.input("Email", value=applicant.email).classes("w-full")
                address = ui.input("Address", value=applicant.address).classes("w-full")
                marital = ui.select(
                    {s.value: s.name.title() for s in MaritalStatus},
                    value=applicant.marital_status.value,
                    label="Marital status",
                ).classes("w-full")
                option = ui.select(
                    OPTION_LABELS, value=applicant.option_selected.value, label="Option"
                ).classes("w-full")
                unit_type = ui.input("Unit type preference", value=applicant.unit_type_preference).classes(
                    "w-full"
                )
                urgency = ui.select(
                    {u.value: u.name.replace("_", " ").title() for u in Urgency},
                    value=applicant.urgency.value,
                    label="Moving-in status",
                ).classes("w-full")
                ui.label(f"Payment status: {'Paid' if applicant.paid else 'Pending'}")
                ui.label(f"Record status: {applicant.status.value}")

                def save() -> None:
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
                        crud.update_applicant(session, applicant.id, update)
                    ui.notify("Details updated", color="positive")
                    dialog.close()
                    search()

                def mark_paid() -> None:
                    with get_session() as session:
                        crud.mark_paid(session, applicant.id)
                    ui.notify("Marked as paid", color="positive")
                    dialog.close()
                    search()

                def remove() -> None:
                    with get_session() as session:
                        crud.remove_applicant(session, applicant.id)
                    ui.notify("Applicant removed from list")
                    dialog.close()
                    search()

                with ui.row().classes("gap-2 mt-2"):
                    ui.button("Save changes", on_click=save, color="primary")
                    if not applicant.paid:
                        ui.button("Mark as paid", on_click=mark_paid, color="green")
                    if applicant.status.value == "active":
                        ui.button("Remove from list", on_click=remove, color="red")
                    ui.button("Close", on_click=dialog.close).props("flat")

                ui.separator()
                ui.label("Offers").classes("font-semibold")
                offers_column = ui.column().classes("w-full gap-1")

                def refresh_offers() -> None:
                    offers_column.clear()
                    with get_session() as session:
                        current = crud.list_offers(session, applicant.id)
                    with offers_column:
                        if not current:
                            ui.label("No offers recorded yet.").classes("text-sm text-gray-500")
                        for offer in current:
                            with ui.row().classes("items-center gap-2"):
                                ui.label(
                                    f"Unit {offer.unit_number} — offered {offer.date_offered}"
                                    f" — {offer.response.value}"
                                )
                                if offer.response.value == "pending":
                                    ui.button(
                                        "Accepted",
                                        on_click=lambda o=offer: respond(o.id, True),
                                        color="green",
                                    ).props("dense")
                                    ui.button(
                                        "Rejected",
                                        on_click=lambda o=offer: respond(o.id, False),
                                        color="red",
                                    ).props("dense")

                def respond(offer_id: int, accepted: bool) -> None:
                    with get_session() as session:
                        crud.respond_offer(session, offer_id, accepted)
                    refresh_offers()

                refresh_offers()
                with ui.row().classes("items-end gap-2 mt-2"):
                    unit_number_input = ui.input("Unit number").classes("w-40")

                    def add_offer() -> None:
                        if not unit_number_input.value:
                            return
                        with get_session() as session:
                            crud.create_offer(session, applicant.id, unit_number_input.value, date.today())
                        unit_number_input.value = ""
                        refresh_offers()

                    ui.button("Record offer", on_click=add_offer)

            dialog.open()

    def build_reports_panel() -> None:
        option_select = ui.select(OPTION_LABELS, value=OptionType.RENTAL.value, label="Option").classes(
            "w-full max-w-md"
        )
        unit_type_input = ui.input("Unit type (optional, e.g. 2 bed 2 bath)").classes("w-full max-w-md")
        columns = [
            {"name": "application_date", "label": "Applied", "field": "application_date"},
            {"name": "code", "label": "Code", "field": "code"},
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "phone", "label": "Phone", "field": "phone"},
            {"name": "email", "label": "Email", "field": "email"},
            {"name": "unit_type", "label": "Unit type", "field": "unit_type"},
        ]
        report_table = ui.table(columns=columns, rows=[], row_key="code").classes("w-full mt-2")

        def generate() -> None:
            with get_session() as session:
                results = crud.generate_availability_report(
                    session, OptionType(option_select.value), unit_type_input.value or None
                )
            report_table.rows = [_applicant_row(a) for a in results]
            report_table.update()

        ui.button("Generate report", on_click=generate).classes("mt-2")

    def build_renewal_panel() -> None:
        columns = [
            {"name": "code", "label": "Code", "field": "code"},
            {"name": "name", "label": "Name", "field": "name"},
            {"name": "phone", "label": "Phone", "field": "phone"},
            {"name": "email", "label": "Email", "field": "email"},
            {"name": "application_date", "label": "Applied", "field": "application_date"},
        ]
        table = ui.table(columns=columns, rows=[], row_key="code").classes("w-full mt-2")

        def generate() -> None:
            with get_session() as session:
                results = crud.list_due_for_renewal(session)
            table.rows = [_applicant_row(a) for a in results]
            table.update()

        ui.label("Applicants who have not renewed more than 6 months past their due date.").classes(
            "text-sm text-gray-600"
        )
        ui.button("Generate list", on_click=generate).classes("mt-2")

    def build_settings_panel() -> None:
        ui.label("Estimated units becoming available per year, by option:").classes("text-sm text-gray-600")
        with get_session() as session:
            rates = {o: crud.get_wait_rate(session, o) for o in OptionType}

        for option_type in OptionType:
            with ui.row().classes("items-center gap-2"):
                ui.label(OPTION_LABELS[option_type.value]).classes("w-48")
                rate_input = ui.number(value=rates[option_type], min=0, step=1).classes("w-32")

                def save(option_type=option_type, rate_input=rate_input) -> None:
                    with get_session() as session:
                        crud.set_wait_rate(session, option_type, int(rate_input.value or 0))
                    ui.notify(f"Saved rate for {OPTION_LABELS[option_type.value]}", color="positive")

                ui.button("Save", on_click=save).props("dense")

    if app.storage.user.get("is_admin"):
        render_dashboard()
    else:
        render_login()
