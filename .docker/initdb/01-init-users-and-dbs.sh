#!/usr/bin/env bash
set -euo pipefail

# Required env (provided by Compose)
: "${POSTGRES_USER:?missing}"
: "${POSTGRES_DB:?missing}"

: "${APP_DB_NAME:?missing}"
: "${APP_DB_USER:?missing}"
: "${APP_DB_PASSWORD:?missing}"

: "${PREFECT_DB_NAME:?missing}"
: "${PREFECT_DB_USER:?missing}"
: "${PREFECT_DB_PASSWORD:?missing}"

# Pass vars to psql and generate SQL only if objects don't exist
psql -v ON_ERROR_STOP=1 \
  --username "${POSTGRES_USER}" \
  --dbname "${POSTGRES_DB}" \
  --set "app_user=${APP_DB_USER}" \
  --set "app_password=${APP_DB_PASSWORD}" \
  --set "app_db=${APP_DB_NAME}" \
  --set "prefect_user=${PREFECT_DB_USER}" \
  --set "prefect_password=${PREFECT_DB_PASSWORD}" \
  --set "prefect_db=${PREFECT_DB_NAME}" <<'SQL'
-- Create App role if missing
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'app_user', :'app_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'app_user') \gexec

-- Create App database if missing
SELECT format('CREATE DATABASE %I OWNER %I', :'app_db', :'app_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = :'app_db') \gexec

-- Create Prefect role if missing
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'prefect_user', :'prefect_password')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'prefect_user') \gexec

-- Create Prefect database if missing
SELECT format('CREATE DATABASE %I OWNER %I', :'prefect_db', :'prefect_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = :'prefect_db') \gexec
SQL