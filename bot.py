from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import aioschedule
import csv
import asyncio
import pytz
from datetime import datetime

import config, db, utils, keyboards
from datetime import date
import time

bot = Bot(token=config.TOKEN)
bot2 = Bot(token=config.TOKEN2)
dp = Dispatcher(bot)
dp2 = Dispatcher(bot2)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	if(not db.check_user(message.from_user.id)):
		db.add_user(message.from_user.id, datetime.now(pytz.timezone('Europe/Moscow')))

	await bot.send_message(message.from_user.id, f"{utils.zn[1][0]} / {utils.zn[1][1]}", reply_markup=keyboards.start_kb)



@dp.message_handler()
async def text_mes(msg: types.Message):
	if(msg.text == 'Русский'):
		db.set_language(msg.from_user.id,'Русский')
		await bot.send_message(msg.from_user.id, utils.zn[1][2], reply_markup=types.ReplyKeyboardRemove())

		photo = open('img.jpg', 'rb')
		await bot.send_photo(msg.from_user.id,photo, caption = utils.zn[1][4])

		db.update_question(msg.from_user.id)

	elif(msg.text == 'English'):
		db.set_language(msg.from_user.id,'English')
		await bot.send_message(msg.from_user.id, utils.zn[1][3], reply_markup=types.ReplyKeyboardRemove())

		photo = open('img.jpg', 'rb')
		await bot.send_photo(msg.from_user.id,photo, caption = utils.zn[1][5])

		db.update_question(msg.from_user.id)
		

	elif(msg.text.lower() == 'таблица'):
		if(msg.from_user.id in config.ADMINS):
			if(msg.reply_to_message):
				user = int(msg.reply_to_message.text.split(':')[0])
				db.import_messages_for_user(user)
				await bot2.send_document(msg.from_user.id, open("messages.csv", "rb"), reply_markup=types.ReplyKeyboardRemove())
			else:
				db.import_messages()
				await bot2.send_document(msg.from_user.id, open("messages.csv", "rb"), reply_markup=types.ReplyKeyboardRemove())

	elif msg.reply_to_message and msg.from_user.id in config.ADMINS:
		user = msg.reply_to_message.text.split(':')[0]
		await bot.send_message(user, msg.text)

	else:
		if(db.get_language(msg.from_user.id)=='Русский'):
			await bot.send_message(msg.from_user.id, f'Спасибо, что делишься со мной 💓')
		else:
			await bot.send_message(msg.from_user.id, f'Thanks for sharing with me 💓')

		for i in config.ADMINS:
			await bot2.send_message(i, f'{msg.from_user.id}:{msg.text}')

		db.add_message(msg.from_user.id,msg.text,datetime.now(pytz.timezone('Europe/Moscow')))
		


@dp.message_handler(content_types=['document'])
async def load_file(message: types.Message):
	if(message.from_user.id in config.ADMINS):
		await message.document.download(destination_file='conf.csv') # это его скачивание
		utils.update_conf()
		utils.update_time()
		await message.answer('Обновленно')


@dp.message_handler()
async def choose_your_dinner():
	if(utils.get_time() in utils.times_send):
		for row in db.get_users():
			try:
				time.sleep(10)
				d1 = datetime.strptime(row[1][:-6],"%Y-%m-%d %H:%M:%S.%f")
				d2 = datetime.now()
				if((d2-d1).days<3):
					if(row[2]=='Русский'):
						await bot.send_message(row[0], utils.zn[1][4])
					elif(row[2]=='English'):
						await bot.send_message(row[0], utils.zn[1][5])
				else:
					if(row[2]=='Русский'):
						await bot.send_message(row[0], utils.zn[1][6])
					elif(row[2]=='English'):
						await bot.send_message(row[0], utils.zn[1][7])
			except Exception as e:
				print(e)
		sleep(60)
async def scheduler():
	aioschedule.every(60).seconds.do(choose_your_dinner)
	while True:
		await aioschedule.run_pending()
		await asyncio.sleep(60)
		

async def on_startup(dp): 
	asyncio.create_task(scheduler())


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
