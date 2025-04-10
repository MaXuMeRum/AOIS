import unittest
from collections import defaultdict
from main import BooleanMinimizer

class TestBooleanMinimizer(unittest.TestCase):
    def setUp(self):
        self.minimizer = BooleanMinimizer()

    def test_get_literals(self):
        # Тестирование извлечения литералов из термов
        self.assertEqual(self.minimizer._get_literals("a∧b"), {'a', 'b'})
        self.assertEqual(self.minimizer._get_literals("¬a∧b"), {'¬a', 'b'})
        self.assertEqual(self.minimizer._get_literals("a∧¬b∨c"), {'a', '¬b', 'c'})
        self.assertEqual(self.minimizer._get_literals("¬a∧¬b∧¬c"), {'¬a', '¬b', '¬c'})
        self.assertEqual(self.minimizer._get_literals("a∨b∨c"), {'a', 'b', 'c'})

    def test_are_adjacent(self):
        # Тестирование поиска соседних термов
        self.assertEqual(
            self.minimizer._are_adjacent("a∧b∧c", "a∧b∧¬c"),
            {'a', 'b'}
        )
        self.assertEqual(
            self.minimizer._are_adjacent("a∧¬b∧c", "a∧b∧c"),
            {'a', 'c'}
        )
        self.assertIsNone(self.minimizer._are_adjacent("a∧b", "a∧c"))
        self.assertIsNone(self.minimizer._are_adjacent("a∧b", "c∧d"))
        self.assertEqual(
            self.minimizer._are_adjacent("¬a∧b∧¬c", "¬a∧b∧c"),
            {'¬a', 'b'}
        )

    def test_detect_operator(self):
        # Тестирование определения оператора
        self.assertEqual(self.minimizer._detect_operator(["a∧b", "b∧c"]), "∧")
        self.assertEqual(self.minimizer._detect_operator(["a∨b", "b∨c"]), "∨")
        self.assertIsNone(self.minimizer._detect_operator(["a", "b"]))
        self.assertEqual(self.minimizer._detect_operator(["a∧b∨c"]), "∧")

    def test_minimize_calculus_method_dnf(self):
        # Тестирование минимизации СДНФ расчетным методом
        terms = ["a∧b∧c", "a∧b∧¬c", "a∧¬b∧c"]
        result = self.minimizer.minimize_calculus_method(terms, True)
        self.assertTrue("(a∧b)" in result)
        self.assertTrue("(a∧c)" in result)

    def test_minimize_calculus_method_cnf(self):
        # Тестирование минимизации СКНФ расчетным методом
        terms = ["a∨b∨c", "a∨b∨¬c", "a∨¬b∨c"]
        result = self.minimizer.minimize_calculus_method(terms, False)
        self.assertTrue("(a∨b)" in result)
        self.assertTrue("(a∨c)" in result)

    def test_minimize_table_calculus_method_dnf(self):
        # Тестирование минимизации СДНФ расчетно-табличным методом
        terms = ["a∧b∧c", "a∧b∧¬c", "¬a∧b∧¬c", "¬a∧¬b∧c"]
        result = self.minimizer.minimize_table_calculus_method(terms, True)
        self.assertTrue("(b∧¬c)" in result or "(a∧b)" in result)
        self.assertTrue("(¬a∧¬b∧c)" in result)

    def test_minimize_table_calculus_method_cnf(self):
        # Тестирование минимизации СКНФ расчетно-табличным методом
        terms = ["a∨b∨c", "a∨b∨¬c", "¬a∨b∨¬c", "¬a∨¬b∨c"]
        result = self.minimizer.minimize_table_calculus_method(terms, False)
        self.assertTrue("(b∨¬c)" in result or "(a∨b)" in result)
        self.assertTrue("(¬a∨¬b∨c)" in result)

    def test_minimize_karnaugh_2vars(self):
        # Тестирование минимизации методом Карно для 2 переменных
        terms = ["a∧b", "a∧¬b"]
        vars = ['a', 'b']
        result = self.minimizer.minimize_karnaugh(terms, vars, True)
        self.assertEqual(result, "(a)")

    def test_minimize_karnaugh_3vars(self):
        terms = ["a∧b∧c", "a∧b∧¬c", "¬a∧b∧¬c", "¬a∧¬b∧c"]
        vars = ['a', 'b', 'c']
        result = self.minimizer.minimize_karnaugh(terms, vars, True)
        print("3vars result:", result)  # <--- вот это
        self.assertTrue("(b∧¬c)" in result.replace(" ", ""))

    def test_minimize_karnaugh_4vars(self):
        # Тестирование минимизации методом Карно для 4 переменных
        terms = ["a∧b∧c∧d", "a∧b∧¬c∧d", "¬a∧b∧¬c∧d", "¬a∧¬b∧c∧¬d"]
        vars = ['a', 'b', 'c', 'd']
        result = self.minimizer.minimize_karnaugh(terms, vars, True).replace(" ", "")
        self.assertTrue("(b∧d)" in result or "(a∧b∧d)" in result)
        self.assertTrue("(¬a∧¬b∧c∧¬d)" in result)

    def test_minimize_karnaugh_5vars(self):
        # Тестирование минимизации методом Карно для 5 переменных
        terms = ["a∧b∧c∧d∧e", "a∧b∧¬c∧d∧e", "¬a∧b∧¬c∧d∧¬e"]
        vars = ['a', 'b', 'c', 'd', 'e']
        result = self.minimizer.minimize_karnaugh(terms, vars, True).replace(" ", "")
        self.assertTrue("(b∧d∧e)" in result or "(a∧b∧d∧e)" in result)
        self.assertTrue("(¬a∧b∧¬c∧d∧¬e)" in result)

    def test_quine_mccluskey(self):
        # Тестирование алгоритма Квайна-МакКласки
        minterms = [
            {'a', 'b', 'c'},
            {'a', 'b', '¬c'},
            {'¬a', 'b', '¬c'},
            {'¬a', '¬b', 'c'}
        ]
        result = self.minimizer._quine_mccluskey(minterms, 3)
        expected = [
            {'b', '¬c'},
            {'a', 'b'},
            {'¬a', '¬b', 'c'}
        ]
        self.assertEqual(len(result), len(expected))
        for imp in expected:
            self.assertTrue(any(imp == set(pi) for pi in result))

if __name__ == '__main__':
    unittest.main()