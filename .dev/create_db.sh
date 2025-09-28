#!/bin/bash
source .venv/bin/activate
source .venv/.env

# Credentials
PGUSER=$PGUSER
PGPASSWORD=$PGPASSWORD
DBNAME=$TEMP_DB

export PGPASSWORD=$PGPASSWORD
export SQLALCHEMY_URL_DEV="postgresql+psycopg2://$PGUSER:$PGPASSWORD@localhost/$DBNAME"

# Create temporary DB
createdb -h localhost -U $PGUSER $DBNAME

# Update db to current state
alembic upgrade head