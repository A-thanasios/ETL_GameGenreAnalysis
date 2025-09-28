import os
from dotenv import load_dotenv

from src.etl.extract.steam_client import SteamClient

class TestSteamClient:
    load_dotenv('.venv/.env')
    steam_api_key = os.getenv('STEAM_API_KEY')
    steam_client = SteamClient(steam_api_key)


    def test_get_user_games_data(self):
        status, json = self.steam_client.get_user_games_data('76561198043667710')
        assert status == 200

    def test_get_user_friend_list(self):
        status, json = self.steam_client.get_user_friend_list('76561198043667710')
        assert status == 200