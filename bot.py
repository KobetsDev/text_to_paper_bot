#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import random
import threading
import time
import zipfile  # подключаем модуль
from os.path import basename

import telebot
from telebot import types
from telebot.types import InputMediaPhoto  # , Message

import Buttons
from mainPic import CreatePhoto
from dotenv import load_dotenv


# Устанавливаем путь


def main():
    bot = telebot.TeleBot(os.environ.get('API_KEY'))

    def thread(func):  # Функция запуска нового потока
        def wrapper(*args, **kwargs):
            my_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            my_thread.start()

        return wrapper
    user = {}
    slovar_ = {}
    default_font_color = '48, 75, 143'
    default_list_type = 'cell'

    def get_user_data(self2):
        self_id = self2.id
        # Если нет пользователя то создаёт его
        if not self_id in user:
            user[self_id] = {'last_time': 0,
                             'user_name': self2.username,
                             'all_text': '',
                             'text_true': False,
                             'inputs_active': False,
                             'list_type': default_list_type,
                             'font_color': default_font_color,
                             'gif': '',
                             'jdem': '',
                             'font': 'Merkucio',
                             'payments': {},
                             'order': {}}
        return user[self_id]

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        b = bot.send_message(message.from_user.id,
                             f'Привет {message.from_user.first_name}, нажми ▶️Начать◀️ и я всё тебе тут покажу.',
                             reply_markup=Buttons.UserKBstart)
        u = message.message_id
        # bot.delete_message(message.chat.id, u)
        bot.delete_message(message.chat.id, u)

    @bot.callback_query_handler(func=lambda call: True)
    def Select_list_type_work(call):
        user_data = get_user_data(call.from_user)
        if 'Select_list_type_work' in call.data:
            if 'Select_list_type_work_1' == call.data:
                user_data["list_type"] = "cell"
                user_data['order']['list'] = 'В клетку'
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, в клетку.')
                # bot.send_message(message.from_user.id, )
            # Если привелегия VIP >=
            elif 'Select_list_type_work_2' == call.data:  # and user_status[1] >= VIP:
                user_data["list_type"] = "line"
                user_data['order']['list'] = 'В линию'
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, в линию.')
        elif 'Select_font' in call.data:
            if 'Select_font_1' == call.data:
                user_data["font"] = "Merkucio"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран шрифт Merkucio.')
            elif 'Select_font_2' == call.data:
                user_data["font"] = "Abram"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран шрифт Abram.')
            elif 'Select_font_3' == call.data:  # and user_status[1] >= VIP:
                user_data["font"] = "Gregory"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран шрифт Gregory.')
            elif 'Select_font_4' == call.data:  # and user_status[1] >= Premium:
                user_data["font"] = "Lorenco"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран шрифт Lorenco.')
            elif 'Select_font_5' == call.data:  # and user_status[1] >= Premium:
                user_data["font"] = "Merk"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран шрифт Merk.')
            elif 'Select_font_6' == call.data:  # and user_status[1] >= BOSS:
                user_data["font"] = "Salavat"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран шрифт Salavat.')
            # elif 'Select_font_7' == call.data and user_status[1] >= BOSS:
            #     user_data["font"] = "AlisaFont"
            #     bot.answer_callback_query(
            #         callback_query_id=call.id, text='Окей, выбран шрифт AlisaFont.')

        elif 'Select_color_font_work' in call.data:
            # Если привелегия выше VIP
            # print(call.data)
            # print(user_status[1])
            if 'Select_color_font_work_1' == call.data:  # and user_status[1] >= VIP:
                user_data["font_color"] = "65, 105, 225"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран светло синий.')

            # доступен всем
            elif 'Select_color_font_work_2' == call.data:
                user_data["font_color"] = "48, 75, 143"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран синий.')

            elif 'Select_color_font_work_3' == call.data:  # and user_status[1] >= Premium:
                user_data["font_color"] = "49, 88, 143"
                bot.answer_callback_query(callback_query_id=call.id, text='Окей, выбран тёмно синий цвет.')

            elif 'Select_color_font_work_4' == call.data:  # and user_status[1] >= BOSS:
                user_data["font_color"] = "37, 37, 37"
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    text='Окей, выбран чёрный цвет.')

        elif 'Select_space' in call.data:
            # print("qwe")
            bot.answer_callback_query(callback_query_id=call.id, text='Выбери шрифт!')
        # user_status[1] == Admin:
        elif 'AdminPanel' in call.data and call.from_user.id == 420624020 or 569452912:
            # bot.delete_message(message.chat.id, message.message_id+1)
            if 'AdminPanel*UserEdit' == call.data:
                mess = bot.send_message(call.from_user.id, "Ник/id этого грешника мне!")
                bot.register_next_step_handler(mess, UserEdit)
            elif 'AdminPanel*User' in call.data:
                user_data = call.data.replace("AdminPanel*User*", "").split("*")
                # print(user_data)
                if user_data[0] == 'ChangeThePrivilege':
                    # if len(user_data) <= 2:
                    KB_Buy_in_message = types.InlineKeyboardMarkup()  # наша клавиатура
                    cmd = types.InlineKeyboardButton(text="Standart",
                                                     callback_data=f"AdminPanel*User*BonusPrivilege*{user_data[1]}*1")
                    KB_Buy_in_message.add(cmd)
                    for i in slovar_:
                        # print(i)
                        cmd1 = types.InlineKeyboardButton(text=i,
                                                          callback_data=f"AdminPanel*User*BonusPrivilege*{user_data[1]}*{slovar_[i]['id']}")
                        KB_Buy_in_message.add(cmd1)
                    bot.send_message(call.from_user.id, "Какую дадим?", reply_markup=KB_Buy_in_message)

    @bot.message_handler(content_types=['text'])
    def text(message):
        user_data = get_user_data(message.from_user)
        if message.text == '❌Отмена❌' or message.text == '🌚Назад🌝':
            # Удаляем текущее сообщения пользователя
            bot.delete_message(message.chat.id, message.message_id)
            # Удаляем сообщения по выше
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id-2)
            user_data['inputs_active'] = False
            mesu = '''ㅤ💬
🏄\nВыбери любой пункт'''
            bot.send_message(message.from_user.id, mesu, reply_markup=Buttons.UserKB)
        elif user_data['inputs_active']:
            post_text(message)
        elif message.text == '▶️Начать◀️':
            # Удаляем само сообщения начать
            bot.delete_message(message.chat.id, message.message_id)
            # Востанавливаем значения по дефолту до выбора пользователя
            user_data['list_type'] = default_list_type
            user_data['font_color'] = default_font_color
            guide = '📃Инструкция📃\n🗿Это раздел конспектов, сейчас я жду твой конспект.🗿\n⬇️Кстати можешь выбрать лист и цвет и даже шрифт.⬇️'
            bot.send_message(message.from_user.id,
                             '🏄🏽‍♂️', parse_mode='Markdown', reply_markup=Buttons.KB_print)
            bot.send_message(message.from_user.id,
                             guide, parse_mode='Markdown', reply_markup=Buttons.Select_list_type)  # UserKB)
            user_data['inputs_active'] = True

        elif message.text == '📰О сервисе📰':
            about = ''' *Авто конспект* _-_ бот для написания конспектов.
Сервис позволяет забыть о написании своей рукой конспектов,
и занять более полезными вещами.

О сотрудничестве писать: itsunrisetea@gmail.com
'''
            # Служба поддержки: [@WT_Tini] @ssinnerr
            ops = '''😧🕶👌
Тот самый бот, чекни😎
ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ👇
'''
            URLS = f'https://t.me/share/url?text=https://t.me/Text_to_List_Bot?url={ops}'  # start=AK{message.from_user.id}
            ref = types.InlineKeyboardButton(
                text='📣Рассказать друзьям', url=URLS)
            referal_KB = types.InlineKeyboardMarkup()
            referal_KB.add(ref)
            bot.send_message(message.from_user.id,
                             about, parse_mode='Markdown', reply_markup=referal_KB)
        else:
            bot.delete_message(message.chat.id, message.message_id)
            # print(bot.get_message(message.chat.id, message.message_id-1))
            bot.send_message(message.from_user.id,
                             'Нажми на кнопку!', reply_markup=Buttons.UserKB)

    def post_text(message):
        user_data = get_user_data(message.from_user)
        # Устанавливаем время
        if user_data['last_time'] == 0:
            user_data['last_time'] = int(time.time())
        # Если прошло больше 5 секунд
        if int(time.time()) - user_data['last_time'] > 5:
            # Устанавливаем новое время
            user_data['last_time'] = time.time()
            # добавляем то что ввёл пользователь
            user_data['all_text'] += ' ' + str(message.text)
        else:
            # Устанавливаем новое время
            user_data['last_time'] = int(time.time())
            # добавляем то что ввёл пользователь
            user_data['all_text'] += ' ' + str(message.text)
        if user_data['text_true'] == False:
            user_data['last_time'] = int(time.time())
            user_data['text_true'] = True
            mass_gif = [
                os.path.join(BASE_DIR, 'GIF', 'grif.gif'),
                os.path.join(BASE_DIR, 'GIF', 'old_print.gif'),
                os.path.join(BASE_DIR, 'GIF', 'phone.gif'),
                os.path.join(BASE_DIR, 'GIF', 'sister.gif'),
                os.path.join(BASE_DIR, 'GIF', 'kit.gif'),
            ]
            gif = random.choice(mass_gif)
            user_data['gif'] = bot.send_video(
                message.from_user.id,
                open(gif, 'rb'), None,
                'Уже пишу...', reply_markup=Buttons.KB_print_none)
            magic(message)

    @thread
    def magic(message):
        while True:
            user_data = get_user_data(message.from_user)
            # Если прошло 5 секунд
            if int(time.time()) - user_data['last_time'] > 5:
                CP = CreatePhoto(
                    path_save_image_folder=os.path.join(BASE_DIR, 'IMG'),
                    path_global_image_folder=os.path.join(BASE_DIR, 'PAGES'),

                    path_fonts_folder=os.path.join(BASE_DIR, 'Fonts'),
                    size=85,

                    text=user_data['all_text'],
                    user_id=message.from_user.id,
                    font_color=user_data['font_color'],
                    font_name=user_data['font'],
                    page_type=user_data['list_type'],
                )
                path = CP.create()
                # Если одно фото на отправку
                if len(path) == 1:
                    bot.send_photo(message.from_user.id, photo=open(path[0], 'rb'))
                else:
                    image_path = [InputMediaPhoto(open(i, 'rb')) for i in path]
                    # Если мало фоток на отправку
                    if len(path) <= 10:
                        bot.send_media_group(message.chat.id, media=image_path, timeout=10)
                    else:
                        # создаем переменную - название и местоположение файла
                        zname = os.path.join(BASE_DIR, f'{message.from_user.id}.zip')
                        newzip = zipfile.ZipFile(zname, 'w')  # создаем архив
                        for foto in path:
                            newzip.write(foto, basename(foto))  # добавляем файл в архив
                        newzip.close()
                        if os.path.getsize(zname) > 49000000:
                            bot.send_message(message.from_user.id, 'Извини но текста слишком много')
                            os.remove(zname)
                        else:
                            zip_file = open(zname, 'rb')
                            for i in range(5):
                                try:
                                    bot.send_document(message.chat.id, zip_file)
                                    break
                                except:
                                    pass
                            zip_file.close()
                        # del_img(zname)
                bot.send_message(message.from_user.id, 'Захочешь ещё, просто нажми ▶️Начать◀️',
                                 reply_markup=Buttons.UserKB)
                # Удаляем картинки
                del_img(path)
                # Удаляем гифку
                if user_data['gif'] != '':
                    bot.delete_message(message.from_user.id, user_data['gif'].message_id)
                user_data['text_true'] = False
                user_data['all_text'] = ''
                user_data['inputs_active'] = False
                break
            time.sleep(1)

    # @thread
    def del_img(path):
        # time.sleep(15)
        try:
            for i in path:
                # print('Удалем картинку', i)
                os.remove(i)
        except Exception as e:
            print(e)

    bot.infinity_polling()  # none_stop=True,


if '__main__' == __name__:
    absFilePath = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(absFilePath)
    # В конфиге должен лежать api_key бота
    # API_KEY=...
    load_dotenv(os.path.join(BASE_DIR, 'config.env'))
    main()
