import os

from dotenv import load_dotenv

from src.SteamAPI import get_user_games_data



def main():
    load_dotenv(dotenv_path='.venv/.env')
    steam_api_key = os.getenv('STEAM_API_KEY')
    if not steam_api_key:
        print("Steam API key not found.")
        exit(1)

    print("Running")
    get_user_games_data(steam_api_key, '76561198287452552')


if __name__ == "__main__":
    main()