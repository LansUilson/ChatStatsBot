from aiogram.types import ChatType
from connector import dp, db, bot
from aiogram import types
import utils

@dp.message_handler(commands=['list'], ceu=True, chat_type=ChatType.PRIVATE)
async def list(message: types.Message):

	names = await utils.getUserChats(message.from_user.id)

	if(len(names) == 0):
		return await message.answer("У вас нет подключённых чатов.")

	keyboard_markup = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	for i in names:
		keyboard_markup.add(
			types.KeyboardButton(i['name'], callback_data=-i['id']),
		)

	return await message.answer("Список Ваших чатов.\n\nДля того, чтобы увидеть статистику выберите чат:", reply_markup=keyboard_markup)
