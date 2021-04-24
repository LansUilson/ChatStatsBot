from aiogram.utils.markdown import pre
from aiogram.types import ChatType
from connector import dp, data, bot
from aiogram import types
import utils

@dp.callback_query_handler(cch=["id"], chat_type=ChatType.PRIVATE)
async def send_data(query: types.CallbackQuery, chat_id):

	msg = f"Статистика чата \"{data[chat_id]['chat']['name']}\" ({pre(data[chat_id]['chat']['id'])}):\n\n  Сообщений: {data[chat_id]['chat']['msgs']}\n  Сообщений не подряд: {data[chat_id]['chat']['msgsnotr']}\n  Уровень: {data[chat_id]['chat']['level']}\n  Опыт: {data[chat_id]['chat']['exp']}/{data[chat_id]['chat']['needexp']}"

	keyboard_markup = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
	
	if(len(data[chat_id]['users']) > 5): t = "Топ 5"
	else: t = f"Топ {len(data[chat_id]['users'])}"

	keyboard_markup.add(
		types.KeyboardButton(f"{t} пользователей по сообщениям", callback_data=f"utm{chat_id}"),
		types.KeyboardButton(f"{t} пользователей по уровню", callback_data=f"utl{chat_id}"),
	)

	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=msg, parse_mode='Markdown', reply_markup=keyboard_markup)

@dp.callback_query_handler(cch=["top"], chat_type=ChatType.PRIVATE)
async def top(query: types.CallbackQuery, chat_id):

	users = data[chat_id]['users']
	msg = f"Топ 5 самых активных учатников чата \"{data[chat_id]['chat']['name']}\":\n\n"

	if((query.data)[2] == "l"):
		sort = sorted(users, key=lambda x : x['level'], reverse=True)
	
		n = 0
		for i in sort:
			n += 1
			if(n > 5):
				break
			msg += f"  {n}. [{await utils.getName(i['fname'], i['lname'])}](tg://user?id={i['id']}):\n    Уровень: {i['level']}\n    Опыт: {i['exp']}/{i['needexp']}\n    Сообщений не подряд: {i['msgsnotr']}\n\n"
			
	elif((query.data)[2] == "m"):
		sort = sorted(users, key=lambda x : x['msgs'], reverse=True)
	
		n = 0
		for i in sort:
			n += 1
			if(n > 5):
				break
			msg += f"  {n}. [{await utils.getName(i['fname'], i['lname'])}](tg://user?id={i['id']}):\n    Сообщений: {i['msgs']}\n    Сообщений не подряд: {i['msgsnotr']}\n    Уровень: {i['level']}\n\n"

	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=msg, parse_mode='Markdown')
	return True

@dp.message_handler(commands=['хуй'], ceu=True, chat_type=ChatType.PRIVATE) 
async def kb(message: types.Message):

	keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	keyboard_markup.add(
		types.KeyboardButton('Топ чатов', callback_data='chatsTop'),
	)
	keyboard_markup.add(
		types.KeyboardButton('Топ даунов', callback_data='chatsTop'),
	)

	await message.answer("Test", reply_markup=keyboard_markup)