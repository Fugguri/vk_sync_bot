from dataclasses import dataclass


@dataclass
class UserClient:
    id: int
    user_id: int
    api_id: int
    api_hash: str
    phone: str
    ai_settings: str
    mailing_text: str
    answers: int
    gs: str
    is_active: bool


@dataclass
class User:
    id: int
    telegram_id: int
    full_name: str
    vk_access_token: str
    username: str


@dataclass
class Telegram_group:
    id: int
    telegram_id: int
    vk_group_id: str
    vk_group_name: str
    username: str
    chat_id: str
    user_telegram_id: int
