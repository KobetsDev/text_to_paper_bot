# -*- coding: utf-8 -*-
import os
import random
import sys
import time
from dataclasses import dataclass

from dotenv import load_dotenv
from PIL import Image, ImageFont

from art_to_page import Drawing
from defis_text import SplitText

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, 'config.env'))


@dataclass
class OpenImage(object):
    """Открываем картинку листка"""
    path_save_image_folder: str
    page_type: str
    path_global_image_folder: str

    def _load_cell_list(self, REFLECTED_PAGE: bool):
        """Подгружаем лист в клетку"""
        file = 'cell_reflected.jpg' if REFLECTED_PAGE else 'cell.jpg'

        clear_paper = Image.open(
            os.path.join(self.path_global_image_folder, file)
        )
        clear_paper.load()
        return clear_paper

    def _load_line_list(self, REFLECTED_PAGE: bool):
        """Подгружаем лист в линию"""
        file = 'line_reflected.jpg' if REFLECTED_PAGE else 'line.jpg'
        clear_paper = Image.open(
            os.path.join(self.path_global_image_folder, file)
        )
        clear_paper.load()
        return clear_paper

    def open_image(self, REFLECTED_PAGE):
        if self.page_type == 'cell':
            return self._load_cell_list(REFLECTED_PAGE)
        elif self.page_type == 'line':
            return self._load_line_list(REFLECTED_PAGE)
        else:
            raise ValueError('Переданы не существующий тип листка')

    def save_image(self, user_id: int, str_number: str, page):
        # global clear_paper
        path = os.path.join(self.path_save_image_folder, f'{user_id}_{int(time.time())}_{str_number}.jpg')
        page.save(path)
        page.close()
        return path


@dataclass
class Fonts:
    path_fonts_folder: str
    font_name: str
    size: int

    def __post_init__(self):
        self.merkucio: str = os.path.join(self.path_fonts_folder, "Merkucio Font4You.ttf")
        self.abram: str = os.path.join(self.path_fonts_folder, "Abram.ttf")
        self.gregory: str = os.path.join(self.path_fonts_folder, "Gregory.ttf")
        self.lorenco: str = os.path.join(self.path_fonts_folder, "Lorenco.ttf")
        self.merk: str = os.path.join(self.path_fonts_folder, "Merk.ttf")
        self.salavat: str = os.path.join(self.path_fonts_folder, "Salavat.ttf")

    def _font_list(self) -> str:
        fonts = {
            "Merkucio": self.merkucio,
            "Abram": self.abram,
            "Gregory": self.gregory,
            "Lorenco": self.lorenco,
            "Merk": self.merk,
            "Salavat": self.salavat,
        }
        return fonts[self.font_name]

    def font(self):
        font_use = self._font_list()
        font_use = ImageFont.truetype(font_use, self.size, encoding='unic')
        return font_use


@dataclass
class CreatePhoto(OpenImage, Fonts):
    # height_list = int(os.environ.get('height_list'))
    path_save_image_folder: str
    path_fonts_folder: str
    size: int
    text: str
    user_id: int
    font_color: str
    font_name: str
    page_type: str
    path_global_image_folder: str
    REFLECTED_PAGE: bool = False
    spaser_word: int = int(os.environ.get('spaser_word'))
    COLOR_USE: bool = int(os.environ.get('COLOR_USE'))
    list_size: int = int(os.environ.get('list_size'))

    def _config(self, page_type, font_use):
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

    @classmethod
    def __get_split_text(cls, text, font_use) -> list:
        """Разбиваем текст на строки"""
        text_split = []
        for i in text.split('\n\n'):
            ST = SplitText(text=i,
                           font_use=font_use,
                           spaser_word=cls.spaser_word,
                           width_all=cls.list_size)
            text_split.append(ST.split())
        return text_split

    def create(self) -> list:
        # Подгружаем шрифт
        font_use = self.font()
        # Подгружаем картинку
        page = self.open_image(self.REFLECTED_PAGE)
        # print(self.page_type, font_use)
        offset, self.list_size = self._config(self.page_type, font_use)
        # номер сохранения страницы
        str_number = 0
        paths = []
        line_number = 0
        # разбиваем на абзатцы
        text_split = self.__get_split_text(text, font_use)
        # text_split.append(
        #     split_a_text(text=i, width_all=self.list_size,
        #                  font_use=font_use,
        #                  spaser_word=self.spaser_word)
        # )
        if self.page_type == 'cell':
            global_line_start = 300 if self.REFLECTED_PAGE else 75
        elif self.page_type == 'line':
            global_line_start = 250 if self.REFLECTED_PAGE else 75
        for abzats in text_split:
            for stroka in abzats:
                # print(line_number)
                # Создаём новую страницу
                if (line_number == 20 and self.page_type == 'cell'):
                    offset = 38
                    paths.append(self.save_image(self.user_id, str_number, page))
                    str_number += 1
                    #  Смена страниц
                    self.REFLECTED_PAGE = False if self.REFLECTED_PAGE else True
                    page = self.open_image(self.REFLECTED_PAGE)
                    line_number = 0
                    global_line_start = 300 if self.REFLECTED_PAGE else 75

                if (line_number == 25 and self.page_type == 'line'):
                    offset = 94
                    paths.append(self.save_image(self.user_id, str_number, page))
                    str_number += 1
                    #  Смена страниц
                    self.REFLECTED_PAGE = False if self.REFLECTED_PAGE else True
                    page = self.open_image(self.REFLECTED_PAGE)
                    print(line_number)
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
                    text=stroka,
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
            self.save_image(self.user_id, str_number, page)
        )
        return paths


# text = """Как принято считать, сделанные на базе интернет-аналитики выводы являются только методом политического участия и превращены в посмешище, хотя само их существование приносит несомненную пользу обществу. Сложно сказать, почему интерактивные прототипы смешаны с не уникальными данными до степени совершенной неузнаваемости, из-за чего возрастает их статус бесполезности. В целом, конечно, синтетическое тестирование в значительной степени обусловливает важность анализа существующих паттернов поведения.
# Как уже неоднократно упомянуто, акционеры крупнейших компаний, вне зависимости от их уровня, должны быть подвергнуты целой серии независимых исследований. Не следует, однако, забывать, что разбавленное изрядной долей эмпатии, рациональное мышление в значительной степени обусловливает важность как самодостаточных, так и внешне зависимых концептуальных решений. Каждый из нас понимает очевидную вещь: разбавленное изрядной долей эмпатии, рациональное мышление требует определения и уточнения модели развития. Значимость этих проблем настолько очевидна, что начало повседневной работы по формированию позиции не оставляет шанса для направлений прогрессивного развития! Прежде всего, высококачественный прототип будущего проекта говорит о возможностях дальнейших направлений развития.
# Задача организации, в особенности же дальнейшее развитие различных форм деятельности играет определяющее значение для дальнейших направлений развития. Принимая во внимание показатели успешности, сложившаяся структура организации говорит о возможностях благоприятных перспектив.
# """
# absFilePath = os.path.abspath(__file__)
# BASE_DIR = os.path.dirname(absFilePath)
# CP = CreatePhoto(
#     path_save_image_folder=os.path.join(BASE_DIR, 'IMG'),
#     path_global_image_folder=os.path.join(BASE_DIR, 'PAGES'),

#     path_fonts_folder=os.path.join(BASE_DIR, 'Fonts'),
#     size=85,

#     text=text,
#     user_id=123,
#     # font_color='49, 88, 143',
#     font_color=[48, 75, 143],
#     font_name='Merkucio',
#     page_type='line')
# print(CP.create())
