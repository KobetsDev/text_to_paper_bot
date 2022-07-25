from dataclasses import dataclass
import split_text
from PIL import ImageFont


@dataclass
class SplitText:
    text: str
    font_use: ImageFont
    spaser_word: int
    width_all: int

    # @classmethod
    def _get_word_width(self, text):
        """Получаем ширину текста"""
        # width2, height = self.font_use.getsize(text)
        # width = self.font_use.getlength(text)
        # print(self.font_use.getlength(text))
        # width1 = self.font_use.getbbox(text)[2]
        # print('\ngetbbox', width1, '\ngetsize', width2)
        # print(self.font_use.getsize(text), self.font_use.getmask(text).getbbox())
        return self.font_use.getbbox(text)[2]  # int(self.font_use.getlength(text))  # -110

    def split(self):
        pogr = 100  # На сколько текст может вылазить на поля
        lines = []  # Массив со строками
        line_width = 0  # Длина строки
        line_now = ''  # Текущая строка
        num_word = 0
        words = self.text.split()
        for word in words:
            separated_word = split_text.split_word(word)
            # print(separated_word)
            width = self._get_word_width(word + ' ')
            # Если длина строки меньше всей длины строки
            if line_width < self.width_all:
                # Если длина строки + длина слова(и пробела) + длина пробела МЕНЬШЕ длины все строки
                if (line_width + width + self.spaser_word) < self.width_all:
                    # Слово помещается
                    line_now += word + ' '
                    line_width += width + self.spaser_word
                else:
                    # Берём длину первого слога
                    width = self._get_word_width(separated_word[0])
                    # Если длина строки + длина первого слога МЕНЬШЕ длины всей строки ИЛИ не выступает дальше чем pogr
                    if (line_width + width < self.width_all) or (width < pogr):
                        # Слово помещается по слогам
                        transfer_word = ''  # Слово для переноса
                        count_slog = 0  # Кол-во слогов
                        # Проходимся по слогам
                        for slog in separated_word:
                            # Берём длинуслогов что уже были(или нет) + слог
                            width = self._get_word_width(transfer_word + slog)
                            # Если длина строки + длина первого слога МЕНЬШЕ длины всей строки ИЛИ не выступает дальше чем pogr
                            if (line_width + width < self.width_all) or (width < pogr):
                                transfer_word += slog
                                count_slog += 1
                            else:
                                break
                        # Если длина слогов - кол-во слогов не равно 0
                        # В общем если слово полностью не осталось на конце строки
                        if len(separated_word) - count_slog != 0:
                            # print(f'Часть слова останется "{transfer_word}"')
                            # Получаем длину слога
                            width_slog = self._get_word_width(transfer_word + '-')
                            line_width += width_slog
                            text_s = ''
                            # Проходимся по слогам в слове
                            for el in range(len(separated_word) - count_slog):
                                text_s = separated_word[len(separated_word)-el-1] + text_s
                            if len(transfer_word) >= 2:
                                if len(text_s) < 2:
                                    # print('Остается 1 буква')
                                    line_now += word
                                else:
                                    line_now += transfer_word + '-'
                                    words.insert(num_word+1, text_s)
                            else:
                                words.insert(num_word+1, word)
                        else:
                            line_now += word
                    else:
                        # Слово не помещается
                        words.insert(num_word+1, word)
                    lines.append(line_now)
                    line_width = 0
                    line_now = ''  # Очищаем строку
            num_word += 1
            # print(line_width)
        if len(line_now) > 0:
            lines.append(line_now)
        return lines
