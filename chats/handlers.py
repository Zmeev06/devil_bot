import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, chat
from aiogram.utils.exceptions import MessageNotModified
import aiogram.utils.markdown as fmt
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, CommandStart
from aiomysql import connection
from telethon import TelegramClient
from datetime import datetime
import pytz

from telethon.sync import TelegramClient
from telethon import connection
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from tgbot.database import connect, close_connection
from load_all import bot

from .dbworker import add_chat, add_member, new_chat_users_list


client= TelegramClient('my_account', '5844266', '4974fa0b2d33d85d1368bb8e9e8ddabe')
client.start()



async def getter_id(chat_id):
	users_id = []
	users= await client.get_participants(chat_id)
	for user in users:
		if user.id is not None:
			users_id.append(user.id)
	return users_id

async def new_chat_member(message: types.Message):
	print(message)
	connection = await connect()
	user_id = message.from_user.id
	full_name = message.from_user.full_name
	username = message.from_user.username
	chat_id = message.chat.id
	chat_name = message.chat.title
	user_id_add_list=message.new_chat_members

	user_full_name_add_list = message.new_chat_members[0].full_name
	username_add_list = message.new_chat_members[0].username 
	message_date=datetime.utcnow()
	utcmoment = message_date.replace(tzinfo=pytz.utc)
	tz = 'Europe/Moscow'
	localDatetime = utcmoment.astimezone(pytz.timezone(tz))
	format_date = '%Y-%m-%d %H:%M:%S'
	user_date=localDatetime.strftime(format_date)

	await add_member(connection, user_id, username, full_name, chat_id, user_id_add, user_full_name_add, username_add, user_date)
	await add_chat(connection, chat_id, chat_name)

	users_id = await getter_id(chat_id)
	message_date=datetime.utcnow()
	utcmoment = message_date.replace(tzinfo=pytz.utc)
	tz = 'Europe/Moscow'
	localDatetime = utcmoment.astimezone(pytz.timezone(tz))
	format_date = '%Y-%m-%d %H:%M:%S'
	user_date=localDatetime.strftime(format_date)
	for user_id in users_id:
		users=await bot.get_chat_member(chat_id, user_id)
		username=users.user['username']
		user_fullname=users.user['full_name']
		await new_chat_users_list(connection, user_id, chat_id, username, user_fullname, user_date)
	print('hui')
	await close_connection(connection)
	types.ContentTypes

async def get_users_on_chat(message: types.Message):
	bot_id=int(message.new_chat_members[0].id)
	print(bot_id)
	if bot_id == message.bot.id:
		chat_id=message.chat.id
		print(chat_id)
		users_id=await getter_id(chat_id)
		print(users_id)
		message_date=datetime.utcnow()
		utcmoment = message_date.replace(tzinfo=pytz.utc)
		tz = 'Europe/Moscow'
		localDatetime = utcmoment.astimezone(pytz.timezone(tz))
		format_date = '%Y-%m-%d %H:%M:%S'
		user_date=localDatetime.strftime(format_date)
		for user_id in users_id:
			users=await bot.get_chat_member(chat_id, user_id)
			username=users.user['username']
			user_fullname=users.user['full_name']
			await new_chat_users_list(connection, user_id, chat_id, username, user_fullname, user_date)
		print('hui')

async def test(message: types.Message):
	chat_id = message.chat.username
	users = await getter_id(chat_id)
	print(users)
	client.run_until_disconnected()



def chats_register(dp:Dispatcher):
	#dp.register_message_handler(new_chat_member, content_types=["new_chat_members"])
	dp.register_message_handler(get_users_on_chat, content_types=['new_chat_members'])
	dp.register_message_handler(test, commands=['hui'])
