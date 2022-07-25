from dataclasses import dataclass
import random
from PIL import Image, ImageDraw, ImageFont
# from numba import prange


@dataclass
class Drawing:
    """Рисуем чернилами на листке"""
    COLOR_USE: bool
    text: str
    font_use: ImageFont
    list_size: int
    clear_paper: ImageDraw
    line_start: int
    offset: int
    spaser_word: int
    font_name: str
    font_color: list

    def _drawing_word(self, number: int, slovo: str):
        """Рисуем слово"""
        img_slovo = Image.new('RGBA', (self.width+number, self.height),
                              (255, random.randint(0, 150),
                               random.randint(0, 200), self.color_word))
        draw = ImageDraw.Draw(img_slovo)

        draw.text((number, 0), slovo, fill=tuple(self.font_color[:3]), font=self.font_use)
        return img_slovo

    def _drawing_line(self, mass_img: list):
        """Рисуем слова на строке"""
        for slovo in self.text.split():
            # print(self.width, self.height)
            new_size = self.font_use.getbbox(slovo)
            self.width, self.height = new_size[2], new_size[3]
            self.color_word = 200 if self.COLOR_USE else 0
            # Пишем на этой картинке шрифтом
            number = 15 if self.font_name == 'Salavat' else 10
            img_slovo = self._drawing_word(number, slovo)
            # поварачиваем текст
            ran_rotate = random.uniform(-2.0, 1.5)
            img_slovo = img_slovo.rotate(ran_rotate, expand=True)
            # img_slovo = img_slovo.transform(img_slovo.size, Image.AFFINE, (1, 20, 0, 0, 1, 0), resample=Image.BICUBIC)
            # Добавляем картинку со словом в масив
            mass_img.append(img_slovo)
        return mass_img

    def _paste_on_paper(self, mass_img: list, clear_paper: ImageDraw):
        """Рисуем строки на листке"""
        self.color_line = 155 if self.COLOR_USE else 0
        # Создаём картинку всей строки
        stroka_img = Image.new('RGBA', (self.list_size, 135), (255, 255, 255, self.color_line))
        line_width = 0
        for i, line in enumerate(mass_img):
            # Узнаём ширину картинки)
            width = mass_img[i].width
            # Наносим картинку фото на картинку строки
            ran_down_text = random.randint(-2, 2)
            stroka_img.paste(mass_img[i], (line_width, ran_down_text),
                             mask=mass_img[i])
            # Если есть это не последнее слово то добавляем после него пробел
            # рандомный отступ между слов
            ran_spase = random.randint(25, 35)  # 30/len(mass_img)
            line_width += width + ran_spase  # spaser_word  # 30
        clear_paper.paste(stroka_img, (self.line_start, self.offset), mask=stroka_img)

    def draw(self):
        mass_img = []
        mass_img = self._drawing_line(mass_img)
        self._paste_on_paper(mass_img, self.clear_paper)
