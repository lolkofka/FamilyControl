from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import additions.config as config
from additions.database import db
from additions.control import startControl
import additions.keyboards as keyboards
import additions.filters as ft
import additions.iot as iot

import asyncio, time, threading, os

bot = Bot(token = config.tgToken, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage = MemoryStorage())

users_db = db('userbase.json')
database = db('database.json')


pc = iot.device(authKey=config.authKey)
pc.get_device(config.deviceName)


@dp.message_handler(state='*', commands=['start'])
async def startCommand(message: types.Message):
    user = message.from_user
    users_db.set(user.id, {'userName':str(user.username)})
    with open('texts/start.txt', encoding='utf-8') as dataTxt:
        text = dataTxt.read()
    if user.id in config.parentsIds:
        await message.answer(
            text.format(userId = user.id), reply_markup= await keyboards.startParentKeyboard(),
            parse_mode='Markdown'
        )
    elif user.id in config.childs:
        await message.answer(
            text.format(userId = user.id), reply_markup= await keyboards.startChildKeyboard(),
            parse_mode='Markdown'
        )
    else:
        await message.answer(
            text.format(userId = user.id),
            parse_mode='Markdown'
        )


@dp.message_handler(ft.isParentOrChild(), filters.Text(startswith='Узнать время'), state='*')
async def seeTime(message: types.Message, state):
    user = message.from_user
    tm = database.get('workTime')
    if not tm:
        rm = config.timeToPlay
    else:
        rm = config.timeToPlay - tm
        if rm < 0: rm = 0
    remaining = time.strftime("%H:%M %Ssec", time.gmtime(rm))
    await bot.send_message(user.id, remaining)


@dp.message_handler(ft.isParentOrChild(), filters.Text(startswith='Продлить время'), state='*')
async def seeTime(message: types.Message, state):
    user = message.from_user
    tm = database.get('workTime')
    if not tm:
        rm = config.timeToPlay
    else:
        rm = config.timeToPlay - tm
        if rm < 0: rm = 0
    remaining = time.strftime("%H:%M %Ssec", time.gmtime(rm))
    await bot.send_message(user.id, remaining)


@dp.message_handler(ft.isParent(), filters.Text(startswith='Изменить время'), state='*')
async def changeTime(message):
    user = message.from_user

    tm = database.get('workTime')
    if not tm:
        rm = config.timeToPlay
    else:
        rm = config.timeToPlay - tm
        if rm < 0: rm = 0
    remaining = time.strftime("%H:%M %Ssec", time.gmtime(rm))

    if type(message) == types.Message:
        await message.answer(f'Оставшееся время: {remaining}, Изменить время',
            reply_markup = await keyboards.addTimeKeyboard())
    else:
        await message.message.edit_text(f'Оставшееся время: {remaining}, Изменить время',
            reply_markup = await keyboards.addTimeKeyboard())


@dp.callback_query_handler(ft.isParent(), filters.Text(startswith='time_'), state='*')
async def changeTimeComplete(callback: types.CallbackQuery):
    t, action, tm = callback.data.split('_')
    t = database.get('workTime')
    if action == 'add':
        t -= int(tm)*60
    else:
        t += int(tm)*60
    database.set('workTime', t)
    await callback.answer('Успешно!')
    await changeTime(callback)


@dp.message_handler(ft.isParentOrChild(), filters.Text(startswith='Включить/Выключить'), state='*')
async def onOffPc(message):
    user = message.from_user

    pcStatus = pc.get_status()
    strPcStatus = 'Включен' if pcStatus else 'Выключен'

    tm = database.get('workTime')
    if not tm:
        rm = config.timeToPlay
    else:
        rm = config.timeToPlay - tm
        if rm < 0: rm = 0
    remaining = time.strftime("%H:%M %Ssec", time.gmtime(rm))

    text = f'''
Текущее состояние компьютера: {strPcStatus}
Оставшееся время работы: {remaining}
'''
    if type(message) == types.Message:
        await bot.send_message(user.id, text, reply_markup=await keyboards.setState(pcStatus))
    else:
        await message.message.edit_text(text, reply_markup=await keyboards.setState(pcStatus))        


@dp.callback_query_handler(ft.isParentOrChild(), filters.Text(startswith='setState'), state='*')
async def setState(callback: types.CallbackQuery):
    pc.set_state(callback.data.split('_')[1] == 'On')
    time.sleep(1)
    await callback.answer('Успешно!')
    await onOffPc(callback)


# init
async def initialize(data):
    info = await data.bot.me
    print(f'ID: {info["id"]}')
    print(f'Username: {info["username"]}')
    t = threading.Thread(target=startControl)
    t.start()


# logging
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=initialize, skip_updates=True)