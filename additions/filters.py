from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message

import additions.config as config


class isParent(BoundFilter):
    async def check(self, msg: Message):
        user = msg.from_user
        if user.id in config.parentsIds:
            return True
        else:
            return False

class isChild(BoundFilter):
    async def check(self, msg: Message):
        user = msg.from_user
        if user.id in config.childs:
            return True
        else:
            return False

class isParentOrChild(BoundFilter):
    async def check(self, msg: Message):
        user = msg.from_user
        if user.id in config.parentsIds or user.id in config.childs:
            return True
        else:
            return False