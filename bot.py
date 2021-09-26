import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import api_req

bot = Bot(token='вы')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в бота @VimeStats_bot! Список команд - /help')

@dp.message_handler(commands=['stats'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.stats(username=message.text[7:], user_id=message.from_user.id))

@dp.message_handler(commands=['friends'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.friends(username=message.text[9:], user_id=message.from_user.id))

@dp.message_handler(commands=['guild'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.guild(guild=message.text[7:], user_id=message.from_user.id))

@dp.message_handler(commands=['skin'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.skin(username=message.text[6:], user_id=message.from_user.id))

@dp.message_handler(commands=['cape'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.cape(username=message.text[6:], user_id=message.from_user.id))

@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вот список команд которые есть у бота:\n'
                                '/stats <id/username> - информация о игроке\n'
                                '/friends <id/username> - вывести список друзей игрока\n'
                                '/guild <id/name> - информация о гильдии\n'
                                '/skin <username> - получить скин игрока\n'
                                '/cape <username> - получить плащ игрока\n'
                                '/staff - получить список админов онлайн\n'
                                '/games - список игр доступных для просмотра топа\n'
                                '/top <game_id> - топ по определенной игре\n'
                           )


@dp.message_handler(commands=['staff'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.staff(user_id=message.from_user.id))

@dp.message_handler(commands=['games'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.games(user_id=message.from_user.id))

@dp.message_handler(commands=['top'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваш запрос принят в обработку, ожидайте')
    asyncio.create_task(api_req.top(game_id=message.text[5:], user_id=message.from_user.id))

@dp.message_handler()
async def any_message_answer(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Я не знаю что ответить, вот список доступных команд: \n'
                                '/stats <id/username> - информация о игроке\n'
                                '/friends <id/username> - вывести список друзей игрока\n'
                                '/guild <id/name> - информация о гильдии\n'
                                '/skin <username> - получить скин игрока\n'
                                '/cape <username> - получить плащ игрока\n'
                                '/staff - получить список админов онлайн\n'
                                '/games - список игр доступных для просмотра топа\n'
                                '/top <game_id> - топ по определенной игре\n')


if __name__ == '__main__':
    executor.start_polling(dp)
