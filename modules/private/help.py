from aiogram.types import ChatType
from aiogram import types
from connector import dp
import utils

@dp.message_handler(commands=['help'], ceu=True, chat_type=ChatType.PRIVATE)
async def help(message: types.Message):

	return await message.answer("Для использования бота нужно:\n  ●Пригласить бота в ВАШ чат (вы должны быть создателем)\n  ●Выдать ему права администратора (иначе бот не сможет читать все сообщения)\n  ●Написать /bind\n\nТем самым бот будет собирать статистику из чатов и вы сможете когда захотите посмотреть на активность пользователей.")
