import CONFIG
import datetime

from telebot import TeleBot, types
from itertools import permutations
from Database.ordersDatabase import OrdersDatabase
from Database.userDatabase import UserDatabase
from Keyboard import keyboard
from order import *


DATABASE_PATH = "database.db"

bot = TeleBot(CONFIG.TOKEN, threaded=True)

user_database = UserDatabase(DATABASE_PATH)
orders_database = OrdersDatabase(DATABASE_PATH)


def validate(func):

    def wrapper(message):
        if message.from_user.id in CONFIG.ADMIN_LIST:
            return func(message)
        else:
            return

    return wrapper


@bot.message_handler(commands=['start'])
@validate
def welcome(message):
    bot.send_message(message.chat.id, text="Привет! Это бот администратор Marusya!",
                     reply_markup=keyboard.admin_keyboard)


@bot.message_handler(content_types='text')
@validate
def order_adding(message: types.Message):
    if message.text == keyboard.add_order_button.text:
        create_order(message)
    elif message.text == keyboard.get_orders_list_button.text:
        orders = orders_database.get_orders_by_offset(0)

        bot.send_message(message.from_user.id, text="Список заказов:",
                         reply_markup=get_inline_orders(orders, 0))


@bot.callback_query_handler(func=lambda call: True)
def order_selector(call: types.CallbackQuery):
    if call.data in ["back", "forward"]:
        current_page = int(call.message.json["reply_markup"]["inline_keyboard"][0][0]["callback_data"])

        if current_page == 0 and call.data == "back":
            return

        offset = 1 if call.data == "forward" else -1

        bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id,
                                      reply_markup=get_inline_orders(
                                          orders_database.get_orders_by_offset(current_page + offset),
                                          current_page + offset
                                      ))

    elif call.data.startswith("edit"):
        pass

    elif call.data.startswith("delete"):
        order_id = call.data.split(" ")[1]

        orders_database.delete_order(int(order_id))
        bot.send_message(call.message.chat.id, text="Заказ удален!", reply_markup=keyboard.admin_keyboard)

    elif call.data.startswith("finish"):
        pass

    else:
        order = orders_database.find_order_by_id(int(call.data))

        bot.send_message(call.message.chat.id, text=get_order_string(order),
                         reply_markup=get_order_inline_keyboard(order[ORDER_ID]))


def get_order_inline_keyboard(order_id: int):
    order_keyboard = types.InlineKeyboardMarkup()

    edit_order_button = types.InlineKeyboardButton("Редактировать", callback_data=f"edit_order {order_id}")
    delete_order_button = types.InlineKeyboardButton(f"Удалить", callback_data=f"delete_order {order_id}")
    finish_order_button = types.InlineKeyboardButton(f"Завершить", callback_data=f"finish_order {order_id}")

    order_keyboard.add(edit_order_button, delete_order_button, finish_order_button)

    return order_keyboard


def get_inline_orders(order_list, current_page):
    items = types.InlineKeyboardMarkup()

    items.add(types.InlineKeyboardButton(f"Страница: {current_page + 1}", callback_data=str(current_page)))

    for order in order_list:
        order_string = get_inline_order_string(order)
        button = types.InlineKeyboardButton(order_string, callback_data=order[ORDER_ID])
        items.add(button)

    items.row(types.InlineKeyboardButton("<<", callback_data="back"),
              types.InlineKeyboardButton(">>", callback_data="forward"))

    return items


def get_order_string(order):
    order_client = user_database.find_user_by_id(order[USER_ID])
    return f"""Заказ № {order[ORDER_ID]}:
Заказчик: {order_client[1]}, {order_client[2]}
Изделие: {order[PRODUCT]}
Мерки: {order[SIZES]}
Дата окончания работы: {order[FINISH_DATE]}
Стадия работы: {order[STAGE]}
Статус оплаты: {order[PRICE_INFO]}"""


def get_inline_order_string(order):
    order_client = user_database.find_user_by_id(order[USER_ID])
    return f"""{order_client[1]}, {order[PRODUCT]}, {order[STAGE]}"""


def create_order(message: types.Message):
    order = Order()

    def input_first_name(m):
        order.client_name = m.text
        bot.send_message(message.from_user.id, text="Введите номер клиента")
        bot.register_next_step_handler(message, input_client_phone)

    def input_client_phone(m):
        order.client_phone = m.text
        bot.send_message(message.from_user.id, text="Введите тип изделия")
        bot.register_next_step_handler(message, input_product_type)

    def input_product_type(m):
        order.product = m.text
        bot.send_message(message.from_user.id, text="Введите размеры закзачика")
        bot.register_next_step_handler(message, input_sizes)

    def input_sizes(m):
        order.sizes = m.text
        bot.send_message(message.from_user.id, text="Введите дату оканчания работы")
        bot.register_next_step_handler(message, input_finish_date)

    def input_finish_date(m):
        order.finish_date = m.text
        bot.send_message(message.from_user.id, text="Введите стадию работы")
        bot.register_next_step_handler(message, input_stage)

    def input_stage(m):
        order.stage = m.text
        bot.send_message(message.from_user.id, text="Введите информацию об оплате")
        bot.register_next_step_handler(message, input_price_info)

    def input_price_info(m):
        order.price_info = m.text
        add_order(order)

    order.start_date = datetime.date.today()

    bot.send_message(message.from_user.id, text="Введите ФИО закзачика")
    bot.register_next_step_handler(message, input_first_name)


def notify_admins():
    order = orders_database.get_last_added_item()

    for admin in CONFIG.ADMIN_LIST:
        bot.send_message(admin, "Новый заказ создан!")
        bot.send_message(admin, get_order_string(order))


def find_user(name: str):
    user = None

    combos = list(permutations(name.split()))

    for comb_name in combos:
        name = " ".join(comb_name)
        user = user_database.find_user_by_name(name)

        if user is not None:
            return user

    return user


def add_order(order: Order):

    client = find_user(order.client_name)

    if client is None:
        user_database.add_user(order.client_name, order.client_phone)

        client = user_database.get_last_added_item()

    orders_database.add_order(client[0], order.sizes, order.product, order.start_date,
                              order.finish_date, order.stage, order.price_info)

    notify_admins()


if __name__ == '__main__':
    bot.infinity_polling()
