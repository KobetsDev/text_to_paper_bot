
from telebot import types

Select_list_type = types.InlineKeyboardMarkup()  # наша клавиатура
otv1 = types.InlineKeyboardButton(
    text="Страница в клетку", callback_data=f"Select_list_type_work_1")
otv2 = types.InlineKeyboardButton(
    text="Страница в линию", callback_data=f"Select_list_type_work_2")
otv_color_1 = types.InlineKeyboardButton(
    text="Светло синий", callback_data=f"Select_color_font_work_1")
otv_color_2 = types.InlineKeyboardButton(
    text="Синий", callback_data=f"Select_color_font_work_2")
otv_color_3 = types.InlineKeyboardButton(
    text="Тёмно синий", callback_data=f"Select_color_font_work_3")
otv_color_4 = types.InlineKeyboardButton(
    text="Чёрный", callback_data=f"Select_color_font_work_4")

space = types.InlineKeyboardButton(
    text="⬇️Шрифты⬇️", callback_data=f"Select_space")

otv_font_1 = types.InlineKeyboardButton(
    text="Merkucio", callback_data=f"Select_font_1")
otv_font_2 = types.InlineKeyboardButton(
    text="Abram", callback_data=f"Select_font_2")
otv_font_3 = types.InlineKeyboardButton(
    text="Gregory", callback_data=f"Select_font_3")
otv_font_4 = types.InlineKeyboardButton(
    text="Lorenco", callback_data=f"Select_font_4")
otv_font_5 = types.InlineKeyboardButton(
    text="Merk", callback_data=f"Select_font_5")
otv_font_6 = types.InlineKeyboardButton(
    text="Salavat", callback_data=f"Select_font_6")

Select_list_type.row(otv1, otv2)  # добавляем кнопку в клавиатуру
Select_list_type.row(otv_color_1, otv_color_2, otv_color_3, otv_color_4)
Select_list_type.row(space)
Select_list_type.row(otv_font_1, otv_font_2, otv_font_3, otv_font_4)
Select_list_type.row(otv_font_5, otv_font_6)  # , otv_font_7)


UserKBstart = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True)  # наша клавиатура
button0 = types.KeyboardButton(text='▶️Начать◀️')
button1 = types.KeyboardButton(text=' ')
button2 = types.KeyboardButton(text=' ')
button3 = types.KeyboardButton(text=' ')
UserKBstart.row(button0)
UserKBstart.row(button1, button2, button3)

KB_print = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True)  # наша клавиатура
b0 = types.KeyboardButton(text=' ')
b1 = types.KeyboardButton(text=' ')
b2 = types.KeyboardButton(text=' ')
b3 = types.KeyboardButton(text='❌Отмена❌')
KB_print.row(b0)
KB_print.row(b1, b2)
KB_print.row(b3)

KB_print_none = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True)  # наша клавиатура
b0 = types.KeyboardButton(text=' ')
b1 = types.KeyboardButton(text=' ')
b2 = types.KeyboardButton(text=' ')
b3 = types.KeyboardButton(text=' ')
KB_print_none.row(b0)
KB_print_none.row(b1, b2)
KB_print_none.row(b3)

UserKB = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True)  # наша клавиатура
button0 = types.KeyboardButton(text='▶️Начать◀️')
button3 = types.KeyboardButton(text='📰О сервисе📰')
UserKB.row(button0)
UserKB.row(button3)
