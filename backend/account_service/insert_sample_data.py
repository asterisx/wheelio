from os import environ
from pymongo import MongoClient, UpdateOne
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SALT = environ["SALT"]
DATABASE_URL = environ["DATABASE_URL"]


def insert_sample_data():
    try:
        client = MongoClient(DATABASE_URL)
        db = client.get_database()

        db.User.create_index("username", unique=True)
        db.PrivacySetting.create_index("username", unique=True)

        users = [
            {"username": "john_doe", "password": pwd_context.hash("password123" + SALT)},
            {"username": "jane_smith", "password": pwd_context.hash("password123" + SALT)},
            {"username": "alice_jones", "password": pwd_context.hash("password123" + SALT)},
            {"username": "bob_brown", "password": pwd_context.hash("password123" + SALT)},
            {"username": "charlie_black", "password": pwd_context.hash("password123" + SALT)},
            {"username": "david_white", "password": pwd_context.hash("password123" + SALT)},
            {"username": "eve_green", "password": pwd_context.hash("password123" + SALT)},
            {"username": "frank_blue", "password": pwd_context.hash("password123" + SALT)},
            {"username": "grace_red", "password": pwd_context.hash("password123" + SALT)},
            {"username": "hank_yellow", "password": pwd_context.hash("password123" + SALT)},
        ]

        privacy_settings = [
            {"username": "john_doe", "profile_private": False},
            {"username": "jane_smith", "profile_private": False},
            {"username": "alice_jones", "profile_private": False},
            {"username": "bob_brown", "profile_private": False},
            {"username": "charlie_black", "profile_private": False},
            {"username": "david_white", "profile_private": False},
            {"username": "eve_green", "profile_private": False},
            {"username": "frank_blue", "profile_private": False},
            {"username": "grace_red", "profile_private": False},
            {"username": "hank_yellow", "profile_private": False},
        ]

        db.User.bulk_write([
            UpdateOne({"username": user["username"]}, {"$set": user}, upsert=True)
            for user in users
        ])
        db.PrivacySetting.bulk_write([
            UpdateOne({"username": setting["username"]}, {"$set": setting}, upsert=True)
            for setting in privacy_settings
        ])

        print("Sample data inserted successfully")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    insert_sample_data()
