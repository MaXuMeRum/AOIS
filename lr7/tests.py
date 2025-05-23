import unittest
from main import CustomDiagonalGrid


class TestCustomDiagonalGrid(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой матрицы 4x4 перед каждым тестом"""
        self.grid = CustomDiagonalGrid(4, 4)
        # Заполним матрицу тестовыми данными
        for col in range(4):
            self.grid.store_data_row([1, 0, 1, 0], 0, col)

    def test_store_and_fetch_data_row(self):
        """Тест записи и чтения строки данных"""
        test_data = [1, 0, 1, 1]
        self.grid.store_data_row(test_data, 0, 0)
        result = self.grid.fetch_data_row(0, 0, 4)
        self.assertEqual(result, test_data)

    def test_store_and_fetch_diagonal_data(self):
        """Тест записи и чтения диагональных данных"""
        test_data = [1, 0, 1, 0]
        self.grid.store_diagonal_data(test_data, 0, 0)
        result = self.grid.fetch_diagonal_data(0, 0, 4)
        self.assertEqual(result, test_data)

    def test_f1_conjunction(self):
        """Тест операции f1 (конъюнкция, И)"""
        self.grid.store_data_row([1, 0, 1, 0], 0, 0)  # Столбец 0
        self.grid.store_data_row([1, 1, 0, 0], 0, 1)  # Столбец 1
        result = self.grid.f1(0, 1, 2)  # Результат в столбец 2
        self.assertEqual(result, [1 & 1, 0 & 1, 1 & 0, 0 & 0])  # [1, 0, 0, 0]
        # Проверяем, что результат записался в столбец 2
        self.assertEqual(self.grid.fetch_data_row(0, 2, 4), [1, 0, 0, 0])

    def test_f14_nand(self):
        """Тест операции f14 (И-НЕ)"""
        self.grid.store_data_row([1, 0, 1, 0], 0, 0)  # Столбец 0
        self.grid.store_data_row([1, 1, 0, 0], 0, 1)  # Столбец 1
        result = self.grid.f14(0, 1, 2)  # Результат в столбец 2
        expected = [1 if not (a & b) else 0 for a, b in zip([1, 0, 1, 0], [1, 1, 0, 0])]
        self.assertEqual(result, expected)  # [0, 1, 1, 1]
        self.assertEqual(self.grid.fetch_data_row(0, 2, 4), expected)

    def test_f3_repeat(self):
        """Тест операции f3 (повторение 1 аргумента)"""
        test_data = [1, 0, 1, 1]
        self.grid.store_data_row(test_data, 0, 0)  # Столбец 0
        result = self.grid.f3(0, 1, 2)  # Копируем столбец 0 в 2, игнорируя столбец 1
        self.assertEqual(result, test_data)
        self.assertEqual(self.grid.fetch_data_row(0, 2, 4), test_data)

    def test_f12_invert(self):
        """Тест операции f12 (отрицание 1 аргумента)"""
        test_data = [1, 0, 1, 1]
        self.grid.store_data_row(test_data, 0, 0)  # Столбец 0
        result = self.grid.f12(0, 1, 2)  # Инвертируем столбец 0 в 2, игнорируя столбец 1
        expected = [0, 1, 0, 0]
        self.assertEqual(result, expected)
        self.assertEqual(self.grid.fetch_data_row(0, 2, 4), expected)

    def test_binary_addition(self):
        """Тест двоичного сложения"""
        result = self.grid.binary_addition([1, 0, 1], [1, 1, 0])
        self.assertEqual(result, [1, 0, 1, 1])  # 5 + 6 = 11 (1011)

    def test_process_key_fields(self):
        """Тест обработки ключевых полей"""
        test_grid = CustomDiagonalGrid(4, 4)
        test_data = [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Ключ 101
        test_grid.store_data_row(test_data[:4], 0, 0)
        test_grid.store_data_row(test_data[4:8], 0, 1)
        test_grid.store_data_row(test_data[8:12], 0, 2)
        test_grid.store_data_row(test_data[12:], 0, 3)

        test_grid.process_key_fields([1, 0, 1])
        result = test_grid.fetch_data_row(0, 0, 4)
        self.assertEqual(result[3:7], [0])  # Проверяем часть результата

    def test_find_closest_values(self):
        """Тест поиска ближайших значений"""
        test_grid = CustomDiagonalGrid(4, 4)
        test_data = [
            [0, 0, 0, 0],  # Столбец 0
            [0, 0, 1, 1],  # Столбец 1 (target)
            [0, 0, 1, 0],  # Столбец 2 (ближайшее снизу)
            [0, 1, 0, 0]   # Столбец 3 (ближайшее сверху)
        ]
        for col in range(4):
            test_grid.store_data_row(test_data[col], 0, col)

        below_col, below_word, above_col, above_word = test_grid.find_closest_values([0, 0, 1, 1])

        self.assertEqual(below_col, 3)
        self.assertEqual(below_word, [0, 0, 1, 0])
        self.assertEqual(above_col, 1)
        self.assertEqual(above_word, [0, 1, 1, 0])


if __name__ == '__main__':
    unittest.main()