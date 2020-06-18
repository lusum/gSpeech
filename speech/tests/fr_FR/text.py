from os.path import dirname, join
from unittest import TestCase

from speech.textutils import text_to_dict

from .data import datas


class TestTextConversion(TestCase):
    def test_text(self):
        for data in datas:
            text = data['ini']
            transform = data['new']
            lang = 'fr-FR'
            result = text_to_dict(
                text,
                join(
                    dirname(dirname(dirname(dirname(__file__)))),
                    'dict',
                    lang.replace('-', '_')
                ),
                lang
            )
            self.assertEqual(transform, result)
