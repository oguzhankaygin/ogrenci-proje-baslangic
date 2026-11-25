import unittest

from src.{{paket}} import topla


class ToplaTesti(unittest.TestCase):
    def test_iki_sayiyi_toplar(self):
        self.assertEqual(topla(2, 3), 5)
