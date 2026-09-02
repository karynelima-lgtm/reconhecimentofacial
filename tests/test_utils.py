import unittest

from utils import classificar_pessoa


class TestClassificacaoPessoa(unittest.TestCase):
    def test_pessoas_iguais(self):
        self.assertEqual(classificar_pessoa(True), "Mesma pessoa")

    def test_pessoas_diferentes(self):
        self.assertEqual(classificar_pessoa(False), "Pessoas diferentes")


if __name__ == "__main__":
    unittest.main()
