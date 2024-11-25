import unittest
from unittest import IsolatedAsyncioTestCase

from chzzk.model import Message, Connect, DefaultMessage, PersonalData


class TestModel(IsolatedAsyncioTestCase):

    async def test_model(self):
        default = {"cid": 1, "svcid": "game", "ver": "2"}
        connect = Connect(acc_tkn="123", auth="READ", dev_type=2001, uid="123")
        # connect = {"accTkn": "123", "auth": "READ", "devType": 2001, "uid": "123"}
        body = {"bdy": {"accTkn": "123", "auth": "READ", "devType": 2001, "uid": "123"}, "cmd": 2001, "tid": 1}
        msg = Message[Connect](**default | {"cmd": 2001, "tid": 1}, **{"bdy": connect.model_dump(by_alias=True)})

        print(msg)

    async def test_model2(self):
        # connect = Connect()
        # connect.dev_type = 2001
        connect = Connect(acc_tkn="123", auth="READ", dev_type=2001, uid="123")
        msg = Message[Connect](bdy=connect, cid=1, svcid="game", ver="2", cmd=2001, tid=1)

        print(msg.model_dump_json(by_alias=True))


if __name__ == '__main__':
    unittest.main()
