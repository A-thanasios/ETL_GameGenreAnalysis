import httpx

allowed_format = ['json']

def get_user_games_data(api_key: str, player_id: str,
                    include_played_free_games: bool=True,
                    include_appinfo: bool=True,
                    response_format: allowed_format= 'json'):
    params = {
        'key': api_key,
        'steamid': player_id,
        'include_played_free_games': include_played_free_games,
        'include_appinfo': include_appinfo,
        'format': response_format
    }
    r = httpx.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1',
                  params=params)
    print(r)
    print(r.json())

def get_user_friend_list(api_key: str, player_id: str):
    params = {
        'key': api_key,
        'steamid': player_id,
        'relationship': 'all'
    }

    r = httpx.get('https://api.steampowered.com/ISteamUser/GetFriendList/v0001',
                  params=params)
    print(r)
    print(r.json())