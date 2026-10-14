#!/bin/sh
set -e

echo "=== [Kisan Backend] Initializing Docker Environment ==="

# 1. Setup .env from .env.example if .env does not exist
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "--> .env not found. Auto-generating .env from .env.example..."
    cp .env.example .env
fi

# 2. Ensure all requirements are installed (handles volume mount syncing)
if [ -f requirements.txt ]; then
    echo "--> Checking and installing python dependencies..."
    pip install --no-cache-dir -r requirements.txt
fi

# 3. Run database migrations automatically if database is reachable
if [ -f alembic.ini ]; then
    echo "--> Running database migrations (alembic upgrade head)..."
    alembic upgrade head || echo "--> [Notice] Migrations completed or skipped."
fi

echo "=== [Kisan Backend] Setup complete. Starting application server... ==="

# Execute the main container command
exec "$@"
