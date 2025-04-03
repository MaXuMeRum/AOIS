from main import *
import unittest
from main import Minimizer


class TestMinimizer(unittest.TestCase):
    def setUp(self):
        self.variables = ['a', 'b', 'c']
        self.minimizer = Minimizer(self.variables)

    def test_term_to_str(self):
        self.assertEqual(self.minimizer.term_to_str((0, 1, 1)), "¬abc")
        self.assertEqual(self.minimizer.term_to_str((1, 0, 0)), "a¬b¬c")
        self.assertEqual(self.minimizer.term_to_str((1, 1, 1)), "abc")

    def test_str_to_term(self):
        self.assertEqual(self.minimizer.str_to_term("¬abc"), (0, 1, 1))
        self.assertEqual(self.minimizer.str_to_term("a¬b¬c"), (1, 0, 0))
        self.assertEqual(self.minimizer.str_to_term("abc"), (1, 1, 1))

    def test_is_implicant_covered(self):
        implicant = ('1', 'X', '1')
        self.assertTrue(self.minimizer.is_implicant_covered(implicant, (1, 0, 1)))
        self.assertTrue(self.minimizer.is_implicant_covered(implicant, (1, 1, 1)))
        self.assertFalse(self.minimizer.is_implicant_covered(implicant, (0, 1, 1)))

    def test_calculate_method_dnf(self):
        terms = [
            (0, 1, 1),  # ¬abc
            (1, 0, 0),  # a¬b¬c
            (1, 0, 1),  # a¬bc
            (1, 1, 0),  # ab¬c
            (1, 1, 1)  # abc
        ]
        result = self.minimizer.calculate_method(terms, is_dnf=True)
        self.assertTrue("a" in result)
        self.assertTrue("bc" in result)

    def test_calculate_method_cnf(self):
        terms = [
            (0, 0, 0),  # ¬a¬b¬c
            (0, 0, 1),  # ¬a¬bc
            (0, 1, 0),  # ¬ab¬c
            (1, 0, 1),  # a¬bc
            (1, 1, 0)  # ab¬c
        ]
        result = self.minimizer.calculate_method(terms, is_dnf=False)
        self.assertTrue("¬a" in result or "¬b" in result or "¬c" in result)

    def test_table_method_dnf(self):
        terms = [
            (0, 1, 1),  # ¬abc
            (1, 0, 0),  # a¬b¬c
            (1, 0, 1),  # a¬bc
            (1, 1, 0),  # ab¬c
            (1, 1, 1)  # abc
        ]
        result = self.minimizer.table_method(terms, is_dnf=True)
        self.assertTrue("a" in result)
        self.assertTrue("bc" in result)

    def test_karnaugh_method_dnf(self):
        terms = [
            (0, 1, 1),  # ¬abc
            (1, 0, 0),  # a¬b¬c
            (1, 0, 1),  # a¬bc
            (1, 1, 0),  # ab¬c
            (1, 1, 1)  # abc
        ]
        result = self.minimizer.karnaugh_method(terms, is_dnf=True)
        # Проверяем оба возможных варианта минимизации
        self.assertTrue("a ∨ bc" in result or "a ∨ b¬c" in result)

    def test_implicant_to_str(self):
        self.assertEqual(self.minimizer.implicant_to_str(('1', 'X', '1')), "ac")
        self.assertEqual(self.minimizer.implicant_to_str(('X', '0', '1')), "¬bc")
        self.assertEqual(self.minimizer.implicant_to_str(('0', 'X', 'X')), "¬a")

    def test_minimization_with_two_variables(self):
        minimizer = Minimizer(['a', 'b'])
        terms = [
            (0, 1),  # ¬ab
            (1, 0),  # a¬b
            (1, 1)  # ab
        ]
        result = minimizer.calculate_method(terms, is_dnf=True)
        self.assertTrue("a" in result)
        self.assertTrue("b" in result)


if __name__ == '__main__':
    unittest.main()