
import unittest
import os
import PIL

from mainPic import OpenImage, Fonts, CreatePhoto
from split_text import split_word
from defis_text import SplitText

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
text = """Прежде всего, сплочённость команды профессионалов требует определения и уточнения форм воздействия. Однозначно, многие известные личности и по сей день остаются уделом либералов, которые жаждут быть в равной степени предоставлены сами себе. Господа, высококачественный прототип будущего проекта выявляет срочную потребность поставленных обществом задач. Сложно сказать, почему сделанные на базе интернет-аналитики выводы и по сей день остаются уделом либералов, которые жаждут быть ассоциативно распределены по отраслям. Каждый из нас понимает очевидную вещь: убеждённость некоторых оппонентов говорит о возможностях направлений прогрессивного развития.
            First of all, the cohesion of the team of professionals requires the definition and clarification of the forms of influence. Definitely, many famous personalities to this day remain the lot of liberals who crave to be equally left to themselves. Gentlemen, a high-quality prototype of a future project reveals the urgent need for the tasks set by society. It is difficult to say why the conclusions made on the basis of Internet analytics to this day remain the lot of liberals who crave to be associatively distributed by industry. Each of us understands the obvious thing: the conviction of some opponents speaks about the possibilities of the directions of progressive development."""
spaser_word = 30
font_name = 'Merkucio'


# class TestSplitText(unittest.TestCase):
#     def setUp(self) -> None:
#         self.splitText = SplitText(text=text,
#                                    width_all=1600,
#                                    font_use=font_name,
#                                    spaser_word=spaser_word)

#     def test_split(self) -> None:
#         print('qwe')
#         print(self.splitText.split())
# self.assertEqual(self.splitText.split())


class TestSplitText(unittest.TestCase):

    def test_split(self) -> None:
        self.assertEqual(split_word('Превосходящий'), ['Пре', 'вос', 'хо', 'дя', 'щий'])


class TestMainPic(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self) -> None:
        self.openImage = OpenImage(path_save_image_folder=os.path.join(BASE_DIR, 'IMG'),
                                   path_global_image_folder=os.path.join(BASE_DIR, 'PAGES'),
                                   page_type='cell')
        self.font = Fonts(path_fonts_folder=os.path.join(BASE_DIR, 'Fonts'),
                          font_name=font_name,
                          size=85)

        self.createPhoto = CreatePhoto(
            path_save_image_folder=os.path.join(BASE_DIR, 'IMG'),
            path_global_image_folder=os.path.join(BASE_DIR, 'PAGES'),

            path_fonts_folder=os.path.join(BASE_DIR, 'Fonts'),
            size=85,

            text=text,
            user_id=12345,
            font_color=[48, 75, 143],
            font_name='Merkucio',
            page_type='line',
        )

    def test_open(self):
        REFLECTED_PAGE = True
        self.assertIsInstance(self.openImage.open_image(REFLECTED_PAGE), PIL.JpegImagePlugin.JpegImageFile)

    def test_font(self):
        self.assertIsInstance(self.font.font(), PIL.ImageFont.FreeTypeFont)

    def test_photo(self):
        created_protos = self.createPhoto.create()
        self.assertNotEqual(len(created_protos), 0)
        # Delete images
        # for photo in created_protos:
        #     os.remove(photo)


if __name__ == "__main__":
    unittest.main()
