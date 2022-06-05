import random
from PIL import Image, ImageDraw
# from numba import prange


class Drawing(object):
    """Рисуем чернилами на листке"""

    def __init__(self, COLOR_USE, stroka, font_use, list_size, clear_paper,
                 line_start, offset, spaser_word, font_color, font_name):
        self.COLOR_USE = COLOR_USE
        self.stroka = stroka
        self.font_use = font_use
        self.list_size = list_size
        self.clear_paper = clear_paper
        self.line_start = line_start
        self.offset = offset
        self.spaser_word = spaser_word
        self.font_name = font_name
        self.font_color = font_color

    def _drawing_word(self, number, slovo):
        """Рисуем слово"""
        img_slovo = Image.new('RGBA', (self.width+number, self.height),
                              (255, random.randint(0, 150),
                               random.randint(0, 200), self.color_word))
        draw = ImageDraw.Draw(img_slovo)
        draw.text((number, 0), slovo, fill=(
            int(self.font_color[0]),
            int(self.font_color[1]),
            int(self.font_color[2])
        ), font=self.font_use)
        return img_slovo

    def _drawing_line(self):
        """Рисуем слова на строке"""
        for slovo in self.stroka.split():
            self.width, self.height = self.font_use.getsize(slovo)
            self.color_word = 200 if self.COLOR_USE else 0
            # Пишем на этой картинке шрифтом
            if self.font_name == 'Salavat':
                img_slovo = self._drawing_word(15, slovo)
            else:
                img_slovo = self._drawing_word(10, slovo)
            # поварачиваем текст
            ran_rotate = random.uniform(-2.0, 1.5)
            img_slovo = img_slovo.rotate(ran_rotate, expand=True)
            # img_slovo = img_slovo.transform(img_slovo.size, Image.AFFINE, (1, 20, 0, 0, 1, 0), resample=Image.BICUBIC)
            # Добавляем картинку со словом в масив
            self.mass_img.append(img_slovo)
        return self.mass_img

    def _paste_on_paper(self):
        """Рисуем строки на листке"""
        self.color_line = 155 if self.COLOR_USE else 0
        # Создаём картинку всей строки
        stroka_img = Image.new('RGBA', (self.list_size, 135), (255, 255, 255, self.color_line))
        line_width = 0
        for i in range(len(self.mass_img)):
            # Узнаём ширину картинки)
            width = self.mass_img[i].width
            # Наносим картинку фото на картинку строки
            ran_down_text = random.randint(-2, 2)
            stroka_img.paste(self.mass_img[i], (line_width, ran_down_text),
                             mask=self.mass_img[i])
            # Если есть это не последнее слово то добавляем после него пробел
            # рандомный отступ между слов
            ran_spase = random.randint(25, 35)  # 30/len(mass_img)
            # print(ran_spase)
            line_width += width + ran_spase  # spaser_word  # 30
            # except:
            #     len_width += width
        self.clear_paper.paste(stroka_img, (self.line_start, self.offset), mask=stroka_img)

    def draw(self):
        self.mass_img = []
        self.font_color = str(self.font_color).split(", ")
        self._drawing_line()
        self._paste_on_paper()
