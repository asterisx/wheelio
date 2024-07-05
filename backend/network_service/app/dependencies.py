from typing import List
from schemas import Friend


async def get_friends_for_user(username: str) -> List[str]:
    friends = await Friend.find(Friend.username == username).to_list()
    return [friend.friend_username for friend in friends]
