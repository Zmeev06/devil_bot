import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.exceptions import MessageNotModified
import aiogram.utils.markdown as fmt
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, CommandStart
from aiomysql import connection

from tgbot.database import connect, close_connection

logger = logging.getLogger(__name__)


async def new_family (message:types.Message):
    connection = await connect()
    if message.chat.type == 'private':
        message_text = fmt.text(
            fmt.text('Укажите фамилию вашей семьи')
        )
        message.reply(
            text=message_text,
            reply=False,
            disable_web_page_preview=True
        )
        family_name = message.text.split()
        del family_name [0]; del family_name [0]
        family_name = ' '.join(family_name)

        username = message.from_user.username
        full_name = message.from_user.full_name
        user_id = message.from_user.id
    else:
        message_text = fmt.text(
            fmt.text('Чтоб создать семью, напишите мне в личные сообщения команду ".создать семью"')
        )
        await message.reply(
            text=message_text,
            reply=False,
            disable_web_page_preview=True
        )


def family_register (dp: Dispatcher):
    dp.register_message_handler(new_family, lambda message: message.text.lower().startswith('.создать семью'))