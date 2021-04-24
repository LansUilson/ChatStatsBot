from aiogram.utils.markdown import pre
from aiogram.types import ChatType
from connector import dp, data
from aiogram import types
import utils

@dp.message_handler(regexp_commands=['stats(?: +((-?\d+) +(-?\d+))|)'], ceu=True, chat_type=ChatType.PRIVATE)
async def stats(message: types.Message, regexp_command):

	if(regexp_command.group(1)):
		chat = -int(str(regexp_command.group(2)).replace("-", "")) 

		if(not chat in (await utils.getUser(data['users'], message.from_user.id))['chats']):
			return await message.answer("Вы не являетесь владельцем этого чата.")

		if(await utils.existUserChat(chat, regexp_command.group(3))):
			user = await utils.getUser(data[chat]['users'], regexp_command.group(3))

			return await message.answer(f"Статистика [{await utils.getName(user['fname'], user['lname'])}](tg://user?id={user['id']}) в чате \"{data[chat]['chat']['name']}\" ({pre(data[chat]['chat']['id'])}):\n\n    Сообщений: {user['msgs']}\n    Сообщений не подряд: {user['msgsnotr']}\n    Уровень: {user['level']}\n    Опыт: {user['exp']}/{user['needexp']}", parse_mode='Markdown')
		else:
			return await message.answer("Этого пользователя нет в указанном чате.")
	else:
		user = await utils.getUser(data['users'], message.from_user.id)

		return await message.answer(f"Ваша личная статистика:\n\n    Сообщений: {user['msgs']}\n    Сообщений не подряд: {user['msgsnotr']}\n    Уровень: {user['level']}\n    Опыт: {user['exp']}/{user['needexp']}", parse_mode='Markdown')
