from datetime import datetime
import sqlite3
import csv


def add_user(id_telegram, joining_date):
	try:
		# подключение к бд
		con = sqlite3.connect('data.db')
		cur = con.cursor()

		# вставить данные пользователя
		sqlite_insert_with_param = """INSERT INTO 'users'
						  ('id_telegram', 'joiningDate')
						  VALUES (?, ?);"""

		cur.execute(sqlite_insert_with_param, (id_telegram, joining_date))
		con.commit()
		cur.close()
	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)
	
def get_users():
	try:
		# подключение к бд
		con = sqlite3.connect('data.db')
		cur = con.cursor()

		cur.execute("SELECT * from users")
		records = cur.fetchall()
		cur.close()

		return records
	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)


def set_language(id_telegram,language):
	try:
		sqlite_connection = sqlite3.connect('data.db')
		cursor = sqlite_connection.cursor()

		sql_update_query = """UPDATE users set language = ? where id_telegram = ?"""
		cursor.execute(sql_update_query,(language, id_telegram))
		sqlite_connection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)

def get_language(id_telegram):
	try:
		# подключение к бд
		con = sqlite3.connect('data.db')
		cur = con.cursor()

		info = cur.execute('SELECT * FROM users WHERE id_telegram=?', (id_telegram, ))
		records = info.fetchall()

		return records[0][2]

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)

def check_user(id_telegram):
	try:
		# подключение к бд
		con = sqlite3.connect('data.db')
		cur = con.cursor()

		try:
			cur.execute('''CREATE TABLE users (id_telegram INTEGER, joiningDate timestamp, language text)''')
		except:
			pass

		info = cur.execute('SELECT * FROM users WHERE id_telegram=?', (id_telegram, ))
		if info.fetchone() is None: 
			return False
		else:
			return True

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)
		

def add_message(id_telegram,message_text,send_date):
	try:
		# подключение к бд
		con = sqlite3.connect('data.db')
		cur = con.cursor()

		try:
			cur.execute('''CREATE TABLE messages (id_telegram INTEGER,message_text text, send_date timestamp)''')
		except:
			pass

		# вставить данные пользователя
		sqlite_insert_with_param = """INSERT INTO 'messages'
						  ('id_telegram', 'message_text', 'send_date')
						  VALUES (?, ?, ?);"""

		cur.execute(sqlite_insert_with_param, (id_telegram, message_text, send_date))
		con.commit()
		cur.close()
	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error)


def import_messages():
	try:
		con = sqlite3.connect('data.db')
		cur = con.cursor()
		
		try:
			cur.execute('''CREATE TABLE messages (id_telegram INTEGER,message_text text, send_date timestamp)''')
		except:
			pass

		cur.execute("SELECT * from messages ORDER BY id_telegram DESC")
		records = cur.fetchall()
		with open('messages.csv', mode='w', encoding='utf-8') as employee_file:
			employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			l = ['telegram ID', "текст сообшения",'дата и время']
			employee_writer.writerow(l)

		for row in records:
			with open('messages.csv', mode='a', encoding='utf-8') as employee_file:
				employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				l = [row[0], row[1],datetime.strptime(row[2][:-6],"%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d %H:%M:%S')]
				employee_writer.writerow(l)

		cur.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error) 



def import_messages_for_user(id_telegram):
	try:
		con = sqlite3.connect('data.db')
		cur = con.cursor()
		
		try:
			cur.execute('''CREATE TABLE messages (id_telegram INTEGER,message_text text, send_date timestamp)''')
		except:
			pass


		info = cur.execute('SELECT * FROM messages WHERE id_telegram=? ORDER BY send_date DESC', (id_telegram, ))
		records = info.fetchall()

		with open('messages.csv', mode='w', encoding='utf-8') as employee_file:
			employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			l = ['telegram ID', "текст сообшения",'дата и время']
			employee_writer.writerow(l)

		for row in records:
			with open('messages.csv', mode='a', encoding='utf-8') as employee_file:
				employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				l = [row[0], row[1],datetime.strptime(row[2][:-6],"%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d %H:%M:%S')]
				employee_writer.writerow(l)

		cur.close()

	except sqlite3.Error as error:
		print("Ошибка при работе с SQLite", error) 





