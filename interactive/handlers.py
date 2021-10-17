import random
import asyncio

import aiogram.utils.markdown as fmt
from aiogram import Bot, types
from aiogram import Dispatcher


from load_all import bot
from interactive import keyboards

async def start (message: types.Message):
    if message.chat.type == 'private':
        message_text = fmt.text(
            fmt.text('Привет!'),
            fmt.text('Чтоб ознакомиться с моими командами нажимай на кнопку'),
            fmt.text('Для обратной связи пишите @serenaflowrichard')
        )
        await message.reply(
            text=message_text,
            reply=False,
            reply_markup=await keyboards.start_keyboard(),
            disable_web_page_preview=True
        )

async def russian_roulette(message:types.Message):
	user_id=message.from_user.id
	name=message.from_user.full_name
	i=random.randint(0,100)
	if i <= 20:
		await message.reply(f'<a href="tg://user?id={user_id}">{name}</a> совсем ополоумел и решил сыграть в русскую рулетку.\
			\nУдача была не на его стороне, поэтому он вынес себе мозг(мут на 10 минут)', parse_mode=types.ParseMode.HTML)
		await bot.restrict_chat_member(
			chat_id=-1001133240329,
			 user_id=message.from_user.id,
			  permissions=types.ChatPermissions(can_send_messages=False, 
			  can_send_media_messages=False,
			   can_send_polls=False,
			    can_send_other_messages=False)
		)
		await asyncio.sleep(600)
		await bot.restrict_chat_member(
			chat_id=-1001133240329,
			 user_id=message.from_user.id,
			  permissions=types.ChatPermissions(can_send_messages=True, 
			  can_send_media_messages=True,
			   can_send_polls=True,
			    can_send_other_messages=True))
	else:
		await message.reply(f'<a href="tg://user?id={user_id}">{name}</a>, в этот раз тебе повезло, но я бы не советовала играться с оружием. Хих', parse_mode=types.ParseMode.HTML)


async def boobs(message: types.Message):
	chat_id=message.chat.id
	photo='https://r1.mt.ru/r2/photoCF3E/20175309137-0/png/bp.jpeg'
	await bot.send_photo(chat_id, photo)

async def love(message:types.Message):
	await message.reply_sticker(r'CAACAgIAAxkBAAMkYKVPVoBgBf00MfKKrPuWySP2h0EAAgkDAAM4oArsoUihizudAh8E')


def interactive_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(russian_roulette, lambda message: message.text.lower()=='.русская рулетка')
    dp.register_message_handler(boobs, lambda message: message.text.lower()=='.сиськи')
    dp.register_message_handler(love, lambda message:message.text.lower()=='зайцы')