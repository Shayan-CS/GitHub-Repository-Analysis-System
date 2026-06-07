#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  echo ".env already exists - leaving it alone"
  exit 0
fi

if [ ! -f .env.example ]; then
  echo ".env.example not found - create one first"
  exit 1
fi

cp .env.example .env
echo "Created .env from .env.example. Edit .env to add secrets before running docker compose."
