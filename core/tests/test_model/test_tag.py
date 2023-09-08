from django.test import TestCase

from core import models
from core import factories


class Tag(TestCase):
    def setUp(self):
        self.tag = factories.Tag()

    def test_str(self):
        """
        Тест строки
        """
        self.assertEqual(str(self.tag), self.tag.name, "проверка строкового метода")
