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

bot = Bot(token=config.TOKEN)
bot2 = Bot(token=config.TOKEN2)
dp2 = Dispatcher(bot2)


@dp2.message_handler()
async def text_mes(msg: types.Message):
	if(msg.text.lower() == 'таблица'):
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
		

@dp2.message_handler(content_types=['document'])
async def load_file(message: types.Message):
	if(message.from_user.id in config.ADMINS):
		await message.document.download(destination_file='conf.csv') # это его скачивание
		utils.update_conf()
		utils.update_time()
		await message.answer('Обновленно') 

if __name__ == '__main__':
	executor.start_polling(dp2) 
