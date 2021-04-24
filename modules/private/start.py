from aiogram.types import ChatType
from aiogram.types import BotCommand
from aiogram import types
from connector import dp, bot
import utils

@dp.message_handler(commands=['start'], ceu=True, chat_type=ChatType.PRIVATE)
async def start(message: types.Message):

	commands = [
		BotCommand(command="/start", description="Начало"),
		BotCommand(command="/help", description="Помощь"),
		BotCommand(command="/list", description="Список чатов"), 
		BotCommand(command="/stats", description="Узнать статистику человека в определённом чате"), 
		BotCommand(command="/addowner", description="Добавить пользователя в список администраторов чата"), 
		BotCommand(command="/removeowner", description="Убрать пользователя из списка администраторов чата"), 
		BotCommand(command="/list", description="Список чатов"), 
		BotCommand(command="/id", description="Узнать ID человека (в чате)"),  
		BotCommand(command="/bind", description="Подлючить чат к боту (в чате)"), 
		BotCommand(command="/unbind", description="Отключить чат от бота (в чате)"), 
	]

	await bot.set_my_commands(commands)
	return await message.answer("Что умеет этот бот?\n\nЭто бот для отслеживания автивности чатов и людей в них.\nИспользуйте /help для получения информации.")
