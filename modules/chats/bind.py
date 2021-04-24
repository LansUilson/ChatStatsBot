from connector import dp, db, bot, data 
from aiogram.types import ChatType
from aiogram import types
import utils

@dp.message_handler(commands=['bind'], ceu=True, chat_type=ChatType.SUPERGROUP)
async def bind(message: types.Message):

	member = await bot.get_chat_member(message.chat.id, message.from_user.id)
	if(member.status == "creator"):
		user = await utils.getUser(data['users'], message.from_user.id) 

		if(not (message.chat.id in user['chats'])):

			if(not await db.exist_chat(message.chat.id)):
				await db.new_chat(message.chat.id)

				if(len(user['chats']) > 25):
					return await message.answer("Количество привязанных чатов не должно превышать 25.")
				else:
					user['chats'].append(message.chat.id) 

				await db.new_chat_user(message.chat.id, message.chat.id, message.chat.title, None, 200)
				await db.new_chat_user(message.chat.id, message.from_user.id, message.from_user.first_name, message.from_user.last_name)
			else:
				if(len(user['chats']) > 25):
					return await message.answer("Количество привязанных чатов не должно превышать 25.")
				else:
					user['chats'].append(message.chat.id)

			return await message.answer(f"Чат успешно привязан к [{await utils.getName(message.from_user.first_name, message.from_user.last_name)}](tg://user?id={message.from_user.id})!\n\nТеперь вы можете отслеживать общую статистику, статистику отдельных людей прямо из чатов и из личных сообщений с ботом.", parse_mode='Markdown', disable_notification = True) 

		else:
			return await message.answer(f"Чат уже привязан!") 

	else:
		return await message.answer("Статистику может отслеживать только создатель.\nЕсли Вы тоже хотите отслеживать статистику попросите создателя добавить Вас в лист отслеживания.\nЕсли у вас стоит анонимность, то её следует убрать для корректной работы бота.")
