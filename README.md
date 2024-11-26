# chzzk.py

네이버 라이브 스트리밍 서비스 치치직(CHZZK)의 비공식 API 라이브러리.<br/>
공부 목적으로 만들었으며, 참조한 레포는 하단의 `References`에 명시했습니다.

현재는 배포되지 않은 상태입니다.

# Requirements

- Python 3.11+

# Installation

# Example

```py
import asyncio

from chzzk import ChzzkChat, Chzzk
from chzzk.model import ChatMessage

from dotenv import dotenv_values


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
```

# References

- [jonghwanhyeon/python-chzzk](https://github.com/jonghwanhyeon/python-chzzk?tab=readme-ov-file)
- [kimcore/chzzk](https://github.com/kimcore/chzzk)
- [gunyu1019/chzzkpy](https://github.com/gunyu1019/chzzkpy)