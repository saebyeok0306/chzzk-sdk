import asyncio

from chzzk import ChzzkChat
from chzzk.model import ChatMessage

chat = ChzzkChat()
channel_id = "aed9d6557bebfb21ab3d081b862cdd2d"


@chat.event
async def on_connect():
    print("연결완료")


@chat.event
async def on_chat(message: ChatMessage):
    print(f"채팅: {message.content}")


async def main():
    await chat.run(channel_id=channel_id)

if __name__ == "__main__":
    asyncio.run(main())