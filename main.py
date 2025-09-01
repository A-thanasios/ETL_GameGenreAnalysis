import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.SteamAPI import *
from src.db.database_factory import DatabaseFactory, DBType

from src.db.user_src.users import User
from src.db.user_src.user_src_repo import UserSrcRepo


def main():
    load_dotenv(dotenv_path='.venv/.env')
    steam_api_key = os.getenv('STEAM_API_KEY')
    if not steam_api_key:
        print("Steam API key not found.")
        exit(1)
    user_src_db = DatabaseFactory.init_db(DBType.USER_SRC)
    user_src_repo = UserSrcRepo(user_src_db)

    print("Running")



    db_url = os.getenv('SQLALCHEMY_URL')
    engine = create_engine(db_url, echo=True)
    #print(User.get_users(engine, ['76561198287452552']))
    data = get_user_games_data(steam_api_key, '76561198015279647')
    friends = get_user_friend_list(steam_api_key, '76561198015279647')

    print(f"{data} \n {friends}")

if __name__ == "__main__":
    main()