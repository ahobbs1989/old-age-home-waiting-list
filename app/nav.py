"""Shared navigation header for all pages."""

from nicegui import ui


def add_nav() -> None:
    with ui.header().classes("items-center justify-between"):
        ui.link("Waiting List", "/").classes("text-white text-lg no-underline")
        with ui.row():
            ui.link("Join", "/join").classes("text-white no-underline")
            ui.link("Status", "/status").classes("text-white no-underline")
            ui.link("Renew", "/renew").classes("text-white no-underline")
            ui.link("Admin", "/admin").classes("text-white no-underline")
