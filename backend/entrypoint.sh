#!/bin/sh

echo "Waiting for PostgreSQL..."

sleep 5

echo "Applying database migrations..."

alembic upgrade head

echo "Starting FastAPI..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload