import os


def get_database_url():
    return os.getenv("DATABASE_URL")

