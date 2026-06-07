#!/usr/bin/env bash
set -e
echo "Running alembic upgrade head..."
alembic upgrade head
echo "Migrations applied."
