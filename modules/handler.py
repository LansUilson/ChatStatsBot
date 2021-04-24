from aiogram.types import ChatType
from connector import dp, data, db
from aiogram import types
import math
import utils

# Обновление статистики левела, експы, сообщений и т.д #
@dp.message_handler(ceu=True, is_cmd=False, chat_type=ChatType.SUPERGROUP)
async def handler(message: types.Message):

	chatdata = data[message.chat.id]

	if(not await utils.checkExist(message.from_user.id, chatdata)): await db.new_chat_user(message.chat.id, message.from_user.id, message.from_user.first_name, message.from_user.last_name)

	user = await utils.getUser(chatdata['users'], message.from_user.id)
	usr = await utils.getUser(data['users'], message.from_user.id)

	chat = chatdata['chat']

	if(int(chat['last_sender']) != int(message.from_user.id)):

		chat['last_sender'] = message.from_user.id
		chat['msgs'] = chat['msgs']+1
		chat['msgsnotr'] = chat['msgsnotr']+1

		user['msgs'] = user['msgs']+1
		user['msgsnotr'] = user['msgsnotr']+1

		usr['msgs'] = usr['msgs']+1
		usr['msgsnotr'] = usr['msgsnotr']+1

		if(round(user['exp']) >= user['needexp']):
			user['level'] += 1
			user['exp'] = 0
			user['needexp'] = round((50*math.pow(1.1, user['level'])))
			await message.answer(f"Теперь у [{await utils.getName(message.from_user.first_name, message.from_user.last_name)}](tg://user?id={message.from_user.id}) {user['level']} уровень!", parse_mode='Markdown', disable_notification = True)
		else:
			user['exp'] += 0.5 
		
		if(round(usr['exp']) >= usr['needexp']):
			usr['level'] += 1
			usr['exp'] = 0
			usr['needexp'] = round((50*math.pow(1.1, usr['level']))) 
			await message.answer(f"Теперь у [{await utils.getName(message.from_user.first_name, message.from_user.last_name)}](tg://user?id={message.from_user.id}) {usr['level']} персональный уровень!", parse_mode='Markdown', disable_notification = True)
		else:
			usr['exp'] += 0.5 

		if(round(chat['exp']) >= chat['needexp']):
			chat['level'] += 1
			chat['exp'] = 0
			chat['needexp'] = round((182*math.pow(1.1, chat['level']))) 
			await message.answer(f"Ваш чат теперь {chat['level']} уровня!")
		else:
			chat['exp'] += 0.5

	else:
		user['msgs'] = user['msgs']+1

		usr['msgs'] = usr['msgs']+1

		chat['msgs'] = chat['msgs']+1
