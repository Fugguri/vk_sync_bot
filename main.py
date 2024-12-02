import asyncio
import logging
import sys
from db.sqlite_connection import Database
from config import load_config
from keyboards.keyboards import Keyboards
from handlers.users import register_user_handlers
from handlers.admin import register_admin_handlers

from middlewares import AlbumHandler, environment
from aiogram import Bot, Dispatcher, utils
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logger = logging.getLogger(__name__)


async def register_all_middlewares(dp, config, keyboards, db, bot):

    dp.middleware.setup(environment.EnvironmentMiddleware(
        config=config, db=db, keyboards=keyboards, bot=bot, ))
    dp.middleware.setup(AlbumHandler.AlbumMiddleware())


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

    bot['keyboards'] = kbs
    bot['config'] = config
    await register_all_middlewares(dp, config, kbs, db, bot)
    register_all_handlers(dp, config, kbs, db)

    dp.skip_updates = False
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()

if __name__ == '__main__':
    # from backend import app
    # import uvicorn
    # from threading import Thread
    try:
        # backend = Thread(target=uvicorn.run, kwargs={
        #     "app": app, "host": '0.0.0.0', "port": 8000})
        # backend.start()

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
    except utils.exceptions.TerminatedByOtherGetUpdates:
        sys.exit()
