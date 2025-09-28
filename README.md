# Game Genre Analysis (Steam users)

In the phase of small ETL service that crawls Steam friend lists and stores Steam user metadata for downstream analysis and research.

This repository contains a lightweight extractor that reads Steam user IDs, fetches friend lists via the Steam Web API, and persists user metadata to a relational database for purpose of futher use.

## Contents

- `src/etl/extract/steam_api_client.py` — HTTP client for calling Steam Web API.
- `src/etl/extract/steam_users_id.py` — logic for reading user id sources and driving extraction.
- `src/db/` — database layer, repositories and factories used for persistence.

## Features

- Crawl Steam friend lists and insert new users into the DB.
- Track privacy state per user.
- Support for batched extraction and configurable rate limits.
- Database migrations managed with Alembic.
- Model is build with useage of SQLAlchemy

## Quickstart

Prerequisites

- Steam Web API key
- Docker Engine and Compose
- Starting list of user ids (preferred in csv file
- )

### 1. Create a virtual environment and install requirements

I used **venv** as my manager, if you want to use diferent, you need to change loading enviromental variables logic insid src/main.py/prepare_env

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Provide environment variables

Create a `.env` file and/or use provided template `.dev/.env` inside of `venv` folder.

#### ⚠️ Change given names and passwords for your own credentials ⚠️

Environment variables used by the project (common names found in the codebase):

- `STEAM_API_KEY` — Steam Web API key.
- `SQLALCHEMY_URL` — full SQLAlchemy connection URL (in case you want to run db localy).
- `APP_DB_NAME`, `APP_DB_USER`, `APP_DB_PASSWORD`, `APP_DB_HOST`, `APP_DB_PORT` — alternate DB configuration used by some init scripts.

### 3. Run builder

```bash
source .dev/build.sh
```

There is an init script under `alembic/init.sh` used in container setups. If you want to dockerize the app, ensure the container has the `STEAM_API_KEY` and DB connection env vars set and that migrations are applied at startup.

## Development notes

- Alembic migrations are stored in `alembic/versions/` (see `693be165eaeb_update_isextracted_to_extractedat_.py` and `9a7cf47454a6_sync_models.py`).
- Database factory and repository helpers are under `src/db/` and `src/db/steam_users_id/`.
- Example input data lives in `res/players.csv`.

## Testing and small checks

- There are no formal unit tests included. For quick checks, run small Python REPL scripts that import client modules and run a single API call (honoring Steam API rate limits).

## TODO / Ideas

- Add unit tests for API client and repository logic.
- Add configuration to run scheduled extraction (e.g., Prefect or cron wrapper).
- Improve README with example API responses and DB schema documentation.

## License

This repository does not include an explicit license file. Add an appropriate `LICENSE` if you intend to publish or share the code.

---

If you'd like, I can also:

- Add an example `.env.example` file with the required env vars.
- Create a small Dockerfile / docker-compose snippet to run DB + extractor for local development.

Tell me which of those you'd like next.
