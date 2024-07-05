from os import environ
from pymongo import MongoClient, UpdateOne

DATABASE_URL = environ["DATABASE_URL"]


def insert_sample_data():
    try:
        client = MongoClient(DATABASE_URL)
        db = client.get_database()

        friends = [
            {"username": "john_doe", "friend_username": "jane_smith"},
            {"username": "alice_jones", "friend_username": "bob_brown"},
            {"username": "charlie_black", "friend_username": "david_white"},
            {"username": "eve_green", "friend_username": "frank_blue"},
            {"username": "grace_red", "friend_username": "hank_yellow"},
        ]

        friend_requests = [
            {"sender_username": "eve_green", "receiver_username": "frank_blue"},
            {"sender_username": "grace_red", "receiver_username": "hank_yellow"},
            {"sender_username": "john_doe", "receiver_username": "alice_jones"},
            {"sender_username": "charlie_black", "receiver_username": "david_white"},
            {"sender_username": "frank_blue", "receiver_username": "eve_green"},
            {"sender_username": "hank_yellow", "receiver_username": "grace_red"},
            {"sender_username": "alice_jones", "receiver_username": "john_doe"},
            {"sender_username": "david_white", "receiver_username": "charlie_black"},
        ]

        blocked_users = [
            {"blocker_username": "john_doe", "blocked_username": "bob_brown"},
            {"blocker_username": "alice_jones", "blocked_username": "jane_smith"},
            {"blocker_username": "eve_green", "blocked_username": "grace_red"},
            {"blocker_username": "frank_blue", "blocked_username": "hank_yellow"},
        ]

        reported_contents = [
            {
                "reporter_username": "john_doe",
                "reported_username": "jane_smith",
                "content": "I hate dogs!",
            },
        ]

        db.Friend.bulk_write([
            UpdateOne({"username": friend["username"]}, {"$set": friend}, upsert=True)
            for friend in friends
        ])
        db.FriendRequest.bulk_write([
            UpdateOne({"sender_username": request["sender_username"], "receiver_username": request["receiver_username"]}, {"$set": request}, upsert=True)
            for request in friend_requests
        ])
        db.BlockedUser.bulk_write([
            UpdateOne({"blocker_username": blocked["blocker_username"], "blocked_username": blocked["blocked_username"]}, {"$set": blocked}, upsert=True)
            for blocked in blocked_users
        ])
        db.ReportedContent.bulk_write([
            UpdateOne({"reporter_username": report["reporter_username"], "reported_username": report["reported_username"]}, {"$set": report}, upsert=True)
            for report in reported_contents
        ])

        print("Sample data inserted successfully")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    insert_sample_data()
