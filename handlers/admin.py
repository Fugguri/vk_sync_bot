from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from config import Config
from db import Database
from keyboards.keyboards import Keyboards

async def admin(message: types.Message):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    
    markup = await kb.admin_kb()
    
    await message.answer("Выберите пункт меню",reply_markup=markup)

async def give_access(callback: types.CallbackQuery, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    
    markup = await kb.admin_kb()
    
    await callback.message.answer("Введите id или username пользователя",reply_markup=markup)
    
    await state.set_state("give_access")


async def take_access(callback: types.CallbackQuery, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    
    markup = await kb.admin_kb()
    
    await callback.message.answer("Введите id или username пользователя",reply_markup=markup)

    
    await state.set_state("take_access")

async def give_user_access(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    
    markup = await kb.admin_kb()
    # try:
    db.give_access(message.text)
    await message.answer("Обновлено!",reply_markup=markup)
    # except:
    #     await message.answer("Неудачно!\nПроверьте данные.",reply_markup=markup)

async def take_user_access(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    
    markup = await kb.admin_kb()
    # try:
    db.take_access(message.text)
    await message.answer("Обновлено!",reply_markup=markup)
    # except:
        # await message.answer("Неудачно!\nПроверьте данные.",reply_markup=markup)
        


def register_admin_handlers(dp: Dispatcher, cfg: Config, kb: Keyboards, db:Database ):
    
    dp.register_message_handler(admin,commands="admin",state="*")
    
    dp.register_callback_query_handler(give_access,lambda call: call.data=="access grand",state="*")
    dp.register_callback_query_handler(take_access,lambda call: call.data=="access denied",state="*")
    
    dp.register_message_handler(give_user_access,state="give_access")
    dp.register_message_handler(take_user_access,state="take_access")
    
    