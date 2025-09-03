from src.db.user_src.user_src_repo import UserSrcRepo
from src.db.user_src.users import User


class UserSrcService:
    # Get a list of users
    def get_new_users(self, repo: UserSrcRepo, chunk_size: int = 100):
        print(repo.read(filter_by={User.isPrivate: False}, ordered_by={User.createdAt: True}, limit=10))

        # Not updated first
        # Then If updated, and isPrivate is false
        # Else If updated > year and isPrivate is true

    # Fetch their friend list

    # if a response is 401 update user to private

    # if a response is ok and give it users, try to save them into db