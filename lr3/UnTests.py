import unittest
import itertools
import operator
from collections import defaultdict
from main import BooleanMinimizer  # Замените 'your_module' на имя вашего файла

class TestBooleanMinimizer(unittest.TestCase):

    def test__get_literals(self):
        self.assertEqual(BooleanMinimizer._get_literals("a∧¬b"), {"a", "¬b"})
        self.assertEqual(BooleanMinimizer._get_literals("a"), {"a"})
        self.assertEqual(BooleanMinimizer._get_literals("¬b"), {"¬b"})
        self.assertEqual(BooleanMinimizer._get_literals("a∧b∧c"), {"a", "b", "c"})
        self.assertEqual(BooleanMinimizer._get_literals("¬a∨¬b∨¬c"), {"¬a", "¬b", "¬c"})
        self.assertEqual(BooleanMinimizer._get_literals(""), set())
        self.assertEqual(BooleanMinimizer._get_literals("a1b"), {"a", "b"}) # Проверка игнорирования небуквенных символов

    def test__are_adjacent(self):
        self.assertEqual(BooleanMinimizer._are_adjacent("a", "¬a"), set())
        self.assertEqual(BooleanMinimizer._are_adjacent("a∧b", "a∧¬b"), {"a"})
        self.assertEqual(BooleanMinimizer._are_adjacent("a∨b", "a∨¬b"), {"a"})
        self.assertEqual(BooleanMinimizer._are_adjacent("a∧b", "c∧d"), None)
        self.assertEqual(BooleanMinimizer._are_adjacent("a∧b∧c", "a∧b∧¬c"), {"a", "b"})
        self.assertEqual(BooleanMinimizer._are_adjacent("a∧¬b∧c", "¬a∧¬b∧c"), {"¬b", "c"})
        self.assertEqual(BooleanMinimizer._are_adjacent("a", "b"), None)
        self.assertEqual(BooleanMinimizer._are_adjacent("¬a", "b"), None)

    def test__detect_operator(self):
        self.assertEqual(BooleanMinimizer._detect_operator(["a∧b", "a∧c"]), "∧")
        self.assertEqual(BooleanMinimizer._detect_operator(["a∨b", "a∨c"]), "∨")
        self.assertEqual(BooleanMinimizer._detect_operator(["a", "b"]), None)
        self.assertEqual(BooleanMinimizer._detect_operator(["a∧b", "c∨d"]), "∧") # Возвращает первый найденный бинарный оператор


    def test__add_unused_terms(self):
        current_terms = ["a", "b", "c", "d"]
        new_terms = ["a", "c"]
        used_indices = {0, 2}
        result = BooleanMinimizer._add_unused_terms(current_terms, new_terms, used_indices)
        self.assertEqual(sorted(result), sorted(["a", "c", "b", "d"]))

    def test__check_redundant_implicants_dnf(self):
        terms_dnf = ["a∧b", "a", "b∧c"]
        redundant_dnf = BooleanMinimizer._check_redundant_implicants(terms_dnf, True)
        self.assertEqual(redundant_dnf, {0})

        terms_no_redundant_dnf = ["a", "b", "c"]
        redundant_no_redundant_dnf = BooleanMinimizer._check_redundant_implicants(terms_no_redundant_dnf, True)
        self.assertEqual(redundant_no_redundant_dnf, set())

    def test__check_redundant_implicants_knf(self):
        terms_knf = ["a∨b", "a", "b∨c"]
        redundant_knf = BooleanMinimizer._check_redundant_implicants(terms_knf, False)
        self.assertEqual(redundant_knf, {1}) # 'a' покрывает 'a∨b'

        terms_no_redundant_knf = ["a", "b", "c"]
        redundant_no_redundant_knf = BooleanMinimizer._check_redundant_implicants(terms_no_redundant_knf, False)
        self.assertEqual(redundant_no_redundant_knf, set())

    def test__build_coverage_table_dnf(self):
        prime_implicants = ["a", "b"]
        terms = ["a∧c", "b∧d"]
        coverage = BooleanMinimizer._build_coverage_table(prime_implicants, terms, True)
        self.assertEqual(len(coverage), 2)
        self.assertEqual(coverage[0][0], "a")
        self.assertEqual(coverage[0][1], ["X", " "])
        self.assertEqual(coverage[1][0], "b")
        self.assertEqual(coverage[1][1], [" ", "X"])

    def test__build_coverage_table_knf(self):
        prime_implicants = ["a", "b"]
        terms = ["a∨c", "b∨d"]
        coverage = BooleanMinimizer._build_coverage_table(prime_implicants, terms, False)
        self.assertEqual(len(coverage), 2)
        self.assertEqual(coverage[0][0], "a")
        self.assertEqual(coverage[0][1], [" ", " "])
        self.assertEqual(coverage[1][0], "b")
        self.assertEqual(coverage[1][1], [" ", " "])

    def test__select_minimal_coverage_dnf(self):
        coverage = [("a", ["X", " "]), ("b", [" ", "X"]), ("c", ["X", "X"])]
        terms = ["t1", "t2"]
        selected = BooleanMinimizer._select_minimal_coverage(coverage, terms, True)
        self.assertIn("c", selected)
        self.assertNotIn("a", selected)
        self.assertNotIn("b", selected)

        coverage_essential = [("a", ["X", " "]), ("b", [" ", "X"])]
        selected_essential = BooleanMinimizer._select_minimal_coverage(coverage_essential, terms, True)
        self.assertIn("a", selected_essential)
        self.assertIn("b", selected_essential)

    def test__select_minimal_coverage_knf(self):
        coverage = [("a", ["X", " "]), ("b", [" ", "X"]), ("c", ["X", "X"])]
        terms = ["t1", "t2"]
        selected = BooleanMinimizer._select_minimal_coverage(coverage, terms, False)
        self.assertEqual(set(selected), {"a", "b", "c"}) # Для КНФ выбираются все простые импликанты

    def test__create_karnaugh_map_2_vars(self):
        values = [{"a": 0, "b": 0}, {"a": 1, "b": 0}, {"a": 1, "b": 1}]
        variables = ["a", "b"]
        k_map = BooleanMinimizer._create_karnaugh_map(values, variables, 2)
        self.assertEqual(k_map, [[1, 1], [0, 1]])

    def test__create_karnaugh_map_3_vars(self):
        values = [{"a": 0, "b": 0, "c": 0}, {"a": 1, "b": 0, "c": 0}, {"a": 1, "b": 1, "c": 0}, {"a": 0, "b": 1, "c": 1}]
        variables = ["a", "b", "c"]
        k_map = BooleanMinimizer._create_karnaugh_map(values, variables, 3)
        self.assertEqual(k_map, [[1, 0], [1, 0], [1, 0], [0, 1]])

    def test__create_karnaugh_map_4_vars(self):
        values = [{"a": 0, "b": 0, "c": 0, "d": 0}, {"a": 1, "b": 0, "c": 0, "d": 0},
                  {"a": 1, "b": 1, "c": 0, "d": 0}, {"a": 0, "b": 1, "c": 0, "d": 0},
                  {"a": 0, "b": 0, "c": 1, "d": 0}]
        variables = ["a", "b", "c", "d"]
        k_map = BooleanMinimizer._create_karnaugh_map(values, variables, 4)
        expected_map = [[1, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
        self.assertEqual(k_map, expected_map)

    def test__create_karnaugh_map_5_vars(self):
        values = [{"a": 0, "b": 0, "c": 0, "d": 0, "e": 0}, {"a": 1, "b": 0, "c": 0, "d": 0, "e": 1}]
        variables = ["a", "b", "c", "d", "e"]
        k_map = BooleanMinimizer._create_karnaugh_map(values, variables, 5)
        expected_map0 = [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        expected_map1 = [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(k_map[0], expected_map0)
        self.assertEqual(k_map[1], expected_map1)

    def test__format_result_dnf(self):
        prime_implicants = [frozenset({'a'}), frozenset({'¬b', 'c'})]
        variables = ['a', 'b', 'c']
        result = BooleanMinimizer._format_result(prime_implicants, variables, True)
        self.assertEqual(result, "(a) ∨ (¬b ∧ c)")

    def test__format_result_knf(self):
        prime_implicants = [frozenset({'a'}), frozenset({'¬b', 'c'})]
        variables = ['a', 'b', 'c']
        result = BooleanMinimizer._format_result(prime_implicants, variables, False)
        self.assertEqual(result, "(a) ∧ (¬b ∨ c)")

    def test__quine_mccluskey_basic(self):
        minterms = [frozenset({'a'}), frozenset({'¬a'})]
        result = BooleanMinimizer._quine_mccluskey(minterms, 1)
        self.assertEqual(set(result), {frozenset()})

    def test__quine_mccluskey_3_vars(self):
        minterms = [frozenset({'a', 'b', 'c'}), frozenset({'a', 'b', '¬c'}),
                    frozenset({'a', '¬b', 'c'}), frozenset({'¬a', 'b', 'c'})]
        result = BooleanMinimizer._quine_mccluskey(minterms, 3)
        self.assertTrue(frozenset({'a', 'b'}) in result)
        self.assertTrue(frozenset({'a', 'c'}) in result)
        self.assertTrue(frozenset({'b', 'c'}) in result)

    def test__quine_mccluskey_4_vars(self):
        minterms = [frozenset({'¬a', '¬b', '¬c', '¬d'}), frozenset({'a', '¬b', '¬c', '¬d'}),
                    frozenset({'¬a', 'b', '¬c', '¬d'}), frozenset({'¬a', '¬b', 'c', '¬d'})]
        result = BooleanMinimizer._quine_mccluskey(minterms, 4)
        self.assertTrue(frozenset({'¬b', '¬c', '¬d'}) in result)
        self.assertTrue(frozenset({'¬a', '¬c', '¬d'}) in result)
        self.assertTrue(frozenset({'¬a', '¬b', '¬d'}) in result)

    # Тесты для методов, которые в основном выводят информацию, требуют проверки stdout
    # или могут быть протестированы через их побочные эффекты, если таковые имеются.
    # Поскольку minimize_calculus_method, minimize_table_calculus_method и minimize_karnaugh
    # в основном выводят информацию и вызывают другие протестированные методы,
    # прямое юнит-тестирование их внутреннего поведения может быть сложным без
    # рефакторинга для возврата промежуточных состояний.

    # Мы можем проверить, что они вызываются без ошибок для различных входных данных.
    def test_minimize_calculus_method_dnf(self):
        terms_dnf = ["a∧b", "a∧¬b"]
        try:
            BooleanMinimizer.minimize_calculus_method(terms_dnf, True)
            self.assertTrue(True) # Если не было исключения, тест считается пройденным
        except Exception as e:
            self.fail(f"Вызвано исключение: {e}")

    def test_minimize_calculus_method_knf(self):
        terms_knf = ["a∨b", "a∨¬b"]
        try:
            BooleanMinimizer.minimize_calculus_method(terms_knf, False)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Вызвано исключение: {e}")

    def test_minimize_table_calculus_method_dnf(self):
        terms_dnf = ["a∧b", "a∧¬b", "¬a∧b", "¬a∧¬b"]
        try:
            BooleanMinimizer.minimize_table_calculus_method(terms_dnf, True)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Вызвано исключение: {e}")

    def test_minimize_table_calculus_method_knf(self):
        terms_knf = ["a∨b", "a∨¬b", "¬a∨b", "¬a∨¬b"]
        try:
            BooleanMinimizer.minimize_table_calculus_method(terms_knf, False)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Вызвано исключение: {e}")

    def test_minimize_karnaugh_2_vars(self):
        terms = ["a∧b", "a∧¬b", "¬a∧b"]
        variables = ["a", "b"]
        try:
            BooleanMinimizer.minimize_karnaugh(terms, variables, True)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Вызвано исключение: {e}")

    def test_minimize_karnaugh_5_vars(self):
        terms = ["a∧b∧c∧d∧e", "¬a∧b∧c∧d∧e"]
        variables = ["a", "b", "c", "d", "e"]
        try:
            BooleanMinimizer.minimize_karnaugh(terms, variables, True)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Вызвано исключение: {e}")

    def test_minimize_karnaugh_more_than_5_vars(self):
        terms = ["a", "b"]
        variables = ["a", "b", "c", "d", "e", "f"]
        result = BooleanMinimizer.minimize_karnaugh(terms, variables, True)
        self.assertEqual(result, "(a) ∨ (b)") # Ожидаем исходные термы

if __name__ == '__main__':
    unittest.main()