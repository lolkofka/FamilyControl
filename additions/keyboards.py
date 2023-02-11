from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

async def startChildKeyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Включить/Выключить'))
    kb.add(KeyboardButton('Узнать время'))
    return kb

async def startParentKeyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Включить/Выключить'))
    kb.add(
        KeyboardButton('Узнать время'),
        KeyboardButton('Продлить время'),
        )
    return kb

async def setState(state): 
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(InlineKeyboardButton(
        'Включить' if not state else 'Выключить', 
        callback_data='setStateOn'if not state else 'setStateOff'))
    return kb