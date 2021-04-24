from aiogram.dispatcher.filters import BoundFilter
from connector import dp, db, bot, data
from aiogram import types

# Ниже приведены фильтры, созданные модулем aiogram. #

class IsCommand(BoundFilter):
	"""
	Фильтр для проверки сообщения на команду. 
	Проверяет наличие префикса чата в сообщении.
	is_cmd - ключ фильтра.
	"""

	key = 'is_cmd'

	def __init__(self, is_cmd):
		self.is_cmd = is_cmd

	async def check(self, message: types.Message):

		if(not message.text.startswith("/")):
			return True
		return False

class CheckCorrectUser(BoundFilter):

	"""
	Этот фильтр проверяет корректность пользоватеья в базе данных.
	Если пользователя нет, он создаётся.
	ceu - ключ фильтра.
	"""

	key = 'ceu'

	def __init__(self, ceu):
		self.ceu = ceu

	async def check(self, message: types.Message):

		if(not await checkExistUsers(message.from_user.id)):
			await db.new_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name) 
			return True
		return True

class CallbackChatHandler(BoundFilter):

	"""
	Этот фильтр проверяет корректность отправленного callback'a.'
	Если у польщователя нет чата, с которым отпрален callback, то ничего не происходит..
	cch - ключ фильтра.
	"""

	key = 'cch'

	def __init__(self, cch):
		self.cch = cch

	async def check(self, message: types.Message):

		try: message.data = int(message.data) 
		except: pass

		user = await getUser(data['users'], message['from'].id) 

		if(type(message.data) is str):
			if(int((message.data)[3:]) in user['chats']):
				if(self.cch[0] == "top"): return { "chat_id": int((message.data)[3:]) }
				else: return False
			else: return False
			return False

		if(int(message.data) in user['chats']): 
			if(self.cch[0] == "id"): return { "chat_id": int(message.data) }
			else: return False
		else: 
			return False
		return False

dp.filters_factory.bind(IsCommand)
dp.filters_factory.bind(CheckCorrectUser) 
dp.filters_factory.bind(CallbackChatHandler)

"""
Ниже переведены вспомогательные функции
"""

async def getName(fname, lname):
	"""
	Проверяет пользователя на фамилию
	И возвращает никнейм с именем или с именем и фамилией. 
	"""

	if(str(lname) == "None"): 
		return f"{fname}"

	elif(str(lname) != "None"): 
		return f"{fname} {lname}"

async def existUserChat(chat_id, id):
	''' Проверка на существование пользователя в чате '''

	for i in data[chat_id]['users']:
		if(str(i['id']) == str(id)):
			return True
	return False

async def getUser(data, id, number=False):

	def show_indices(obj, indices):
	    for k, v in obj.items() if isinstance(obj, dict) else enumerate(obj):
	        if isinstance(v, (dict, list)):
	            yield from show_indices(v, indices + [k])
	        else:
	            yield indices + [k], v
	
	for keys, v in show_indices(data, [] ):
	   if(str(v) == str(id)):
	    	if(number):
	    		return keys[0]
	    	return data[keys[0]]

async def checkExist(user_id, chatdata):
	''' Проверка на существование пользователя '''
	for i in chatdata['users']:
		if(int(i['id']) == int(user_id)):
			return True
	return False

async def checkExistUsers(user_id):
	''' Проверка на существование пользователя '''
	for i in data['users']:
		if(int(i['id']) == int(user_id)):
			return True
	return False

async def getUserChats(id):
	user = await getUser(data['users'], id)
	chats = user['chats']

	names = []
	for i in chats:
		names.append({ 
			"name": data[i]['chat']['name'], 
			"id": data[i]['chat']['id']
		})

	return names