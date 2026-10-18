#!/bin/sh
set -e
echo "Running migrations..."
alembic upgrade head
echo "Bootstrapping rubrics/admin..."
python -m app.scripts.bootstrap
if [ "${SEED_QUESTIONS:-true}" = "true" ]; then
  echo "Seeding missing questions (existing ones are never overwritten)..."
  python -m app.scripts.kb seed
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
