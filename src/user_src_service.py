from prefect import flow, task

from src.SteamAPIClient import SteamAPIClient
from src.db.user_src.user_src_repo import UserSrcRepo

class UserSrcService:
    def __init__(self, repo: UserSrcRepo, steam_client: SteamAPIClient):
        self.repo = repo
        self.steam_client = steam_client

    @task
    def get_new_users(self, chunk_size:int=100):
        user_lst = self.__read_users_id(chunk_size)

        if not user_lst:
            return

        new_users_list = self.__get_new_ids(user_lst)

        if new_users_list:
            self.repo.create(new_users_list)

    @task
    def __read_users_id(self, chunk_size):
        user_lst = self.repo.read(
            filter_by={'isPrivate': False, 'updatedAt': None},
            limit=chunk_size)

        if len(user_lst) < chunk_size:
            user_lst.extend(self.repo.read(
                filter_by={'isPrivate': False},
                ordered_by={'updatedAt': False},
                limit=chunk_size))

        if len(user_lst) < chunk_size:
            user_lst.extend(self.repo.read(
                filter_by={'isPrivate': True},
                ordered_by={'updatedAt': False},
                limit=chunk_size))
        return user_lst

    @task
    def __get_new_ids(self, user_lst):
        new_users_list = []
        for user in user_lst:
            try:
                code, json = self.steam_client.get_user_friend_list(user.steam_id)
            except Exception as e:
                print(f"Error fetching friend list for user {user.steam_id}: {e}")
                continue

            if code == 200:
                friend_dict_list = json['friendslist']['friends']

                friend_list = [friend.get('steamid') for friend in friend_dict_list]

                new_users_list.extend(friend_list)
                self.repo.update(user.steam_id, is_private=False)
            elif code == 401:
                self.repo.update(user.steam_id, is_private=True)
            else:
                print(f"Error fetching friend list for user {user.steam_id}")
        return new_users_list