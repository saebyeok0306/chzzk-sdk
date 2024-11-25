import unittest
from unittest import IsolatedAsyncioTestCase

from chzzk import Chzzk, ChzzkChat
from chzzk.model import ChatContext

from dotenv import dotenv_values


class TestChzzkClient(IsolatedAsyncioTestCase):

    async def test_chzzk_client(self):
        config = dotenv_values(".env")
        auth_data = {"auth": config.get("AUTH"), "session": config.get("SESSION")}
        client = Chzzk.from_data(**auth_data)

        print(await client.me())

        search_channels = await client.search.channels(keyword="이춘향")

        for channel in search_channels.data:
            print(await client.channel(channel.channel.channel_id))

    async def test_chzzk_live(self):
        config = dotenv_values(".env")
        auth_data = {"auth": config.get("AUTH"), "session": config.get("SESSION")}
        chzzk = Chzzk.from_data(**auth_data)

        pong = "7ce8032370ac5121dcabce7bad375ced"
        live = await chzzk.live.status(pong)
        chat_id = live.chat_channel_id

        print(await chzzk._game_chat.access_token(chat_id))

        chat = ChzzkChat(chzzk=chzzk, chat_context=ChatContext(chat_channel_id=chat_id))
        await chat.connect()
        # await chat.run()
        # await chat.connect()

        print(chat)

    async def test_sum(self):
        server_id = sum(map(lambda x: ord(x), list("N1VvHk")))
        print(server_id)


if __name__ == '__main__':
    unittest.main()
