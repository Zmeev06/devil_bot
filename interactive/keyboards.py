import asyncio
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from telethon.client import buttons

async def start_keyboard ():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text='Узнать команды',
            callback_data='help'
         ))
    return markup