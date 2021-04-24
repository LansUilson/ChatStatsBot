from aiogram.types import ChatType
from connector import dp, bot, data
from aiogram import types
import utils

@dp.message_handler(commands=['unbind'], ceu=True, chat_type=ChatType.SUPERGROUP)
async def unbind(message: types.Message):

	member = await bot.get_chat_member(message.chat.id, message.from_user.id)
	if(member.status == "creator"):

		user = await utils.getUser(data['users'], message.from_user.id)  

		if(message.chat.id in user['chats']):
			user['chats'].remove(message.chat.id) 
			return await message.answer(f"Чат успешно отвязан!") 
		else:
			return await message.answer(f"Этот чат не привязан ни к кому.") 

	else:
		return await message.answer("Отвязать чат может только тот, кто привязан к этому чату.\nЕсли у вас стоит анонимность, то её следует убрать для корректной работы бота.")
