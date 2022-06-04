import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import asyncio
import aioschedule
from config import BOT_TOKEN, BOT_PASSWORD
import telegram_service as tel_s


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == "__main__":
    try:
        print('\n[INFO] Telegram bot launched\n')
        executor.start_polling(dp)
    except Exception as _ex:
        print('\n[ERR] Telegram bot startup error:\n', _ex)


# keyboards
bntMainMenu = KeyboardButton('◀️ Главное меню')
# MAIN MENU
bntClients = KeyboardButton('🛄 Клиенты')
bntUsers = KeyboardButton('😐 Пользователи')
btnSubscriptions = KeyboardButton('💲 Подписки клиентов')
MainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bntClients)
MainMenu.row(bntUsers)
MainMenu.row(btnSubscriptions)
# USERS MENU
bntGetUsers = KeyboardButton('🙌 Все пользователи', callback_data='AllUsers')
bntAddUser = KeyboardButton('😊 Добавить')
bntDeleteUser = KeyboardButton('😒 Удалить')
UsersMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bntGetUsers)
UsersMenu.row(bntAddUser, bntDeleteUser)
UsersMenu.row(bntMainMenu)
# CLIENTS MENU
bntGetClients = KeyboardButton('👥 Все клиенты')
bntAddClient = KeyboardButton('🤝 Добавить клиента')
bntDeleteClient = KeyboardButton('🗿 Удалить клиента')
ClientsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bntGetClients)
ClientsMenu.row(bntAddClient, bntDeleteClient)
ClientsMenu.row(bntMainMenu)
# SUBSCRIPTIONS MENU
bntGetClients = KeyboardButton('👥 Все клиенты')
bntActiveSubs = KeyboardButton('Активные подписки')
bntNoActiveSubs = KeyboardButton('История подписок')
bntAddSub = KeyboardButton('Добавить подписку')
bntDeleteSub = KeyboardButton('Удалить подписку')
bntAddUnlimitedSub = KeyboardButton('Добавить безлимитную подписку')
SubsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bntGetClients)
SubsMenu.row(bntActiveSubs, bntNoActiveSubs)
SubsMenu.row(bntAddSub, bntDeleteSub)
SubsMenu.row(bntAddUnlimitedSub, bntMainMenu)
#  CANCEL MENU
bntCancel = KeyboardButton('Отмена')
CancelMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bntCancel)


# States


class Form(StatesGroup):
    sign_in = State()  # Will be represented in storage as 'Form:sign_in'


class User(StatesGroup):
    user_delete = State()
    user_create_id = State()
    user_create_name = State()


class Client(StatesGroup):
    client_delete = State()
    client_create_name = State()


# START


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if tel_s.user_already_exist(message.from_user.id):
        await message.reply("Добро пожаловать с:", reply_markup=MainMenu)
    else:
        await Form.sign_in.set()
        await message.reply("Вы не зарегестрированы в боте -_-")
        await message.answer("Введите пароль доступа!")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        if tel_s.user_already_exist(message.from_user.id):
            await message.reply('Отменено.', reply_markup=MainMenu)
            return
        else:
            await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())
            return
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    if current_state == Form.sign_in:
        await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply('Отменено.', reply_markup=MainMenu)


@dp.message_handler(lambda message: message.text != BOT_PASSWORD, state=Form.sign_in)
async def process_gender_invalid(message: types.Message):
    # Wrong password
    return await message.reply("Неправильный пароль. Повторите ввод пароля")


@dp.message_handler(state=Form.sign_in)
async def sign_in(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    await Form.next()
    await message.reply("Пароль правильный", reply_markup=MainMenu)

    # Finish authorization
    await state.finish()


# MAIN MENU


@dp.message_handler(commands='main')
@dp.message_handler(Text(equals='◀️ Главное меню'))
async def main(message: types.Message):
    await message.answer('◀️', reply_markup=MainMenu)


@dp.message_handler(commands='clients')
@dp.message_handler(Text(equals='🛄 Клиенты'))
async def clients(message: types.Message):
    await message.answer('🛄', reply_markup=ClientsMenu)


@dp.message_handler(commands='users')
@dp.message_handler(Text(equals='😐 Пользователи'))
async def users(message: types.Message):
    await message.answer('😐', reply_markup=UsersMenu)


@dp.message_handler(Text(equals='💲 Подписки клиентов'))
async def subscriptions(message: types.Message):
    await message.answer('💲', reply_markup=SubsMenu)


# CLIENTS


@dp.message_handler(commands='all_clients')
@dp.message_handler(Text(equals='👥 Все клиенты'))
async def all_clients(message: types.Message):
    all_clients = tel_s.get_all_clients()
    if len(all_clients) == 0:
        await message.answer('Пока что нет ни одного клиента.')
        return

    markup = InlineKeyboardMarkup(row_width=2)
    btns = []
    for id, name, _ in all_clients:
        btns.append(InlineKeyboardButton(text=name, callback_data=f"client_{id}"))
    markup.add(*btns)
    await message.answer('Все клиенты:', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('client_'))
async def callback_client(call: types.callback_query):
    client_id = call.data.split('_')[1]
    client_info = tel_s.get_client_info(client_id)
    if len(client_info) == 0:
        await call.message.answer(f'Клиента с id {client_id} уже не существует!', reply_markup=ClientsMenu)
    else:
        await call.message.answer(f'ID: {client_info[0]}\nНаименование: {client_info[1]}\nАктивен: {client_info[2]}', reply_markup=ClientsMenu)
    await call.answer()


@dp.message_handler(Text(equals='🗿 Удалить клиента'))
async def del_user(message: types.Message):
    await Client.client_delete.set()
    await message.answer('Отправьте id клиента:', reply_markup=CancelMenu)


@dp.message_handler(state=Client.client_delete)
async def del_user_finish(message: types.Message, state: FSMContext):
    res = tel_s.delete_client(message.text)
    await message.reply(res, reply_markup=MainMenu)
    await state.finish()


@dp.message_handler(Text(equals='🤝 Добавить клиента'))
async def del_user(message: types.Message):
    await Client.client_create_name.set()
    await message.answer('Отправьте наименование пользователя:', reply_markup=CancelMenu)


@dp.message_handler(lambda message: message.text, state=Client.client_create_name)
async def process_user_id(message: types.Message, state: FSMContext):
    res = tel_s.create_new_client(message.text)
    await message.reply(res[1], reply_markup=MainMenu)
    await state.finish()


# USERS MENU


@dp.message_handler(commands='all_users')
@dp.message_handler(Text(equals='🙌 Все пользователи'))
async def all_users(message: types.Message):
    all_users = tel_s.get_all_users()
    if len(all_users) == 0:
        await message.answer('Пока что нет ни одного пользователя.')
        return

    markup = InlineKeyboardMarkup(row_width=2)
    btns = []
    for user_id, user_name in all_users:
        btns.append(InlineKeyboardButton(text=user_name, callback_data=f"user_{user_id}"))
    markup.add(*btns)
    await message.answer('Все пользователи:', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('user_'))
async def callback_user(call: types.callback_query):
    user_id = call.data.split('_')[1]
    if tel_s.user_already_exist(user_id):
        await call.message.answer(f'ID: {user_id}', reply_markup=UsersMenu)
    else:
        await call.message.answer(f'Пользователя с ID: {user_id} уже не существует!', reply_markup=UsersMenu)
    await call.answer()


@dp.message_handler(Text(equals='😒 Удалить'))
async def del_user(message: types.Message):
    await User.user_delete.set()
    await message.answer('Отправьте id пользователя:', reply_markup=CancelMenu)


@dp.message_handler(state=User.user_delete)
async def del_user_finish(message: types.Message, state: FSMContext):
    res = tel_s.delete_user(message.text)
    await message.reply(res, reply_markup=MainMenu)
    await state.finish()


@dp.message_handler(Text(equals='😊 Добавить'))
async def del_user(message: types.Message):
    await User.user_create_id.set()
    await message.answer('1) Отправьте id пользователя:', reply_markup=CancelMenu)


@dp.message_handler(lambda message: not message.text.isdigit(), state=User.user_create_id)
async def process_age_invalid(message: types.Message):
    # If user id is invalid
    return await message.reply("Неверный id пользователя! Отправьте правильный id")


@dp.message_handler(lambda message: message.text.isdigit(), state=User.user_create_id)
async def process_user_id(message: types.Message, state: FSMContext):
    if len(message.text) != 9:
        return await message.reply("Неверный id пользователя! Отправьте правильный id")

    await User.user_create_name.set()
    async with state.proxy() as data:
        data['user_id'] = message.text

    await message.reply("2) Теперь отправьте имя пользователя")


@dp.message_handler(lambda message: message.text, state=User.user_create_name)
async def process_user_mame(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text

    res = tel_s.create_new_user(user_id=data['user_id'],user_name=data['user_name'])
    await message.reply(res[1], reply_markup=MainMenu)
    await state.finish()


# START BOT


def start_bot():
    if BOT_TOKEN is not None:
        try:
            print('\n[INFO] Telegram bot launched\n')
            executor.start_polling(dp)  # on_startup=on_startup
        except Exception as _ex:
            print('\n[ERR] Telegram bot startup error:\n', _ex)


async def add_msg_to_list(uid: int, msg_id: int):
    if uid not in users_messages:
        users_messages[uid] = [msg_id, ]
    else:
        users_messages[uid].append(msg_id)


async def on_startup(_):
    asyncio.create_task(scheduler())


async def do_something():
    pass


async def scheduler():
    aioschedule.every().day.at("2:50").do(do_something)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0)

