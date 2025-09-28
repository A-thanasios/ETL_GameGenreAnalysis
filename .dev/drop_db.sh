#!/bin/bash
source .venv/bin/activate
source .venv/.env

# Drop temporary DB
dropdb -h localhost -U $PGUSER $TEMP_DB