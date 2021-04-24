from aiogram.utils.markdown import pre
from aiogram.types import ChatType
from connector import dp, data
from aiogram import types
import utils

@dp.message_handler(regexp_commands=['addowner +((-?\d+) +(-?\d+))'], ceu=True, chat_type=ChatType.PRIVATE)
async def stats(message: types.Message, regexp_command):

	if(regexp_command.group(1)):
		chat = -int(str(regexp_command.group(2)).replace("-", "")) 

		if(not chat in (await utils.getUser(data['users'], message.from_user.id))['chats']):
			return await message.answer("Вы не являетесь владельцем этого чата.")

		if(await utils.existUserChat(chat, regexp_command.group(3))):
			user = await utils.getUser(data['users'], regexp_command.group(3))

			if(chat in user['chats']):
				return await message.answer("Этот пользователь уже может отслеживать статистику.")

			user['chats'].append(chat)

			return await message.answer(f"Пользователь [{await utils.getName(user['fname'], user['lname'])}](tg://user?id={user['id']}) теперь тоже может смотреть статистику чата \"{data[chat]['chat']['name']}\" ({pre(data[chat]['chat']['id'])}).", parse_mode='Markdown')
		else:
			return await message.answer("Этого пользователя нет в указанном чате.")
