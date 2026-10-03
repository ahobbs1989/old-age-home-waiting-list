"""Entry point: builds UI and calls ui.run()."""

import os

from nicegui import ui

from app.config import STORAGE_SECRET
from app.db import create_db_and_tables
from app.nav import add_nav
from app.pages import admin, join, renewal, status  # noqa: F401  (registers @ui.page routes)


@ui.page("/")
def index_page() -> None:
    add_nav()
    ui.label("Old Age Home — Waiting List").classes("text-2xl font-bold")
    ui.label("Please choose an option below.").classes("text-gray-600")
    with ui.column().classes("gap-2 mt-4"):
        ui.link("Join the waiting list", "/join").classes("text-lg")
        ui.link("Check my status", "/status").classes("text-lg")
        ui.link("Renew / update / withdraw", "/renew").classes("text-lg")
        ui.link("Admin", "/admin").classes("text-lg")


create_db_and_tables()

# Hosting platforms (Railway, Render, etc.) assign a port via $PORT; default to 8080 locally.
port = int(os.environ.get("PORT", 8080))

ui.run(title="Old Age Home Waiting List", storage_secret=STORAGE_SECRET, host="0.0.0.0", port=port)
