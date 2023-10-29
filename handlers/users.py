from aiogram import types, Bot
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from pyrogram import Client

from utils import vkontakte
from config import Config
from db import Database
from keyboards.keyboards import Keyboards
import os
from models.client import Telegram_group


async def start(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    markup = await kb.start_kb(user_id=message.from_user.id)
    db.add_user(message.from_user.id,
                message.from_user.full_name,
                message.from_user.username
                )
    await message.answer(cfg.misc.messages.start, reply_markup=markup)


async def post_handler(message: types.Message):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    bot: Bot = ctx_data.get()['bot']

    # if message.photo:
    #     caption = None
    #     photos = list()

    #     try:

    #         global last_photos
    #         mg = await client.get_media_group(message.chat.id,message.id)

    #         # print(last_photos)
    #         photos_id = [m.photo.file_id for m in mg]
    #         if last_photos == set(photos_id):
    #             return
    #         last_photos = set(photos_id)
    #         for m in mg:
    #             if m.caption:
    #                 caption = m.caption
    #             photo = await client.download_media(message)
    #             photos.append(photo)

    #         vkontakte.WallPost(caption,photos)
    #     except:
    #         photo = await client.download_media(message)
    #         vkontakte.WallPost(message.caption,[photo,])
    #         os.remove(photo)
    #     finally:
    #         for photo in photos:
    #             os.remove(photo)

    #     return

    chat = db.get_chat_data(message.chat.id)
    user = db.get_user(chat.telegram_id)
    vk = vkontakte.vk_manager(user.vk_access_token, chat.vk_group_id)
    res = vk.post(message.text)
    if res != "success":
        await bot.send_message(user.telegram_id, "<b>Ваша авторизация вконтакте не сработала, авторизуйтесь заново.>/b>")


async def add_vk_group(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer("""Отправьте id группы в вк.\n
Чтобы получить id:\n\n
Откройте любую фотографию пользователя/сообщества; первые цифры после слова photo (XXXXXX в ссылке вида https://vk.com/photoXXXXXX_YYYYYYY) — это и есть интересующий вас ID.\n\n
Бот не будет работать, если вы не авторизовались во вконтакте.
""")
    await state.set_state("vk_group_id")


async def wait_vk_group_id(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    await state.set_data({"id": message.text, })
    await message.answer("Введите название сообщества")
    await state.set_state("vk_group_name")


async def wait_vk_group_name(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    db: Database = ctx_data.get()['db']
    kb: Keyboards = ctx_data.get()['keyboards']
    await state.update_data(name=message.text)

    groups = db.get_all_user_tg_groups(message.from_user.id)
    markup = await kb.groups_kb(groups=groups)
    await message.answer("Выберите группу, из которой будут пересылаться данные", reply_markup=markup)
    await state.set_state("vk_group_telegram_group",)


async def wait_vk_group_telegram_group(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    await state.update_data(telegram_group_id=callback_data["id"])

    data = await state.get_data()
    db.set_vk_data_to_rg_group(data)
    await callback.message.answer("Успешно!")
    await state.finish()
    await state.reset_data()


def make_groups_text(groups: list[Telegram_group]) -> str:
    result = ""
    counter = 0
    for group in groups:
        counter += 1
        result += f"{counter} - TG: {group.username} (id - {group.chat_id}) VK: {group.vk_group_name} (id - {group.vk_group_id})\n"

    return result


async def groups_list(callback: types.CallbackQuery, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']

    groups = db.get_all_user_tg_groups(callback.from_user.id)
    result = make_groups_text(groups)
    await callback.message.answer(result)


async def add_tg_group(callback: types.CallbackQuery, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']

    await callback.message.answer("""Отправьте id группы в telegram или ссылку на нее.\n""")
    await state.set_state("tg_group_id")


async def clear_link(link):
    if "https://t.me/" in link:
        result = link.replace("https://t.me/", "")

    if "@" in link:
        result = link.replace("@", "")

    return result


async def get_chat(link):

    client = Client("+79283529546", api_id=27044267, api_hash="a7448d0befc9804176b9c917898d923a",
                    phone_number="+79283529546", workdir="sessions/")
    await client.connect()
    chat = await client.get_chat(link)
    await client.disconnect()

    return chat


async def wait_tg_group_id(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']

    bot: Bot = ctx_data.get()['bot']
    link = await clear_link(message.text)
    chat = await get_chat(link)
    await message.answer(f"Добавлена группа - {chat.username}")
    db.add_tg_chat(message.from_user.id, chat.username, chat.id)
    await state.finish()
    # try:
    # except Exception as ex:
    #     await message.answer(str(ex))


def register_user_handlers(dp: Dispatcher, cfg: Config, kb: Keyboards, db: Database):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(post_handler,
                                lambda x: x.chat.type in (
                                    types.ChatType.GROUP, types.ChatType.SUPERGROUP, types.ChatType.CHANNEL),
                                state="*")
    dp.register_message_handler(wait_vk_group_id, state="vk_group_id")
    dp.register_message_handler(wait_vk_group_name, state="vk_group_name")
    dp.register_callback_query_handler(
        wait_vk_group_telegram_group, kb.select_group_cd.filter(), state="vk_group_telegram_group")

    dp.register_message_handler(wait_tg_group_id, state="tg_group_id")

    dp.register_callback_query_handler(
        add_tg_group, lambda x: x.data == "tg_group", state="*")
    dp.register_callback_query_handler(
        add_vk_group, lambda x: x.data == "vk_group", state="*")
    dp.register_callback_query_handler(
        groups_list, lambda x: x.data == "groups_list", state="*")
