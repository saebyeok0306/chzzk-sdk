import asyncio
import logging

from chzzk import ChzzkChat, Chzzk
from chzzk.model import ChatMessage

from dotenv import dotenv_values


logging.basicConfig(level=logging.DEBUG)

env = dotenv_values(".env")
chzzk = Chzzk().from_data(auth=env.get("AUTH"), session=env.get("SESSION"))
chat = ChzzkChat(chzzk=chzzk)


@chat.event
async def on_connect():
    print(f"on_connect")
    await chat.send_chat("on_connect test")


@chat.event
async def on_chat(message: ChatMessage):
    print(f"on_chat: {message.content}")


async def main():
    channels = await chzzk.search.channels("갈대s")
    channel_id = channels[0].channel.channel_id
    await chat.run(channel_id=channel_id)

if __name__ == "__main__":
    asyncio.run(main())
