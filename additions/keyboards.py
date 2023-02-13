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
        KeyboardButton('Изменить время'),
        )
    return kb

async def addTimeKeyboard():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(
        InlineKeyboardButton('Продлить на 15м', callback_data='time_add_15'),
        InlineKeyboardButton('Продлить на 30м', callback_data='time_add_30'),
        InlineKeyboardButton('Продлить на 60м', callback_data='time_add_60'),
        )
    kb.add(
        InlineKeyboardButton('Сократить на 15м', callback_data='time_del_15'),
        InlineKeyboardButton('Сократить на 30м', callback_data='time_del_30'),
        InlineKeyboardButton('Сократить на 60м', callback_data='time_del_60'),
        )
    return kb

async def setState(state): 
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(InlineKeyboardButton(
        'Включить' if not state else 'Выключить', 
        callback_data='setState_On'if not state else 'setState_Off'))
    return kb