from pydantic import ValidationError

from chzzk.model.user import User

user_data = {"hasProfile": True, "officialNotiAgree": True, "officialNotiAgreeUpdatedDate": None, "verifiedMark": False,
             "loggedIn": True, "userIdHash": None, "nickname": "test", "profileImageUrl": None, "penalties": None}
user = User(**user_data)

print(user.nickname)
print(user)

try:
    user_data["test"] = 123
    User(**user_data)
except ValidationError as e:
    print(e)
    raise e

