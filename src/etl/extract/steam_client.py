import httpx
from sqlalchemy.orm import Mapped

class SteamClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key not found.")
        
        self._api_key = api_key

    def get_user_games_data(self, player_id: str,
                        include_played_free_games: bool=True,
                        include_appinfo: bool=True):
        params = {
            'key': self._api_key,
            'steamid': player_id,
            'include_played_free_games': include_played_free_games,
            'include_appinfo': include_appinfo,
        }
        r = httpx.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1',
                    params=params)
        return r.status_code, r.json()

    def get_user_friend_list(self, player_id: str|Mapped[str]):
        params = {
            'key': self._api_key,
            'steamid': player_id,
            'relationship': 'all'
        }
        r = httpx.get('https://api.steampowered.com/ISteamUser/GetFriendList/v0001',
                    params=params)

        return r.status_code, r.json()
