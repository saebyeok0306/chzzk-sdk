import functools
import inspect
from typing import Callable, Any

from chzzk.model import ChatCmd, get_enum, ChatType, DonationMessage, SystemMessage, ChatMessage, SubscriptionMessage, \
    RecentChat, NoticeMessage, Blind, MissionDonation


class EventParser:
    def __init__(
            self,
            dispatch: Callable[..., Any],
            handler: dict[ChatCmd | int, Callable[..., Any]]
    ):
        self.dispatch: Callable[..., Any] = dispatch
        self.handler: dict[ChatCmd | int, Callable[..., Any]] = handler
        self.parsers: dict[ChatCmd, Callable[..., Any]] = dict()

        for _, func in inspect.getmembers(self):
            if hasattr(func, "__chzzk_event__"):
                # __chzzk_event__ : ChatCmd
                self.parsers[func.__chzzk_event__] = func

    @staticmethod
    def register(cmd: ChatCmd):
        def decorator(func: Callable[..., Any]):
            func.__chzzk_event__ = cmd
            return func
        return decorator

    @staticmethod
    def catch_exception(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.dispatch("client_error", e, *args, **kwargs)

        return wrapper

    def call_handler(self, key: ChatCmd, *args: Any, **kwargs: Any):
        if key in self.handler:
            func = self.handler[key]
            func(*args, **kwargs)

    @register(ChatCmd.CONNECTED)
    @catch_exception
    def call_connect(self, _: dict[str, Any]):
        self.call_handler(ChatCmd.CONNECTED)
        self.dispatch("connect")

    def _parse_chat(self, data: list[dict[str, Any]]):
        if data is None or len(data) == 0:
            return

        for message in data:
            # bdy
            message_raw_type: int = message.get("messageTypeCode") or message.get("msgTypeCode")
            message_type = get_enum(ChatType, message_raw_type)

            if message.get("profile") == "{}":
                message["profile"] = None

            match message_type:
                case ChatType.DONATION:
                    validated_data = DonationMessage(**message)
                    self.dispatch("donation", validated_data)

                case ChatType.SYSTEM_MESSAGE:
                    validated_data = SystemMessage(**message)
                    self.dispatch("system_message", validated_data)

                case ChatType.TEXT:
                    validated_data = ChatMessage(**message)
                    self.dispatch("chat", validated_data)

                case ChatType.SUBSCRIPTION:
                    validated_data = SubscriptionMessage(**message)
                    self.dispatch("subscription", validated_data)

    @register(ChatCmd.CHAT)
    @catch_exception
    def parse_chat(self, data: list[dict[str, Any]]):
        self._parse_chat(data)

    @register(ChatCmd.RECENT_CHAT)
    @catch_exception
    def parse_recent_chat(self, data: dict[str, Any]):
        validated_data = RecentChat(**data)
        self.dispatch("recent_chat", validated_data)

    @register(ChatCmd.DONATION)
    @catch_exception
    def parse_donation_chat(self, data: list[dict[str, Any]]):
        self._parse_chat(data)

    @register(ChatCmd.NOTICE)
    @catch_exception
    def parse_notice(self, data: dict[str, Any]):
        if len(data) == 0:
            self.dispatch("unpin")
            return

        validated_data = NoticeMessage(**data)
        self.dispatch("notice", validated_data)
        self.dispatch("pin", validated_data)

    @register(ChatCmd.BLIND)
    @catch_exception
    def parse_blind(self, data: dict[str, Any]):
        validated_data = Blind(**data)
        self.dispatch("blind", validated_data)

    @register(ChatCmd.EVENT)
    @catch_exception
    def parse_event(self, data: dict[str, Any]):
        event_type = data.get("type")

        if event_type == "DONATION_MISSION_IN_PROGRESS":
            validated_data = MissionDonation(**data)

            match validated_data.status:
                case "PENDING":
                    self.dispatch("mission_pending", validated_data)
                case "APPROVED":
                    self.dispatch("mission_approved", validated_data)
                case "REJECTED":
                    self.dispatch("mission_rejected", validated_data)
                case "COMPLETED":
                    self.dispatch("mission_completed", validated_data)