#!/bin/sh

echo "Waiting for PostgreSQL..."

python - <<'PY'
import os
import time
import psycopg2

database_url = os.environ["DATABASE_URL"]

for attempt in range(30):
    try:
        connection = psycopg2.connect(database_url)
        connection.close()
        print("PostgreSQL is ready!")
        break
    except psycopg2.OperationalError:
        print(f"PostgreSQL not ready yet. Attempt {attempt + 1}/30...")
        time.sleep(2)
else:
    echo_error = "PostgreSQL did not become ready within 60 seconds."
    raise SystemExit(echo_error)

PY

echo "Applying database migrations..."

alembic upgrade head

echo "Starting FastAPI..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000

