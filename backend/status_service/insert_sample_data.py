from os import environ
from pymongo import MongoClient, UpdateOne

DATABASE_URL = environ["DATABASE_URL"]


def insert_sample_data():
    try:
        client = MongoClient(DATABASE_URL)
        db = client.get_database()

        db.User.create_index("username", unique=True)

        statuses = [
            {"username": "john_doe", "status": "I hate dogs!"},
            {"username": "jane_smith", "status": "Excited for the weekend!"},
            {"username": "alice_jones", "status": "Just finished a great book."},
            {"username": "bob_brown", "status": "Looking forward to the holidays."},
            {"username": "charlie_black", "status": "Had a great workout today."},
            {"username": "david_white", "status": "Enjoying a nice cup of coffee."},
            {"username": "eve_green", "status": "Feeling grateful."},
            {"username": "frank_blue", "status": "Just watched a great movie."},
            {"username": "grace_red", "status": "Loving the weather today."},
            {"username": "hank_yellow", "status": "I hate dogs!"},
        ]

         # Use bulk write with upsert to avoid conflicts
        db.Status.bulk_write([
            UpdateOne({"username": status["username"]}, {"$set": status}, upsert=True)
            for status in statuses
        ])

        print("Sample data inserted successfully")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    insert_sample_data()
