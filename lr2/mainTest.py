import unittest
import itertools
from main import *

class TestLogicFunctions(unittest.TestCase):

    def test_tokenize(self):
        """Тест разбиения выражения на токены."""
        self.assertEqual(tokenize("(a∨b)∧!c"), ["(", "a", "∨", "b", ")", "∧", "!", "c"])
        self.assertEqual(tokenize("a->b"), ["a", "->", "b"])
        self.assertEqual(tokenize("!(a∧b)"), ["!", "(", "a", "∧", "b", ")"])

    def test_to_postfix(self):
        """Тест перевода выражения в обратную польскую запись (RPN)."""
        self.assertEqual(to_postfix(["a", "∨", "b"]), ["a", "b", "∨"])
        self.assertEqual(to_postfix(["a", "∧", "b"]), ["a", "b", "∧"])
        self.assertEqual(to_postfix(["!", "a"]), ["a", "!"])
        self.assertEqual(to_postfix(["a", "->", "b"]), ["a", "b", "->"])
        self.assertEqual(to_postfix(["a", "∨", "b", "∧", "c"]), ["a", "b", "c", "∧", "∨"])



    def test_generate_truth_table(self):
        """Тест генерации таблицы истинности."""
        variables = ["a", "b"]
        expression = "a ∨ b"
        expected_table = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 1)
        ]
        result = generate_truth_table(variables, expression)
        self.assertEqual(result, expected_table)

    def test_build_sdnf_sknf(self):
        """Тест построения СДНФ и СКНФ."""
        table = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)]
        variables = ["a", "b"]
        expected_sdnf = "(¬a ∧ b) ∨ (a ∧ ¬b) ∨ (a ∧ b)"
        expected_sknf = "(a ∨ b)"
        expected_sdnf_nums = (1, 2, 3)
        expected_sknf_nums = (0,)

        result_sdnf, result_sknf, sdnf_nums, sknf_nums = build_sdnf_sknf(table, variables)

        self.assertEqual(result_sdnf, expected_sdnf)
        self.assertEqual(result_sknf, expected_sknf)
        self.assertEqual(sdnf_nums, expected_sdnf_nums)
        self.assertEqual(sknf_nums, expected_sknf_nums)

    def test_compute_index_form(self):
        """Тест вычисления индексной формы функции."""
        table = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)]
        expected_index_form = "0111 - 7"
        result = compute_index_form(table)
        self.assertEqual(result, expected_index_form)


if __name__ == "__main__":
    unittest.main()
