# -*- coding: utf-8 -*-
import os
import random
import time

from PIL import Image, ImageDraw, ImageFont

from art_to_page import Drawing
from defis_text import split_a_text

import os


class OpenImage(object):
    """Открываем картинку листка"""

    def __init__(self, path_save_image_folder, page_type, path_global_image_folder):
        self.path_save_image_folder = path_save_image_folder
        self.page_type = page_type
        self.path_global_image_folder = path_global_image_folder
        # self.REFLECTED_PAGE = REFLECTED_PAGE

    def _load_cell_list(self, REFLECTED_PAGE):
        """Подгружаем лист в клетку"""
        if REFLECTED_PAGE:
            self.clear_paper = Image.open(
                os.path.join(self.path_global_image_folder, 'cell_reflected.jpg')
            )
        else:
            self.clear_paper = Image.open(
                os.path.join(self.path_global_image_folder, 'cell.jpg')
            )
        self.clear_paper.load()
        draw = ImageDraw.Draw(self.clear_paper)
        return self.clear_paper

    def _load_line_list(self, REFLECTED_PAGE):
        """Подгружаем лист в линию"""
        if REFLECTED_PAGE:
            clear_paper = Image.open(
                os.path.join(self.path_global_image_folder, 'line_reflected.jpg')
            )
        else:
            clear_paper = Image.open(
                os.path.join(self.path_global_image_folder, 'line.jpg')
            )
        self.clear_paper.load()
        draw = ImageDraw.Draw(self.clear_paper)
        return draw

    def open_image(self, REFLECTED_PAGE):
        if self.page_type == 'cell':
            return self._load_cell_list(REFLECTED_PAGE)
        if self.page_type == 'line':
            return self._load_line_list(REFLECTED_PAGE)

    def save_image(self, user_id, str_number):
        # global clear_paper
        path = os.path.join(self.path_save_image_folder, f'{user_id}_{int(time.time())}_{str_number}.jpg')
        self.clear_paper.save(path)
        self.clear_paper.close()
        return path


class Fonts(object):
    def __init__(self, path_fonts_folder, font_name, size):
        self.path_fonts_folder = path_fonts_folder
        self.font_name = font_name
        self.size = size

    def _font_list(self):
        fonts = {
            "Merkucio": os.path.join(self.path_fonts_folder, "Merkucio Font4You.ttf"),
            "Abram": os.path.join(self.path_fonts_folder, "Abram.ttf"),
            "Gregory": os.path.join(self.path_fonts_folder, "Gregory.ttf"),
            "Lorenco": os.path.join(self.path_fonts_folder, "Lorenco.ttf"),
            "Merk": os.path.join(self.path_fonts_folder, "Merk.ttf"),
            "Salavat": os.path.join(self.path_fonts_folder, "Salavat.ttf"),
        }
        return fonts[self.font_name]

    def font(self):
        font_use = self._font_list()
        font_use = ImageFont.truetype(font_use, self.size, encoding='unic')
        return font_use


class CreatePhoto(OpenImage, Fonts):
    REFLECTED_PAGE = False
    spaser_word = 30
    COLOR_USE = False
    list_size = 1600
    height_list = 38*61

    def __init__(self, path_save_image_folder,
                 path_fonts_folder, size,
                 text, user_id, font_color, font_name, page_type, path_global_image_folder):
        self.text = text
        self.user_id = user_id
        self.font_color = font_color
        self.font_name = font_name
        self.page_type = page_type
        self.path_global_image_folder = path_global_image_folder
        OpenImage.__init__(self, path_save_image_folder, page_type, path_global_image_folder)
        Fonts.__init__(self, path_fonts_folder, font_name, size)

    def config(self, page_type, font_use):
        if page_type == 'cell':
            offset = 34  # 39
            if font_use == 'Merkucio':
                list_size = 1600
            elif font_use == 'Abram':
                list_size = 1525
            else:
                list_size = 1600
        if page_type == 'line':
            offset = 94
            if font_use == 'Merkucio':
                list_size = 1625
            elif font_use == 'Abram':
                list_size = 1585
            else:
                list_size = 1625
        return offset, list_size

    def create(self):
        # Подгружаем шрифт
        font_use = self.font()
        # Подгружаем картинку
        page = self.open_image(self.REFLECTED_PAGE)
        # print(self.page_type, font_use)
        offset, self.list_size = self.config(self.page_type, font_use)
        # номер сохранения страницы
        str_number = 0
        text_split = []
        paths = []
        line_number = 0
        # разбиваем на абзатцы
        for i in self.text.split('\n\n'):
            text_split.append(
                split_a_text(text=i, width_all=self.list_size,
                             font_use=font_use,
                             spaser_word=self.spaser_word)
            )
        if self.page_type == 'cell':
            global_line_start = 300 if self.REFLECTED_PAGE else 75
        elif self.page_type == 'line':
            global_line_start = 250 if self.REFLECTED_PAGE else 75
        for abzats in text_split:
            for stroka in abzats:
                # Создаём новую страницу
                if (line_number == 20 and self.page_type == 'cell'):
                    offset = 38
                    paths.append(self.save_image(self.user_id, str_number))
                    str_number += 1
                    #  Смена страниц
                    self.REFLECTED_PAGE = False if self.REFLECTED_PAGE else True
                    page = self.open_image(self.REFLECTED_PAGE)
                    line_number = 0
                    global_line_start = 300 if self.REFLECTED_PAGE else 75

                if (str_number == 25 and self.page_type == 'line'):
                    offset = 94
                    paths.append(self.save_image(self.user_id, str_number))
                    str_number += 1
                    #  Смена страниц
                    self.REFLECTED_PAGE = False if self.REFLECTED_PAGE else True
                    page = self.open_image(self.REFLECTED_PAGE)
                    line_number = 0
                    global_line_start = 250 if self.REFLECTED_PAGE else 75

                # Задаём разные отступы вначале строки
                line_start = random.randint(global_line_start-15, global_line_start+15)
                # width, height = font_use.getsize(stroka)
                # if self.list_size-width > 150:
                #     if stroka.split()[0][0].isupper():
                #         self.line_start = self.line_start + \
                #             random.randint(0, int((self.list_size-width)/5))
                D = Drawing(
                    COLOR_USE=self.COLOR_USE,
                    stroka=stroka,
                    font_use=font_use,
                    list_size=self.list_size,
                    clear_paper=page,
                    line_start=line_start,
                    offset=offset,
                    spaser_word=self.spaser_word,
                    font_color=self.font_color,
                    font_name=self.font_name
                )
                D.draw()
                # Выбираем отсуп по типу листа
                if self.page_type == 'cell':
                    offset += 118
                if self.page_type == 'line':
                    # После пятой строчки увеличивает отступ
                    if line_number <= 10:
                        offset += 87
                    elif line_number <= 18:
                        offset += 88
                    else:
                        offset += 88
                line_number += 1

        paths.append(
            self.save_image(self.user_id, str_number)
        )
        return paths


# text = """Как принято считать, сделанные на базе интернет-аналитики выводы являются только методом политического участия и превращены в посмешище, хотя само их существование приносит несомненную пользу обществу. Сложно сказать, почему интерактивные прототипы смешаны с не уникальными данными до степени совершенной неузнаваемости, из-за чего возрастает их статус бесполезности. В целом, конечно, синтетическое тестирование в значительной степени обусловливает важность анализа существующих паттернов поведения.
# Как уже неоднократно упомянуто, акционеры крупнейших компаний, вне зависимости от их уровня, должны быть подвергнуты целой серии независимых исследований. Не следует, однако, забывать, что разбавленное изрядной долей эмпатии, рациональное мышление в значительной степени обусловливает важность как самодостаточных, так и внешне зависимых концептуальных решений. Каждый из нас понимает очевидную вещь: разбавленное изрядной долей эмпатии, рациональное мышление требует определения и уточнения модели развития. Значимость этих проблем настолько очевидна, что начало повседневной работы по формированию позиции не оставляет шанса для направлений прогрессивного развития! Прежде всего, высококачественный прототип будущего проекта говорит о возможностях дальнейших направлений развития.
# Задача организации, в особенности же дальнейшее развитие различных форм деятельности играет определяющее значение для дальнейших направлений развития. Принимая во внимание показатели успешности, сложившаяся структура организации говорит о возможностях благоприятных перспектив.
# """
# CP = CreatePhoto(
#     path_save_image_folder='D:\\w\\text_to_list\\bot_v.2.0\\IMG\\',
#     path_global_image_folder='D:\\w\\text_to_list\\bot_v.2.0\\PAGES\\',

#     path_fonts_folder='D:\w\\text_to_list\\bot_v.2.0\\Fonts\\',
#     size=85,

#     text=text,
#     user_id=123,
#     font_color='49, 88, 143',
#     font_name='Merkucio',
#     page_type='cell')
# print(CP.create())
