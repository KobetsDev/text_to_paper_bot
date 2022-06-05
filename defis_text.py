import split_text


def split_a_text(text, width_all, font_use, spaser_word=0):
    """Функция переносов слов, и создание строк

    Возвращает массив строк

    Args:

        text (str): Текст
        widthall (int): Размер листа
        font_use (font_use): шрифт которым пишется
        spaser_word (int, optional): пробелы между словами. Defaults to 0.
        startindent (int, optional): Отступ параграфа. Defaults to 0.
    """
    pogr = 100  # На сколько текст может вылазить на поля
    lines = []  # Массив со строками
    line_width = 0  # Длина строки
    line_now = ''  # Текущая строка
    now_word = 0
    words = text.split()
    for word in words:
        separated_word = split_text.split_word(word)
        # print(separated_word)
        width, height = font_use.getsize(word + ' ')
        # print(word, width)

        # Если длина строки меньше всей длины строки
        if line_width < width_all:
            # Если длина строки + длина слова(и пробела) + длина пробела МЕНЬШЕ длины все строки
            if (line_width + width + spaser_word) < width_all:
                # Слово помещается
                line_now += word + ' '
                line_width += width + spaser_word
            else:
                # Берём длину первого слога
                width, height = font_use.getsize(separated_word[0])
                # Если длина строки + длина первого слога МЕНЬШЕ длины всей строки ИЛИ не выступает дальше чем pogr
                if (line_width + width < width_all) or (width < pogr):
                    # Слово помещается по слогам
                    transfer_word = ''  # Слово для переноса
                    count_slog = 0  # Кол-во слогов
                    # Проходимся по слогам
                    for slog in separated_word:
                        # Берём длинуслогов что уже были(или нет) + слог
                        width, height = font_use.getsize(transfer_word + slog)
                        # Если длина строки + длина первого слога МЕНЬШЕ длины всей строки ИЛИ не выступает дальше чем pogr
                        if (line_width + width < width_all) or (width < pogr):
                            transfer_word += slog
                            count_slog += 1
                        else:
                            break
                    # Если длина слогов - кол-во слогов не равно 0
                    # В общем если слово полностью не осталось на конце строки
                    if len(separated_word) - count_slog != 0:
                        # print(f'Часть слова останется "{transfer_word}"')
                        # Получаем длину слога
                        width_slog, height_slog = font_use.getsize(transfer_word + '-')
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
                                words.insert(now_word+1, text_s)
                        else:
                            words.insert(now_word+1, word)
                    else:
                        line_now += word
                else:
                    # Слово не помещается
                    words.insert(now_word+1, word)
                lines.append(line_now)
                line_width = 0
                line_now = ''  # Очищаем строку
        now_word += 1
    if len(line_now) > 0:
        lines.append(line_now)
    # print(lines)
    return lines
