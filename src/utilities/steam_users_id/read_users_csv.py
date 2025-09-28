import os
import pandas as pd
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine

from db.steam_users_id.users import User


def main():
    if len(sys.argv) < 2:
        print("Usage: python read_users_id_csv.py <filepath>")
        sys.exit(1)
    load_dotenv(dotenv_path='.venv/.env')

    db_url = os.getenv('SQLALCHEMY_URL')
    engine = create_engine(db_url, echo=True)

    chunk_size = 10 ** 6
    with pd.read_csv(sys.argv[1], chunksize=chunk_size) as reader:
        print("Reading CSV file...")
        for chunk in reader:
            User.add_users(engine, chunk['playerid'].tolist())
    print("Users added to database.")
    sys.exit(0)

if __name__ == "__main__":
    main()