CLAUDE.md

Guidance for Claude Code when working in this repository.

Project overview

A proof-of-concept web application for a retirement facility's waiting list: joining, renewal, status/position reporting, and admin search/reporting (see the waiting-list requirements spec for the full brief). The goal is a working, readable POC — favour simplicity and clarity over abstraction. Payment, admin auth, and wait-time estimation are deliberately stubbed/simplified for the POC — see "POC scope notes" below. (README.md is a separate, non-technical guide for end users — download/run/host — and is not a reference for development.)

POC scope notes
Payment is stubbed: EFT banking details are shown on join and renewal; office staff mark an application "paid" manually from the admin search panel. No real payment gateway is integrated.
Admin access is gated by a single shared password (env var ADMIN_PASSWORD, default admin123 — must be changed before any real/public use). There are no individual admin accounts.
Wait-time estimates are a rough calculation (queue position ÷ an admin-configured "units available per year" rate per option type, set under the admin "Wait-time settings" tab). There's no real historical turnover data behind this yet.
Renewal reminders (spec section B) are not automated — the admin "Renewal follow-up" report lists applicants overdue by more than 6 months, for staff to contact manually.

Hard constraints
100% Python. Do not write HTML, CSS, or JavaScript files. All UI is built with NiceGUI's Python API. Inline styling via .classes() (Tailwind) or .props() (Quasar) is acceptable.
No additional frameworks beyond the stack below without asking first. If a new dependency seems necessary, explain why and wait for approval.
SQLite only for persistence. No external database servers.
Keep the app runnable with a single command: python main.py.
Tech stack
Layer	Choice
UI / web	NiceGUI
ORM/models	SQLModel (on SQLAlchemy)
Database	SQLite (app.db file)
Python	3.11+
Project structure
.
├── CLAUDE.md
├── README.md
├── requirements.txt
├── main.py              # Entry point: builds UI and calls ui.run()
├── app/
│   ├── __init__.py
│   ├── db.py            # Engine, session helper, create_db_and_tables()
│   ├── models.py        # SQLModel table classes
│   ├── crud.py          # All database operations (pure functions)
│   ├── logic.py         # Pure business-rule helpers (no DB, no UI)
│   ├── config.py        # POC config constants (admin password, storage secret)
│   ├── nav.py           # Shared header/nav used by every page
│   └── pages/           # One module per page
│       ├── __init__.py
│       ├── join.py      # Public: join the waiting list
│       ├── status.py    # Public: check position / wait estimate
│       ├── renewal.py   # Public: renew / update / withdraw
│       └── admin.py     # Password-gated: search, edit, reports, offers, settings
└── tests/
    ├── conftest.py      # In-memory SQLite fixture
    ├── test_crud.py
    └── test_logic.py
Architecture rules
Layering is strict: pages → crud → models/db. UI code never builds queries or opens sessions directly; it calls functions in crud.py.
crud.py functions take a Session as their first argument and return model instances or plain values. They contain no UI code. Naming: create_<entity>, get_<entity>, list_<entities>, update_<entity>, delete_<entity>.
Sessions: use a short-lived session per operation via a context manager in db.py:
python
   with get_session() as session:
       crud.create_item(session, item)
Models: separate table models from input models where it helps (e.g. ItemBase, Item(ItemBase, table=True), ItemCreate(ItemBase), ItemUpdate with all-optional fields).
Engine config: create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False}) — required because NiceGUI handles requests across threads. DB_PATH (app/config.py) defaults to "app.db" but can be overridden via env var so a host can point it at a persistent volume.
Call create_db_and_tables() once at startup in main.py, before ui.run().
UI conventions (NiceGUI)
Use ui.table (or ui.aggrid if sorting/filtering is needed) to list records.
Use a ui.dialog with form inputs for create and edit; reuse the same dialog builder for both.
Confirm deletes with a dialog before calling crud.delete_*.
After any write, refresh the table (use @ui.refreshable or update table.rows and call table.update()).
Show feedback with ui.notify(...) on success and on error.
Validate required fields in the form before calling crud; show inline errors rather than raising.
Use ui.page('/...') decorators for routes; keep a simple header/nav shared across pages.
Code style
Type hints on all function signatures.
Docstrings on public functions in crud.py and db.py (one line is fine).
Format with ruff format; lint with ruff check.
Prefer small functions and explicit code over clever abstractions — this is a POC others should be able to read quickly.
No print-debugging left in committed code; use logging if output is needed.
Commands
bash
# Setup
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run (default http://localhost:8080)
python main.py

# Test
pytest -q

# Lint / format
ruff check . && ruff format .

requirements.txt should contain only: nicegui, sqlmodel, pytest, ruff.

Testing
Test crud.py directly against an in-memory SQLite engine (sqlite://) created in a pytest fixture; never touch app.db in tests.
Each CRUD function gets at least one happy-path test and one edge case (missing record, invalid update).
UI code is not unit-tested for the POC.
Environment notes
Development may happen on a remote Linux machine. When running the app there, use ui.run(host="0.0.0.0", port=8080) and access it via the machine's address or an SSH tunnel.
Do not assume admin rights or the ability to install system packages; stay within a virtualenv and pip.
Working with Claude
Before large changes, outline the plan briefly and then proceed.
When adding a new entity, update in order: models.py → crud.py → tests → pages/<entity>.py → nav link in main.py.
Run pytest -q and ruff check . after changes and fix any failures before finishing.
app.db is disposable during the POC; if the schema changes, it's acceptable to delete it and recreate (no migrations yet). Mention this when a schema change is made.
Do not commit app.db or .venv/ (ensure .gitignore covers them).