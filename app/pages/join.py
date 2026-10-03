"""Public page: join the waiting list."""

from __future__ import annotations

from datetime import date

from nicegui import ui

from app import crud
from app.db import get_session
from app.logic import calculate_age, recommend_options
from app.models import ApplicantCreate, MaritalStatus, OptionType, Urgency
from app.nav import add_nav

BANKING_DETAILS = {
    "Account name": "Old Age Home Waiting List Trust",
    "Bank": "Example Bank",
    "Account number": "0123456789",
    "Branch code": "000000",
    "Reference": "Your unique code (shown below)",
}


@ui.page("/join")
def join_page() -> None:
    add_nav()
    ui.label("Join the Waiting List").classes("text-2xl font-bold")

    with ui.card().classes("w-full max-w-2xl"):
        ui.label("Your details").classes("text-lg font-semibold")
        name = ui.input("Full name").classes("w-full")
        id_number = ui.input("ID number").classes("w-full")
        phone = ui.input("Phone").classes("w-full")
        email = ui.input("Email").classes("w-full")
        address = ui.input("Address").classes("w-full")
        is_ethekwini = ui.checkbox("Resident of Ethekwini")
        dob = ui.input("Date of birth (YYYY-MM-DD)").classes("w-full")
        marital = ui.select(
            {s.value: s.name.title() for s in MaritalStatus},
            value=MaritalStatus.SINGLE.value,
            label="Marital status",
        ).classes("w-full")

        spouse_box = ui.column().classes("w-full gap-2")
        with spouse_box:
            ui.label("Spouse / partner details").classes("font-semibold")
            spouse_name = ui.input("Spouse full name").classes("w-full")
            spouse_id_number = ui.input("Spouse ID number").classes("w-full")
            spouse_phone = ui.input("Spouse phone").classes("w-full")
            spouse_email = ui.input("Spouse email").classes("w-full")
        spouse_box.set_visibility(False)

        recommendation_label = ui.label("").classes("text-sm text-blue-700")

        def refresh_recommendation() -> None:
            spouse_box.set_visibility(marital.value != MaritalStatus.SINGLE.value)
            try:
                age = calculate_age(date.fromisoformat(dob.value))
            except (ValueError, TypeError):
                recommendation_label.text = ""
                return
            options = recommend_options(age, MaritalStatus(marital.value))
            names = ", ".join(o.name.replace("_", " ").title() for o in options)
            recommendation_label.text = f"Based on your details, you may want to consider: {names}"

        dob.on("blur", lambda: refresh_recommendation())
        marital.on_value_change(lambda: refresh_recommendation())

        ui.separator()
        ui.label("Your preferences").classes("text-lg font-semibold")
        option = ui.select(
            {o.value: o.name.replace("_", " ").title() for o in OptionType},
            value=OptionType.RENTAL.value,
            label="Option applying for",
        ).classes("w-full")
        unit_type = ui.input("Unit type preference (e.g. 2 bed 2 bath)").classes("w-full")
        urgency = ui.select(
            {u.value: u.name.replace("_", " ").title() for u in Urgency},
            value=Urgency.LONG_TERM.value,
            label="Moving-in status",
        ).classes("w-full")

        error_label = ui.label("").classes("text-red-600")
        result_card = ui.card().classes("w-full")
        result_card.set_visibility(False)

        def submit() -> None:
            required = {
                "Full name": name.value,
                "ID number": id_number.value,
                "Phone": phone.value,
                "Email": email.value,
                "Address": address.value,
                "Date of birth": dob.value,
                "Unit type preference": unit_type.value,
            }
            missing = [label for label, value in required.items() if not value]
            if missing:
                error_label.text = f"Please fill in: {', '.join(missing)}"
                return
            try:
                dob_value = date.fromisoformat(dob.value)
            except ValueError:
                error_label.text = "Date of birth must be in YYYY-MM-DD format."
                return

            error_label.text = ""
            data = ApplicantCreate(
                name=name.value,
                id_number=id_number.value,
                phone=phone.value,
                email=email.value,
                address=address.value,
                is_ethekwini=is_ethekwini.value,
                date_of_birth=dob_value,
                marital_status=MaritalStatus(marital.value),
                spouse_name=spouse_name.value or None,
                spouse_id_number=spouse_id_number.value or None,
                spouse_phone=spouse_phone.value or None,
                spouse_email=spouse_email.value or None,
                option_selected=OptionType(option.value),
                unit_type_preference=unit_type.value,
                urgency=Urgency(urgency.value),
            )
            with get_session() as session:
                applicant = crud.create_applicant(session, data)

            result_card.clear()
            with result_card:
                ui.label("Application received!").classes("text-xl font-bold text-green-700")
                ui.label(f"Your unique waiting-list code is: {applicant.unique_code}").classes("text-lg")
                ui.label("Please keep this code safe — you'll need it to check your status or renew.")
                ui.separator()
                ui.label("To complete your application, please pay the registration fee via EFT:").classes(
                    "font-semibold"
                )
                for label, value in BANKING_DETAILS.items():
                    ui.label(f"{label}: {value}")
                ui.label(
                    "Our office will confirm your payment once received. "
                    "Your place on the list is reserved from your application date regardless."
                ).classes("text-sm text-gray-600")
            result_card.set_visibility(True)
            ui.notify("Application submitted", color="positive")

        ui.button("Submit application", on_click=submit).classes("mt-4")
