#!/bin/bash
source .venv/bin/activate

# Create temporary DB and migrate to latest
source .dev/create_db.sh

# Run Alembic autogenerate
alembic revision --autogenerate -m "init migration"

# Drop temporary DB
source .dev/drop_db.sh