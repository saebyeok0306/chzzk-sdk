import asyncio
import logging
from datetime import datetime
from typing import Self, Optional, Literal

from chzzk import Chzzk
from chzzk.client import ChatClient
from chzzk.event import EventManager
from chzzk.exception import ChzzkError, ReconnectWebsocket
from chzzk.model import ChatContext

_log = logging.getLogger(__name__)


class ChzzkChat(EventManager):
    def __init__(self, chzzk: Optional[Chzzk] = None, loop: asyncio.AbstractEventLoop = None):
        super().__init__(loop=loop)
        self._chzzk = chzzk
        if self._chzzk is None:
            self._chzzk = Chzzk()
        self._chat_client: Optional[ChatClient] = None
        self._context: Optional[ChatContext] = ChatContext()
        self.is_closed = False
        self.is_reconnected = True
        self._live_state: Optional[Literal["OPEN", "CLOSE"]] = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await super().close()

        async def _close():
            if self._chat_client and self._chat_client.is_connect:
                await self._chat_client.close()

        await asyncio.create_task(_close())

    async def run(self, channel_id: str, reconnect: bool = True):
        assert self._chat_client is None, "Already connected."
        self._context.channel_id = channel_id
        self.is_reconnected = reconnect

        if self._context.chat_channel_id is None and self._context.channel_id is not None:
            live = await self._chzzk.live.status(self._context.channel_id)
            if live is None:
                raise ChzzkError(msg="Connection to the server failed with CHZZK.")
            self._context.chat_channel_id = live.chat_channel_id

        if self._context.chat_channel_id and self._context.access_token is None:
            if self._chzzk.has_credentials():
                user = await self._chzzk.me()
                self._context.uid = user.user_id_hash

            token = await self._chzzk._game_chat.access_token(self._context.chat_channel_id)
            self._context.access_token = token.access_token

        await self.polling()

    async def _check_live(self):
        live_status = await self._chzzk.live.status(channel_id=self._context.channel_id)
        if live_status is None:
            return

        if self._live_state != live_status.status:
            self._live_state = live_status.status
            if self._live_state == "OPEN":
                self.dispatch("broadcast_open")
            elif self._live_state == "CLOSE":
                self.dispatch("broadcast_close")

        if live_status.chat_channel_id == self._context.chat_channel_id:
            return

        print("A chat_channel_id has been updated. Reconnect websocket.")
        await self._chat_client.close()

        self._context.chat_channel_id = live_status.chat_channel_id
        raise ReconnectWebsocket()

    async def polling(self) -> None:
        while not self.is_closed:
            try:
                self._chat_client = ChatClient(context=self._context, parsers=self._parser.parsers)
                await self._chat_client.connect()

                last_check_time = datetime.now()

                while True:
                    await self._chat_client.poll_event()
                    await asyncio.sleep(0)
                    _log.info(msg=".")
                    relative_time = datetime.now() - last_check_time
                    if relative_time.total_seconds() >= 59:
                        last_check_time = datetime.now()
                        _log.info(msg=f"check live status...")
                        await self._chzzk.live.status(self._context.channel_id)

            except ReconnectWebsocket:
                self.dispatch("disconnect")
                if self.is_reconnected is False:
                    break
                continue

