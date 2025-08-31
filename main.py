import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.db.user_src.users import User

def main():
    load_dotenv(dotenv_path='.venv/.env')
    steam_api_key = os.getenv('STEAM_API_KEY')
    if not steam_api_key:
        print("Steam API key not found.")
        exit(1)

    print("Running")
    db_url = os.getenv('SQLALCHEMY_URL')
    engine = create_engine(db_url, echo=True)
    print(User.get_user(engine, '76561198277452552'))

if __name__ == "__main__":
    main()