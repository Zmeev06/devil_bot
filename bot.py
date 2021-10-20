import asyncio
import logging

from load_all import bot, DP

from chats.handlers import chats_register


logger = logging.getLogger(__name__)




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    chats_register(DP)
    

    # start
    try:
        # await on_startup()
        await DP.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
