#!/usr/bin/env bash

python -m alembic upgrade head
python -m uvicorn taskmaster.app:app --host 0.0.0.0 --port $PORT
