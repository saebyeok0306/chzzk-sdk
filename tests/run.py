import asyncio
import logging

from chzzk import ChzzkChat, Chzzk
from chzzk.model import ChatMessage

from dotenv import dotenv_values


logging.basicConfig(level=logging.INFO)

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


@chat.commands(name="공지")
async def notice(message: ChatMessage, *args: tuple[str]):
    await chat.pin_message(message=message)


@chat.commands()
async def 공지해제(*args):
    await chat.unpin_message()


@chat.commands(name="덧셈")
async def plus(message: ChatMessage, *args):
    nums = list(map(lambda x: int(x), args))
    await chat.send_chat(f"덧셈 결과: {sum(nums)}")


@chat.event
async def on_error(message, *args, **kwargs):
    print(f"on_error: {message}")


async def main():
    channels = await chzzk.search.channels("갈대s")
    channel_id = channels[0].channel.channel_id
    await chat.run(channel_id=channel_id)

if __name__ == "__main__":
    asyncio.run(main())
