from telebot.types import KeyboardButton, ReplyKeyboardMarkup

back_button = KeyboardButton("Назад")

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

add_order_button = KeyboardButton("Добавить заказ")
get_orders_list_button = KeyboardButton("Список заказов")

admin_keyboard.add(add_order_button, get_orders_list_button)

order_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

edit_order_button = KeyboardButton("Изменить заказ")
delete_order_button = KeyboardButton("Удалить заказ")
finish_order_button = KeyboardButton("Закрыть заказ")

order_keyboard.add(edit_order_button, delete_order_button, finish_order_button)



