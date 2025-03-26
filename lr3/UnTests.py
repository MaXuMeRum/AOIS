import unittest
from io import StringIO
import sys
from unittest.mock import patch
from main import (input_terms, minimize_sknf_calculation,
                         minimize_sdnf_calculation, minimize_sknf_table)


class TestLogicMinimization(unittest.TestCase):
    def setUp(self):
        # Сохраняем оригинальный stdout
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Восстанавливаем stdout
        sys.stdout = self.original_stdout

    def test_input_terms(self):
        # Тест для функции ввода термов
        with patch('builtins.input', side_effect=['a∨b', '¬a∨c', '']):
            terms = input_terms(2)
            self.assertEqual(terms, ['a∨b', '¬a∨c'])

    def test_minimize_sknf_calculation(self):
        # Тест минимизации СКНФ
        variables = ['a', 'b', 'c']
        terms = ['a∨b∨c', 'a∨b∨¬c', 'a∨¬b∨c']

        minimize_sknf_calculation(variables, terms)

        output = sys.stdout.getvalue()
        self.assertIn('a∨b', output)
        self.assertIn('a∨c', output)
        self.assertIn('Минимизированная СКНФ', output)

    def test_minimize_sdnf_calculation(self):
        # Тест минимизации СДНФ
        variables = ['a', 'b', 'c']
        terms = ['¬a∧b∧c', 'a∧¬b∧¬c', 'a∧¬b∧c', 'a∧b∧¬c', 'a∧b∧c']

        minimize_sdnf_calculation(variables, terms)

        output = sys.stdout.getvalue()
        self.assertIn('a∧¬b', output)
        self.assertIn('a∧b', output)
        self.assertIn('Минимизированная СДНФ', output)

    def test_minimize_sknf_table(self):
        # Тест табличного метода минимизации СКНФ
        variables = ['a', 'b']
        terms = ['a∨b', 'a∨¬b']

        minimize_sknf_table(variables, terms)

        output = sys.stdout.getvalue()
        self.assertIn('a', output)
        self.assertIn('Импликанты\\Термы', output)
        self.assertIn('Минимизированная СКНФ', output)

    def test_empty_input(self):
        # Тест пустого ввода
        variables = ['a', 'b']
        terms = []

        minimize_sknf_calculation(variables, terms)
        output = sys.stdout.getvalue()
        self.assertIn('Не удалось минимизировать', output)

    def test_no_minimization_possible(self):
        # Тест случая, когда минимизация невозможна
        variables = ['a', 'b']
        terms = ['a∨b', '¬a∨¬b']

        minimize_sknf_calculation(variables, terms)
        output = sys.stdout.getvalue()
        self.assertIn('Невозможно минимизировать дальше', output)


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_single_term_sknf(self):
        variables = ['a', 'b']
        terms = ['a∨b']

        minimize_sknf_calculation(variables, terms)
        output = sys.stdout.getvalue()
        self.assertIn('Невозможно минимизировать дальше', output)

    def test_duplicate_terms(self):
        variables = ['a', 'b']
        terms = ['a∨b', 'a∨b']

        minimize_sknf_calculation(variables, terms)
        output = sys.stdout.getvalue()
        self.assertIn('Невозможно минимизировать дальше', output)

    def test_all_variables_used(self):
        variables = ['a', 'b', 'c']
        terms = ['a∨b∨c', 'a∨b∨¬c']

        minimize_sknf_calculation(variables, terms)
        output = sys.stdout.getvalue()
        self.assertIn('a∨b', output)


if __name__ == '__main__':
    unittest.main()