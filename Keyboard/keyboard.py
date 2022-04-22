from telebot.types import KeyboardButton, ReplyKeyboardMarkup

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

add_order_button = KeyboardButton("Добавить заказ")
get_orders_list_button = KeyboardButton("Список заказов")

admin_keyboard.add(add_order_button, get_orders_list_button)


