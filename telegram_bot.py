import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
import asyncio
import aioschedule
from config import BOT_TOKEN, BOT_PASSWORD


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
bntGetUsers = KeyboardButton('🙌 Все пользователи')
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
bntAddSub = KeyboardButton('Добавить')
bntDeleteSub = KeyboardButton('Удалить')
bntAddUnlimitedSub = KeyboardButton('Добавить безлимитную')
SubsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bntGetClients)
SubsMenu.row(bntActiveSubs, bntNoActiveSubs)
SubsMenu.row(bntAddSub, bntDeleteSub)
SubsMenu.row(bntAddUnlimitedSub, bntMainMenu)


# States
class Form(StatesGroup):
    sign_in = State()  # Will be represented in storage as 'Form:sign_in'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.sign_in.set()

    await message.reply("Вы не зарегестрированы в боте!")
    await message.answer("Введите пароль доступа")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text not in BOT_PASSWORD, state=Form.sign_in)
async def process_gender_invalid(message: types.Message):
    # Wrong password
    return await message.reply("Неправильный пароль. Повторите ввод пароля")


@dp.message_handler(state=Form.sign_in)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    await Form.next()
    await message.reply("Пароль правильный", reply_markup=MainMenu)

    # Finish authorization
    await state.finish()


# MAIN MENU
@dp.message_handler(Text(equals='◀️ Главное меню'))
async def main(message: types.Message):
    await message.answer('◀️ Главное меню', reply_markup=MainMenu)


@dp.message_handler(Text(equals='🛄 Клиенты'))
async def clients(message: types.Message):
    await message.answer('🛄 Клиенты', reply_markup=ClientsMenu)


@dp.message_handler(Text(equals='😐 Пользователи'))
async def users(message: types.Message):
    await message.answer('😐 Пользователи', reply_markup=UsersMenu)


@dp.message_handler(Text(equals='💲 Подписки клиентов'))
async def subscriptions(message: types.Message):
    await message.answer('💲 Подписки клиентов', reply_markup=SubsMenu)


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

