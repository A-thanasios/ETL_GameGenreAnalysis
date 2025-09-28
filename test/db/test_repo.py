import subprocess

from dotenv import load_dotenv
import pytest
from sqlalchemy import CursorResult

from db.database_factory import DatabaseFactory, DBType
from db.steam_users_id.repo import SteamUserRepo


class TestRepo:
    @pytest.fixture(scope='class')
    def setup(self):
        load_dotenv(dotenv_path='.venv/.env')
        subprocess.run(["bash", ".dev/create_db.sh"], check=True)
        steam_users_db = DatabaseFactory.init_db('test')
        steam_users_repo = SteamUserRepo(steam_users_db)

        yield steam_users_repo

        steam_users_db.engine.dispose()
        subprocess.run(["bash", ".dev/drop_db.sh"], check=True)

    def test_repo(self, setup):
        obj: CursorResult = setup.create('76561198043667710')
        obj2: CursorResult = setup.create('76561198043667710')
        print(obj.fetchall())
        print(obj2.fetchall())