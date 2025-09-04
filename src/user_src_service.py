from src.SteamAPIClient import SteamAPIClient
from src.db.user_src.user_src_repo import UserSrcRepo

class UserSrcService:
    def __init__(self, repo: UserSrcRepo, steam_client: SteamAPIClient):
        self.repo = repo
        self.steam_client = steam_client


    def get_new_users(self, chunk_size:int=100):
        # Get a list of users
            # Not updated not private first
        user_lst = self.repo.read(
            filter_by={'isPrivate': False, 'updatedAt': None},
            limit=chunk_size)

            # Then If updated, and isPrivate is false
        if len(user_lst) < chunk_size:
            user_lst.extend(self.repo.read(
                filter_by={'isPrivate': False},
                ordered_by={'updatedAt': False},
                limit=chunk_size))

        if len(user_lst) < chunk_size:
            # Else If updated > year and isPrivate is true
            user_lst.extend(self.repo.read(
                filter_by={'isPrivate': True},
                ordered_by={'updatedAt': False},
                limit=chunk_size))

        if not user_lst:
            return

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

        if new_users_list:
            print(new_users_list)
            self.repo.create(new_users_list)



    # Fetch their friend list


    # if a response is 401 update user to private

    # if a response is ok and give it users, try to save them into db