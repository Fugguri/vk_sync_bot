import asyncio
import logging
import openai
import sys
from db.sqlite_connection import Database
from config import load_config
from keyboards.keyboards import Keyboards
from handlers.users import register_user_handlers
from handlers.admin import register_admin_handlers

from middlewares.environment import EnvironmentMiddleware
from aiogram import Bot, Dispatcher, executor, utils
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
logger = logging.getLogger(__name__)


async def register_all_middlewares(dp, config, keyboards, db, bot):

    dp.middleware.setup(EnvironmentMiddleware(
        config=config, db=db, keyboards=keyboards, bot=bot, ))


def register_all_handlers(dp, config, keyboards, db, ):
    register_admin_handlers(dp, config, keyboards, db)
    register_user_handlers(dp, config, keyboards, db)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        # filename="logs.log"
    )
    logger.info("Starting bot")
    print("Starting bot")
    config = load_config("config.json", "texts.yml")
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    db = Database(config.tg_bot.db_name)
    dp = Dispatcher(bot, storage=storage)
    kbs = Keyboards(config)

    # openai.api_key = config.tg_bot.openai

    db.cbdt()
    bot['keyboards'] = kbs
    bot['config'] = config
    await register_all_middlewares(dp, config, kbs, db, bot)
    register_all_handlers(dp, config, kbs, db)

    # start
    dp.skip_updates = False
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
    except utils.exceptions.TerminatedByOtherGetUpdates:
        sys.exit()
