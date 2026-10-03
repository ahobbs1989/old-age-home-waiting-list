"""POC configuration constants."""

import os

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
STORAGE_SECRET = os.environ.get("STORAGE_SECRET", "poc-dev-secret-change-me")

# Lets a hosting platform point the database at a persistent volume, e.g. DB_PATH=/data/app.db.
DB_PATH = os.environ.get("DB_PATH", "app.db")
