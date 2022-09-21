from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton, InputFile

start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text='Русский', callback_data="en")).add(InlineKeyboardButton(text="English", callback_data="ru"))
 
