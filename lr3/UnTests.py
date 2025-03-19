import unittest
from itertools import combinations

# Импортируем функции, которые нужно протестировать
from main import merge_terms, minimize_form_calculational, minimize_cnf_tabular

class TestLogicFunctions(unittest.TestCase):

    # Тесты для функции merge_terms
    def test_merge_terms(self):
        # Склеивание возможно
        self.assertEqual(merge_terms(['0', '1', '1'], ['0', '1', '0']), ['0', '1', 'X'])
        self.assertEqual(merge_terms(['1', '0', '1'], ['1', '1', '1']), ['1', 'X', '1'])
        self.assertEqual(merge_terms(['1', '0', '0'], ['1', '0', '1']), ['1', '0', 'X'])

        # Склеивание невозможно
        self.assertIsNone(merge_terms(['0', '0', '0'], ['1', '1', '1']))  # Все переменные разные
        self.assertIsNone(merge_terms(['0', '1', '0'], ['1', '0', '1']))  # Две переменные разные

    # Тесты для функции minimize_form_calculational
    def test_minimize_form_calculational(self):
        # Минимизация DNF
        dnf = [
            ['0', '1', '1'],  # ¬a ∧ b ∧ c
            ['1', '0', '0'],   # a ∧ ¬b ∧ ¬c
            ['1', '0', '1'],   # a ∧ ¬b ∧ c
            ['1', '1', '0'],   # a ∧ b ∧ ¬c
            ['1', '1', '1']    # a ∧ b ∧ c
        ]
        expected_dnf = [['1', 'X', 'X'], ['X', '1', '1']]  # Ожидаемый результат: a ∨ (b ∧ c)
        self.assertEqual(minimize_form_calculational(dnf), expected_dnf)

        # Минимизация CNF
        cnf = [
            ['1', '1', '1'],  # a ∨ b ∨ c
            ['1', '0', '0'],  # a ∨ ¬b ∨ ¬c
            ['1', '0', '1'],  # a ∨ ¬b ∨ c
            ['1', '1', '0'],  # a ∨ b ∨ ¬c
            ['0', '1', '1']   # ¬a ∨ b ∨ c
        ]
        expected_cnf = [['1', 'X', 'X'], ['X', '1', '1']]  # Ожидаемый результат: a ∧ (b ∨ c)
        self.assertEqual(minimize_form_calculational(cnf), expected_cnf)

    # Тесты для функции minimize_cnf_tabular
    def test_minimize_cnf_tabular(self):
        cnf = [
            ['1', '1', '1'],  # a ∨ b ∨ c
            ['1', '0', '0'],  # a ∨ ¬b ∨ ¬c
            ['1', '0', '1'],  # a ∨ ¬b ∨ c
            ['1', '1', '0'],  # a ∨ b ∨ ¬c
            ['0', '1', '1']   # ¬a ∨ b ∨ c
        ]
        expected_cnf = [['1', '1', '1'], ['1', '0', '0']]  # Ожидаемый результат
        self.assertEqual(minimize_cnf_tabular(cnf), expected_cnf)

# Запуск тестов
if __name__ == "__main__":
    unittest.main()