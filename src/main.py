import os
from dotenv import load_dotenv
from prefect import flow

from etl.extract.steam_client import *
from db.database_factory import DatabaseFactory, DBType

from db.steam_users_id.repo import SteamUserRepo
from etl.extract.steam_users_id import SteamUsersID

@flow(name="Get new Steam users",
      description="Get new Steam users from Steam API and store them in the database.")
def new_users_scheduler():
    steam_ids_extraction = prepare_env()

    steam_ids_extraction.get_new_users()


def prepare_env():
    load_dotenv(dotenv_path='.venv/.env')
    steam_api_key = os.getenv('STEAM_API_KEY')
    if not steam_api_key:
        print("Steam API key not found.")
        exit(1)
    steam_users_db = DatabaseFactory.init_db(DBType.Steam_user)
    steam_users_repo = SteamUserRepo(steam_users_db)
    steam_api_client = SteamClient(steam_api_key)
    steam_ids_extraction = SteamUsersID(steam_users_repo, steam_api_client)
    return steam_ids_extraction


if __name__ == "__main__":
    new_users_scheduler.serve(
        cron='0 * * * *'
    )