from config import Config
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from models import client


class Keyboards:
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.text = cfg.misc.buttons_texts
        self.add_profile_cd = CallbackData("add_profile", "level")
        self.select_group_cd = CallbackData("select_group", "id")

        self.back_cd = CallbackData("back")

    async def start_kb(self, user_id=None):

        autorization_url = f"https://oauth.vk.com/authorize?client_id={self.cfg.tg_bot.client_id}&display=page&redirect_uri={self.cfg.tg_bot.redirect_uri}&scope=wall,groups,photos,offline&response_type=code&v=5.131&state={user_id}"
        kb = InlineKeyboardMarkup(row_width=3)
        kb.add(InlineKeyboardButton(text="Авторизоваться", url=autorization_url))
        kb.add(InlineKeyboardButton(
            text="Добавить группу в тг", callback_data='tg_group'))
        kb.add(InlineKeyboardButton(
            text="Добавить сообщество", callback_data='vk_group'))
        kb.add(InlineKeyboardButton(
            text="Список каналов и групп", callback_data='groups_list'))
        return kb

    async def groups_kb(self, groups: list[client.Telegram_group]):
        kb = InlineKeyboardMarkup()

        for group in groups:
            kb.add(InlineKeyboardButton(
                text=group.username, callback_data=self.select_group_cd.new(id=group.id)))
        kb.add(InlineKeyboardButton(text="Назад",
               callback_data=self.back_cd.new()))
        return kb

    async def back_kb(self):
        kb = InlineKeyboardMarkup()

        kb.add(InlineKeyboardButton(text="Назад",
               callback_data=self.back_cd.new()))

        return kb
