import unittest
from unittest import IsolatedAsyncioTestCase

from dotenv import dotenv_values

from chzzk import Chzzk


class TestChzzkClient(IsolatedAsyncioTestCase):

    async def test_chzzk_client(self):
        config = dotenv_values(".env")
        auth_data = {"auth": config.get("AUTH"), "session": config.get("SESSION")}
        client = Chzzk.from_data(**auth_data)

        print(await client.me())

        search_channels = await client.search.channels(keyword="이춘향")

        for channel in search_channels.data:
            print(await client.channel(channel.channel.channel_id))

    async def test_sum(self):
        server_id = sum(map(lambda x: ord(x), list("N1VvHk")))
        print(server_id)


if __name__ == '__main__':
    unittest.main()
