#!/usr/bin/env bash

poetry run alembic upgrade head
poetry run python -m uvicorn taskmasterexp.app:app --host 0.0.0.0 --port 8001 --reload --log-level info
