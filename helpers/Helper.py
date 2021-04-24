from config import PATHDB, db_update_time
from connector import logging
import threading
import sqlite3
import ast

class Helper:
	# Подключение к БД #
	def __init__(self):
		self.con = sqlite3.connect(PATHDB, check_same_thread = False) 
		self.cur = self.con.cursor() 

		global data

		tables = self.cur.execute("SELECT name FROM sqlite_master WHERE name LIKE 'c%' AND type='table';").fetchall()

		data = { 'users': [] }
		for i in tables:
			ais = self.cur.execute(f"SELECT * FROM {i[0]}").fetchall()

			data.update({
				int(ais[0][0]): {
					"chat": {}, 
					"users": []
				}
			})

			for u in ais:
				if("-" in u[0]):
					data[int(ais[0][0])]['chat'].update({
						"id": int(u[0])*-1, 
						"name": u[1], 
						"msgs": u[3], 
						"msgsnotr": u[4] , 
						"exp": u[5], 
						"needexp": u[6], 
						"level": u[7],
						"last_sender": u[8]
					})
				else: 
					data[int(ais[0][0])]['users'].append({
						"id": u[0], 
						"fname": u[1], 
						"lname": u[2], 
						"msgs": u[3], 
						"msgsnotr": u[4], 
						"exp": u[5], 
						"needexp": u[6], 
						"level": u[7]
					})
		
		users = self.cur.execute("SELECT * FROM users;").fetchall()

		for i in users:
			data['users'].append({
				"id": i[0], 
				"fname": i[1], 
				"lname": i[2], 
				"chats": ast.literal_eval(i[3]), 
				"exp": i[4], 
				"needexp": i[5], 
				"level": i[6], 
				"msgs": i[7], 
				"msgsnotr": i[8]
			})

		Helper.updateDB(self)

	async def new_user(self, id, fname, lname):

		self.cur.execute(f"INSERT OR IGNORE INTO users (ID, fname, lname) VALUES ({id}, '{fname}', '{lname}');")

		data['users'].append({
			"id": id, 
			"fname": fname, 
			"lname": lname, 
			"chats": [], 
			"exp": 0.0, 
			"needexp": 55, 
			"level": 1, 
			"msgs": 0, 
			"msgsnotr": 0
		})

		return self.con.commit()

	async def unbind_chat_user(self, chat_id, id):

		chat_id = int(chat_id)*-1

		chats = self.cur.execute(f"SELECT chats FROM users WHERE id={id};").fetchall()
		chats = ast.literal_eval(chats[0][0])
		chats.remove(-chat_id)

		self.cur.execute(f"UPDATE users SET chats = '{chats}' WHERE id={id};")
		return self.con.commit()

	async def exist_bind_chat(self, chat_id, id):

		chat_id = int(chat_id)*-1

		chats = self.cur.execute(f"SELECT chats FROM users WHERE id={id};").fetchall()
		chats = ast.literal_eval(chats[0][0])

		if(chat_id in chats):
			return True
		else:
			return False

	async def exist_user(self, id):

		exist = self.cur.execute(f"SELECT * FROM users WHERE id={id};").fetchall()
		return bool(len(exist))


	async def get_user_chats(self, id):

		chats = self.cur.execute(f"SELECT chats FROM users WHERE id={id};").fetchall()
		chats = ast.literal_eval(chats[0][0])

		names = []
		for i in chats:
			names += self.cur.execute(f"SELECT fname, id FROM c{i} LIMIT 1;").fetchall()

		return names

	async def update_all(self, chat, user):

		chat_id = int(chat['id'])*-1
		user_id = int(user['id'])

		chats = self.con.executescript(f"""UPDATE c{chat_id} SET msgs = {chat['msgs']}, msgsnotr = {chat['msgsnotr']}, exp = {chat['exp']}, needexp = {chat['needexp']}, level = {chat['level']}, lastsender = {chat['last_sender']} WHERE id = {chat['id']};
																	UPDATE c{chat_id} SET msgs = {user['msgs']}, msgsnotr = {user['msgsnotr']}, exp = {user['exp']}, needexp = {user['needexp']}, level = {user['level']} WHERE id = {user['id']}""")

		return self.con.commit() 


	async def new_chat(self, id):

		id = int(id)*-1

		self.cur.execute(f"CREATE TABLE IF NOT EXISTS c{id}(id TEXT NOT NULL PRIMARY KEY, fname TEXT, lname TEXT, msgs INTEGER DEFAULT 0, msgsnotr INTEGER DEFAULT 0, exp REAL DEFAULT 0.0, needexp INTEGER DEFAULT 55, level INTEGER DEFAULT 1, lastsender INTEGER DEFAULT 0);")
		
		data.update({
			-id: {
				"chat": {}, 
				"users": []
			}
		})

		return self.con.commit()

	async def new_chat_user(self, chat_id, id, fname, lname, needexp=55):

		chat_id = int(chat_id)*-1

		self.cur.execute(f"INSERT OR IGNORE INTO c{chat_id} (id, fname, lname, needexp) VALUES ({id}, '{fname}', '{lname}', {needexp});")

		if("-" in str(id)):
			data[-chat_id]['chat'].update({
				"id": chat_id, 
				"name": fname, 
				"msgs": 0, 
				"msgsnotr": 0, 
				"exp": 0.0, 
				"needexp": 200, 
				"level": 1,
				"last_sender": 0
			})
		else:
			data[-chat_id]['users'].append({
				"id": id, 
				"fname": fname, 
				"lname": lname, 
				"msgs": 0,
				"msgsnotr": 0, 
				"exp": 0.0, 
				"needexp": needexp, 
				"level": 1
			})

		return self.con.commit()  
	
	async def exist_user_chat(self, id):

		id = int(id)*-1

		exist = self.cur.execute(f"SELECT count(*) FROM sqlite_master WHERE name='c{id}';").fetchall()
		return bool(exist[0][0]) 

	async def exist_chat(self, id):

		id = int(id)*-1

		exist = self.cur.execute(f"SELECT count(*) FROM sqlite_master WHERE name='c{id}';").fetchall()
		return bool(exist[0][0])

	async def get_chat(self, id):

		id = int(id)*-1

		chat = self.cur.execute(f"SELECT * FROM c{id};").fetchall()
		return chat
	
	# Обновление БД через n время #
	def updateDB(self):
		logging.info("DATABASE UPDATED")
		threading.Timer(db_update_time, Helper.updateDB, args=[self]).start()

		query = ''
		for i in data:
			if("-" in str(i)):
				for u in data[i]['users']:
					query += f"""
					UPDATE c{data[i]['chat']['id']}
					SET
						id = {u['id']}, 
						fname = '{u['fname']}',
						lname = '{u['lname']}', 
						msgs = {u['msgs']}, 
						msgsnotr = {u['msgsnotr']}, 
						exp = {u['exp']},
						needexp = {u['needexp']}, 
						level = {u['level']}
					WHERE 
						id = {u['id']};"""
	
				query += f"""
				UPDATE c{data[i]['chat']['id']}
				SET 
					lastsender = {data[i]['chat']['last_sender']}, 
					level = {data[i]['chat']['level']}, 
					exp = {data[i]['chat']['exp']}, 
					needexp = {data[i]['chat']['needexp']}, 
					fname = '{data[i]['chat']['name']}', 
					msgs = {data[i]['chat']['msgs']}, 
					msgsnotr = {data[i]['chat']['msgsnotr']}
				WHERE
					id = {-data[i]['chat']['id']};"""
			else:
				for e in data['users']:
					query += f"""
					UPDATE users
					SET
						level = {e['level']}, 
						exp = {e['exp']}, 
						needexp = {e['needexp']}, 
						fname = '{e['fname']}', 
						lname = '{e['lname']}', 
						msgs = {e['msgs']}, 
						msgsnotr = {e['msgsnotr']}, 
						chats = '{e['chats']}' 
					WHERE
						id = {e['id']};"""

		if(len(query) == 0):
			return False

		self.con.executescript(query)
		return self.con.commit() 

	async def close(self):
		self.connection.close()
		return True
