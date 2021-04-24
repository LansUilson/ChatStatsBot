from aiogram.utils.markdown import pre
from aiogram.types import ChatType
from aiogram import types
from connector import dp
import utils

@dp.message_handler(commands=['id'], chat_type=ChatType.SUPERGROUP)
async def id(message: types.Message): 

	if("reply_to_message" in str(message)):
		id = message.reply_to_message['from']

		if(id.last_name == None):
			name = message.reply_to_message['from']['first_name']
		else:
			name = f"{message.reply_to_message['from']['first_name']} {message.reply_to_message['from']['last_name']}"
	else:
		id = message.from_user
		name = await utils.getName(message.from_user.first_name, message.from_user.last_name)

	return await message.answer(f"ID пользователя [{name}](tg://user?id={id.id}): {pre(id.id)} (нажмите чтобы скопировать).", parse_mode='Markdown')