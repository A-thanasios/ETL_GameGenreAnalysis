from prefect import flow, get_run_logger, task
from prefect.cache_policies import NO_CACHE

from etl.extract.steam_client import SteamClient
from db.steam_users_id.repo import SteamUserRepo

class SteamUsersID:
    def __init__(self, repo: SteamUserRepo, steam_client: SteamClient):
        self.repo = repo
        self.steam_client = steam_client
        self.logger = get_run_logger()

    @flow(name="ETL - Get new Steam users")
    def get_new_users(self, chunk_size:int=100) -> None:
        """
        Get new users from Steam API and store them in the database. This algorithm is checking user friend lists.
        You can specify how many users to check in one run. Default is 100.
        :param chunk_size: Number of users
        :return: None
        """
        # Read users from DB
        user_lst = self.read_users_from_db(chunk_size)

        # If no users fetched, log an error and exit. The process would not be able to continue.
        # If less than chunk_size, log a warning.
        if not user_lst:
            self.logger.error("No users fetched from database.")
            return
        elif len(user_lst) < chunk_size:
            self.logger.warning(f"Fetched only {len(user_lst)} users from database, expected {chunk_size}.")
        else:
            self.logger.info(f"Fetching {len(user_lst)} users from database. Expected: {chunk_size}.")

        # Get new user ids from Steam API
        new_users_list = self.get_new_ids(user_lst)

        # Try to save new user ids to DB
        self.save_to_db(new_users_list)

    @task(name="Reading database", cache_policy=NO_CACHE)
    def read_users_from_db(self, chunk_size: int) -> list:
        """
        Read users from DB
        :param chunk_size: number of users to read
        :return: a list of User objects
        """
        # Never checked public users first
        user_lst = self.repo.read(
            filter_by={'isPrivate': False, 'updatedAt': None},
            limit=chunk_size)
        self.logger.info(f"{len(user_lst)} never checked users found.")

        # If a list is not full, then public users, ordered by update time
        if len(user_lst) < chunk_size:
            updated = self.repo.read(
                filter_by={'isPrivate': False},
                ordered_by={'updatedAt': False},
                limit=chunk_size)

            user_lst.extend(updated)
            self.logger.info(f"{len(updated)} never checked users found.")

        # If a list is not full, then private users, ordered by update time
        if len(user_lst) < chunk_size:
            private = self.repo.read(
                filter_by={'isPrivate': True},
                ordered_by={'updatedAt': False},
                limit=chunk_size)
            user_lst.extend(private)
            self.logger.info(f"{len(private)} private users found.")

        return user_lst

    @task(name="Calling Steam API", cache_policy=NO_CACHE)
    def get_new_ids(self, user_lst) -> list[str]:
        """
        Get new user ids from Steam API
        :param user_lst: a list of User objects
        :return: a list of new user ids
        """
        new_users_list = []

        # Statistics
        ok_count = 0
        empty_count = 0
        private_count = 0
        error_count = 0

        for user in user_lst:
            try:
                code, json = self.steam_client.get_user_friend_list(user.steam_id)
            except Exception as e:
                self.logger.error(f"Error fetching friend list for user {user.steam_id}: {e}")
                error_count += 1
                continue

            if code == 200:
                friend_dict_list = json['friendslist']['friends']
                friend_list = [friend.get('steamid') for friend in friend_dict_list]

                if not friend_list:
                    self.logger.info(f"No friends found for user {user.steam_id}")
                    empty_count += 1
                else:
                    new_users_list.extend(friend_list)
                    self.repo.update(user.steam_id, is_private=False)
                    ok_count += 1

            elif code == 401:
                self.repo.update(user.steam_id, is_private=True)
                private_count += 1
            else:
                self.logger.error(f"Error fetching friend list for user {user.steam_id}")
                self.logger.error(f"Response code: {code}, Response: {json}")
                error_count += 1

        self.logger.info(f"Friend list fetch summary: OK: {ok_count}, No friends: {empty_count}, Private: {private_count}, Errors: {error_count}")
        return new_users_list

    @task(name="Saving to database", cache_policy=NO_CACHE)
    def save_to_db(self, new_users_list: list[str]) -> None:
        """
        Save new user to DB
        :param new_users_list: list of new user ids
        :return: None
        """
        # If any users found, store them in the database
        if new_users_list:
            self.logger.info(f"Users found: {len(new_users_list)}")
            result = self.repo.create(new_users_list)
            self.logger.info(f"Users stored in the database: {len(result.fetchall())}")
        else:
            self.logger.warning("No users found.")