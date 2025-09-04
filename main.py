import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.SteamAPIClient import *
from src.db.database_factory import DatabaseFactory, DBType

from src.db.user_src.user_src_repo import UserSrcRepo
from src.user_src_service import UserSrcService


def main():
    load_dotenv(dotenv_path='.venv/.env')
    steam_api_key = os.getenv('STEAM_API_KEY')
    if not steam_api_key:
        print("Steam API key not found.")
        exit(1)
    user_src_db = DatabaseFactory.init_db(DBType.USER_SRC)
    user_src_repo = UserSrcRepo(user_src_db)
    steam_api_client = SteamAPIClient(steam_api_key)
    user_src_service = UserSrcService(user_src_repo, steam_api_client)

    print("Running")
    user_src_service.get_new_users(chunk_size=10)
    exit(0)
    #data = get_user_games_data(steam_api_key, '76561198015279647')
    #friends = get_user_friend_list(steam_api_key, '76561198015279647')

    print(f"{data} \n {friends}")

if __name__ == "__main__":
    main()