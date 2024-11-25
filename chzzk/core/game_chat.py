from chzzk.client import GameClient
from chzzk.model import Token


class GameChat:
    def __init__(self, client: GameClient):
        self._game_client = client

    async def access_token(self, chat_channel_id: str) -> Token:
        response = await self._game_client.get(
            f"v1/chats/access-token",
            params={"channelId": chat_channel_id, "chatType": "STREAMING"}
        )

        return Token(**response)
