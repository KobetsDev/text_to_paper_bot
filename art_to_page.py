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

    def __drawing_line(self):
        """Рисуем слова на строке"""
        for slovo in self.stroka.split():
            width1, height1 = self.font_use.getsize(slovo)
            cl1 = 200 if self.COLOR_USE else 0
            # Пишем на этой картинке шрифтом
            if self.font_name == 'Salavat':
                img_slovo = Image.new(
                    'RGBA', (width1+15, height1), (255, random.randint(0, 150), random.randint(0, 200), cl1))
                draw2 = ImageDraw.Draw(img_slovo)
                draw2.text((15, 0), slovo, fill=(int(self.font_color[0]), int(
                    self.font_color[1]), int(self.font_color[2])), font=self.font_use)
            else:
                img_slovo = Image.new(
                    'RGBA', (width1+10, height1), (255, random.randint(0, 150), random.randint(0, 200), cl1))
                draw2 = ImageDraw.Draw(img_slovo)
                draw2.text((10, 0), slovo, fill=(int(self.font_color[0]), int(
                    self.font_color[1]), int(self.font_color[2])), font=self.font_use)
            # поварачиваем текст
            ran_rotate = random.uniform(-2.0, 1.5)
            img_slovo = img_slovo.rotate(ran_rotate, expand=True)
            # img_slovo = img_slovo.transform(img_slovo.size, Image.AFFINE, (1, 20, 0, 0, 1, 0), resample=Image.BICUBIC)
            # Добавляем картинку со словом в масив
            self.mass_img.append(img_slovo)
        return self.mass_img

    def __paste_on_paper(self):
        """Рисуем строки на листке"""
        cl = 155 if self.COLOR_USE else 0
        # Создаём картинку всей строки
        stroka_img = Image.new('RGBA', (self.list_size, 135), (255, 255, 255, cl))
        len_width = 0
        for i in range(len(self.mass_img)):
            # Узнаём ширену картинки
            width = self.mass_img[i].width
            # Наносим картинку фото на картинку строки
            ran_down_text = random.randint(-2, 2)
            stroka_img.paste(self.mass_img[i], (len_width, ran_down_text),
                             mask=self.mass_img[i])
            # try:
            # Если есть это не последнее слово то добавляем после него пробел
            # a = mass_img[i + 1]
            # рандомный отступ между слов
            ran_spase = random.randint(25, 35)  # 30/len(mass_img)
            # print(ran_spase)
            len_width += width + ran_spase  # spaser_word  # 30
            # except:
            #     len_width += width
        self.clear_paper.paste(stroka_img, (self.line_start, self.offset), mask=stroka_img)

    def draw(self):
        self.mass_img = []
        self.font_color = str(self.font_color).split(", ")
        self.__drawing_line()
        self.__paste_on_paper()
